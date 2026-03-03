# Runs the GA experiment and writes summary/history outputs to CSV files.

import argparse  # CLI args for reproducible experiment settings.
import csv  # CSV writer for saving experiment outputs.
from pathlib import Path  # Cross-platform path handling.

# Builds the pool of opponents the GA-evolved strategy is evaluated against.
from src.experiments.opponent_pool import get_opponent_pool
# GA runner + configuration dataclass.
from src.optim.genetic_algorithm import run_ga, GAConfig


# Save final best GA result (one row) to CSV.
def save_best(best_bitstring: str, best_fitness: float, cfg: GAConfig, out_path: Path):
    # Ensure output directory exists before writing.
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Open CSV in text mode with UTF-8.
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Header columns for reproducibility and reporting.
        w.writerow([
            "method", "memory_depth", "population_size", "generations", "crossover_rate", "mutation_rate",
            "elite_size", "rounds", "seed", "best_fitness", "best_bitstring"
        ])

        # One summary row for this run.
        w.writerow([
            "GA",
            cfg.memory_depth,
            cfg.population_size,
            cfg.generations,
            cfg.crossover_rate,
            cfg.mutation_rate,
            cfg.elite_size,
            cfg.rounds,
            cfg.seed,
            best_fitness,
            best_bitstring
        ])


# Save per-generation fitness history to CSV.
def save_history(history, out_path: Path):
    # Ensure output directory exists before writing.
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # History columns.
        w.writerow(["generation", "best_fitness", "avg_fitness"])

        # Write one row per generation.
        for row in history:
            w.writerow([row["generation"], row["best_fitness"], row["avg_fitness"]])


# Main GA experiment flow.
def main():
    parser = argparse.ArgumentParser(description="Run GA for IPD lookup-table strategy.")
    parser.add_argument("--memory-depth", type=int, default=3, help="Lookup-table memory depth d (length = 4^d)")
    parser.add_argument("--population-size", type=int, default=80)
    parser.add_argument("--generations", type=int, default=200)
    parser.add_argument("--mutation-rate", type=float, default=0.001)
    parser.add_argument("--crossover-rate", type=float, default=0.8)
    parser.add_argument("--elite-size", type=int, default=2)
    parser.add_argument("--rounds", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-random-opponents", type=int, default=10)
    parser.add_argument("--suffix", type=str, default="", help="Optional suffix for output file names")
    args = parser.parse_args()

    # Configure GA hyperparameters.
    cfg = GAConfig(
        population_size=args.population_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        elite_size=args.elite_size,
        rounds=args.rounds,
        seed=args.seed,
        memory_depth=args.memory_depth,
    )

    # Build opponent pool (fixed seed for reproducibility).
    pool = get_opponent_pool(seed=cfg.seed, num_random=args.num_random_opponents, memory_depth=cfg.memory_depth)

    # Run optimization.
    best, best_fit, history = run_ga(pool, cfg)

    # Console summary.
    print("BEST FITNESS:", best_fit)
    print("BEST BITSTRING:", best)
    print("MEMORY DEPTH:", cfg.memory_depth)

    # Save outputs if GA returned a valid best solution.
    if best is not None:
        results_dir = Path("results") / "tables"
        suffix = f"_{args.suffix}" if args.suffix else ""
        save_best(best, best_fit, cfg, results_dir / f"ga_best{suffix}.csv")
        save_history(history, results_dir / f"ga_fitness_history{suffix}.csv")


# Script entry point.
if __name__ == "__main__":
    main()