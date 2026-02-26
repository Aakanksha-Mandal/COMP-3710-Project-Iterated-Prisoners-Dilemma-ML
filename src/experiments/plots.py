import os
import pandas as pd
import matplotlib.pyplot as plt


BASELINE_PATH = "results/tables/baselines_tournament_summary.csv"
COMPARISON_PATH = "results/tables/comparison.csv"
GA_HISTORY_PATH = "results/tables/ga_fitness_history.csv"

FIG_DIR = "results/figures"


def ensure_fig_dir():
    os.makedirs(FIG_DIR, exist_ok=True)


# --------------------------------------------------
# 1️⃣ Baseline Bar Plot
# --------------------------------------------------
def plot_baselines():
    df = pd.read_csv(BASELINE_PATH)

    # Your baseline CSV uses column names:
    # strategy, mean_score, std_score
    df = df.sort_values("mean_score", ascending=False)

    plt.figure(figsize=(8, 5))
    plt.bar(df["strategy"], df["mean_score"])
    plt.title("Baseline Strategy Performance")
    plt.xlabel("Strategy")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "baselines_bar.png")
    plt.savefig(out_path)
    plt.close()

    print(f"Saved {out_path}")


# --------------------------------------------------
# 2️⃣ Comparison Bar Plot (GA vs Hill vs Baselines)
# --------------------------------------------------
def plot_comparison():
    df = pd.read_csv(COMPARISON_PATH)

    df = df.sort_values("avg_score", ascending=False)

    plt.figure(figsize=(9, 5))
    plt.bar(df["name"], df["avg_score"])
    plt.title("GA vs Hill vs Baselines")
    plt.xlabel("Strategy")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "comparison_bar.png")
    plt.savefig(out_path)
    plt.close()

    print(f"Saved {out_path}")


# --------------------------------------------------
# 3️⃣ GA Fitness Curve
# --------------------------------------------------
def plot_ga_fitness():
    df = pd.read_csv(GA_HISTORY_PATH)

    # Typical columns in GA history:
    # generation, best_fitness, avg_fitness
    if "generation" not in df.columns:
        print("GA history missing 'generation' column.")
        return

    plt.figure(figsize=(8, 5))

    if "best_fitness" in df.columns:
        plt.plot(df["generation"], df["best_fitness"], label="Best Fitness")

    if "avg_fitness" in df.columns:
        plt.plot(df["generation"], df["avg_fitness"], label="Average Fitness")

    plt.title("GA Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "ga_fitness_curve.png")
    plt.savefig(out_path)
    plt.close()

    print(f"Saved {out_path}")


def main():
    ensure_fig_dir()
    plot_baselines()
    plot_comparison()
    plot_ga_fitness()


if __name__ == "__main__":
    main()