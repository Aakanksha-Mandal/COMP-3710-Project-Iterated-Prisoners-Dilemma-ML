import argparse  # CLI arguments for flexible experiment control
import csv  # Save experiment outputs in tabular format
from collections import defaultdict  # Group runs by memory depth for aggregation
from pathlib import Path  # Cross-platform paths

# Fixed opponent pool builder for fair comparisons
from src.experiments.opponent_pool import get_opponent_pool

# GA runner + configuration dataclass
from src.optim.genetic_algorithm import run_ga, GAConfig


def parse_int_list(value: str):
    """Parse comma-separated integers: '3,5' -> [3, 5]."""
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def first_reach_fraction_of_best(history, fraction: float = 0.99):
    """First generation where best_fitness reaches fraction of final best."""
    final_best = max(row["best_fitness"] for row in history)
    threshold = final_best * fraction
    for row in history:
        if row["best_fitness"] >= threshold:
            return row["generation"]
    return None


def last_improvement_generation(history):
    """Last generation that set a new global best_fitness."""
    best_so_far = float("-inf")
    last_gen = 0
    for row in history:
        if row["best_fitness"] > best_so_far:
            best_so_far = row["best_fitness"]
            last_gen = row["generation"]
    return last_gen


def save_history(history, out_path: Path):
    """Save generation-level fitness history for one run."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["generation", "best_fitness", "avg_fitness"])
        for row in history:
            w.writerow([row["generation"], row["best_fitness"], row["avg_fitness"]])


def main():
    parser = argparse.ArgumentParser(description="Run GA depth sweep (e.g., depth 3 vs 5).")

    # Sweep dimensions
    parser.add_argument("--depths", type=str, default="3,5", help="Comma-separated memory depths")
    parser.add_argument("--seeds", type=str, default="42,43,44", help="Comma-separated GA seeds")

    # GA settings (kept constant across runs for fair depth comparison)
    parser.add_argument("--population-size", type=int, default=80)
    parser.add_argument("--generations", type=int, default=200)
    parser.add_argument("--mutation-rate", type=float, default=0.001)
    parser.add_argument("--crossover-rate", type=float, default=0.8)
    parser.add_argument("--elite-size", type=int, default=2)
    parser.add_argument("--rounds", type=int, default=200)

    # Opponent pool settings
    parser.add_argument("--num-random-opponents", type=int, default=10)
    parser.add_argument("--opponent-pool-seed", type=int, default=42)

    # Output naming
    parser.add_argument("--tag", type=str, default="", help="Optional filename tag suffix")

    args = parser.parse_args()

    depths = parse_int_list(args.depths)
    seeds = parse_int_list(args.seeds)

    out_dir = Path("results") / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    tag = f"_{args.tag}" if args.tag else ""
    per_run_summary_path = out_dir / f"ga_depth_sweep_runs{tag}.csv"
    depth_summary_path = out_dir / f"ga_depth_sweep_summary{tag}.csv"

    # Collect rows for per-depth aggregation
    rows_by_depth = defaultdict(list)

    with per_run_summary_path.open("w", newline="", encoding="utf-8") as fsum:
        wsum = csv.writer(fsum)
        wsum.writerow([
            "run_id",
            "memory_depth",
            "population_size",
            "generations",
            "crossover_rate",
            "mutation_rate",
            "elite_size",
            "rounds",
            "ga_seed",
            "opponent_pool_seed",
            "num_random_opponents",
            "best_fitness_overall",
            "final_best_fitness",
            "final_avg_fitness",
            "first_gen_reach_99pct_best",
            "last_improvement_generation",
            "best_bitstring"
        ])

        run_id = 0
        for depth in depths:
            for seed in seeds:
                run_id += 1

                # Keep comparison fair: same GA settings and same opponent pool seed,
                # changing only memory depth and GA seed.
                cfg = GAConfig(
                    population_size=args.population_size,
                    generations=args.generations,
                    crossover_rate=args.crossover_rate,
                    mutation_rate=args.mutation_rate,
                    elite_size=args.elite_size,
                    rounds=args.rounds,
                    seed=seed,
                    memory_depth=depth,
                )

                opponent_pool = get_opponent_pool(
                    seed=args.opponent_pool_seed,
                    num_random=args.num_random_opponents,
                    memory_depth=depth,
                )

                best, best_fit, history = run_ga(opponent_pool, cfg)

                history_path = out_dir / f"ga_fitness_history_depth{depth}_seed{seed}{tag}.csv"
                save_history(history, history_path)

                final_best = history[-1]["best_fitness"]
                final_avg = history[-1]["avg_fitness"]
                first99 = first_reach_fraction_of_best(history, 0.99)
                last_imp = last_improvement_generation(history)

                row = {
                    "run_id": run_id,
                    "memory_depth": depth,
                    "population_size": cfg.population_size,
                    "generations": cfg.generations,
                    "crossover_rate": cfg.crossover_rate,
                    "mutation_rate": cfg.mutation_rate,
                    "elite_size": cfg.elite_size,
                    "rounds": cfg.rounds,
                    "ga_seed": cfg.seed,
                    "opponent_pool_seed": args.opponent_pool_seed,
                    "num_random_opponents": args.num_random_opponents,
                    "best_fitness_overall": best_fit,
                    "final_best_fitness": final_best,
                    "final_avg_fitness": final_avg,
                    "first_gen_reach_99pct_best": first99,
                    "last_improvement_generation": last_imp,
                    "best_bitstring": best,
                }

                rows_by_depth[depth].append(row)

                wsum.writerow([
                    row["run_id"],
                    row["memory_depth"],
                    row["population_size"],
                    row["generations"],
                    row["crossover_rate"],
                    row["mutation_rate"],
                    row["elite_size"],
                    row["rounds"],
                    row["ga_seed"],
                    row["opponent_pool_seed"],
                    row["num_random_opponents"],
                    row["best_fitness_overall"],
                    row["final_best_fitness"],
                    row["final_avg_fitness"],
                    row["first_gen_reach_99pct_best"],
                    row["last_improvement_generation"],
                    row["best_bitstring"],
                ])

                print(
                    f"[Run {run_id}] depth={depth} seed={seed} "
                    f"best={best_fit:.3f} final_best={final_best:.3f} saved={history_path.name}"
                )

    # Aggregate per depth: mean and max over seeds
    with depth_summary_path.open("w", newline="", encoding="utf-8") as fdepth:
        wdepth = csv.writer(fdepth)
        wdepth.writerow([
            "memory_depth",
            "n_runs",
            "mean_best_fitness_overall",
            "max_best_fitness_overall",
            "mean_final_best_fitness",
            "mean_final_avg_fitness",
            "mean_first_gen_reach_99pct_best",
            "mean_last_improvement_generation",
        ])

        for depth in sorted(rows_by_depth.keys()):
            rows = rows_by_depth[depth]
            n = len(rows)
            mean_best_overall = sum(r["best_fitness_overall"] for r in rows) / n
            max_best_overall = max(r["best_fitness_overall"] for r in rows)
            mean_final_best = sum(r["final_best_fitness"] for r in rows) / n
            mean_final_avg = sum(r["final_avg_fitness"] for r in rows) / n
            mean_first99 = sum(r["first_gen_reach_99pct_best"] for r in rows) / n
            mean_last_imp = sum(r["last_improvement_generation"] for r in rows) / n

            wdepth.writerow([
                depth,
                n,
                mean_best_overall,
                max_best_overall,
                mean_final_best,
                mean_final_avg,
                mean_first99,
                mean_last_imp,
            ])

    print(f"\nSaved per-run sweep table: {per_run_summary_path}")
    print(f"Saved per-depth summary:  {depth_summary_path}")


if __name__ == "__main__":
    main()
