import os
import pandas as pd

from src.experiments.opponent_pool import get_opponent_pool
from src.game.evaluate import evaluate_strategy
from src.strategies.lookup_table import LookupTableStrategy
from src.strategies.baselines import ALLC, ALLD, RAND, TFT, TF2T, STFT


SEED = 42
ROUNDS = 200
NUM_RANDOM = 10

GA_BEST_PATH = "results/tables/ga_best.csv"
HILL_BEST_PATH = "results/tables/hill_best.csv"
OUT_PATH = "results/tables/comparison.csv"


def load_best_bitstring(path: str) -> str:
    df = pd.read_csv(path)
    if "best_bitstring" not in df.columns:
        raise ValueError(f"{path} missing 'best_bitstring'. Found columns: {list(df.columns)}")
    return str(df.iloc[0]["best_bitstring"]).strip()


def main():
    # 1) Fixed opponent pool (single source of truth)
    opponents = get_opponent_pool(seed=SEED, num_random=NUM_RANDOM)

    # 2) Load best strategies from GA + Hill outputs
    ga_bits = load_best_bitstring(GA_BEST_PATH)
    hill_bits = load_best_bitstring(HILL_BEST_PATH)

    ga_best = LookupTableStrategy(ga_bits, name="GA_BEST")
    hill_best = LookupTableStrategy(hill_bits, name="HILL_BEST")

    # 3) Baseline strategies for comparison
    baselines = [
        TFT("TFT"),
        TF2T("TF2T"),
        STFT("STFT"),
        ALLD("ALLD"),
        ALLC("ALLC"),
        RAND("RAND"),
    ]

    candidates = [
        ("GA_BEST", "ga", ga_best),
        ("HILL_BEST", "hill", hill_best),
        *[(b.name, "baseline", b) for b in baselines],
    ]

    # 4) Evaluate (same evaluator used by GA fitness)
    rows = []
    for name, source, strat in candidates:
        avg_score = evaluate_strategy(strat, opponents, rounds=ROUNDS)
        rows.append({
            "name": name,
            "source": source,
            "rounds": ROUNDS,
            "seed": SEED,
            "num_random_opponents": NUM_RANDOM,
            "avg_score": avg_score,
        })

    # 5) Save CSV
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out_df = pd.DataFrame(rows).sort_values("avg_score", ascending=False)
    out_df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print(out_df)


if __name__ == "__main__":
    main()
