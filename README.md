# Iterated Prisoner’s Dilemma — Optimization & ML

This project simulates the Iterated Prisoner’s Dilemma (IPD) and applies optimization methods (Genetic Algorithm, Hill Climb) to evolve strong strategies. It also includes baseline tournaments, comparison scripts, plotting helpers, and dataset generation.

---

## ✅ What’s Included

### Strategies
- Baselines: `ALLC`, `ALLD`, `RAND`, `TFT`, `TF2T`, `STFT`
- Lookup-table strategies with configurable memory depth (`4^depth` chromosome length)

### Optimization
- Genetic Algorithm: `src/optim/genetic_algorithm.py`
- Hill Climb: `src/optim/hill_climb.py`
- Parameter sweep scripts for GA and depth comparisons

### Evaluation & Analysis
- Match/tournament engine and payoff logic
- GA-vs-baseline and GA-vs-Hill comparisons
- Plot helpers and ML dataset builder

### Outputs
- CSV results in `results/tables/`
- Plot output folder in `results/figures/`

---

## ▶️ How to Run

Run from project root:

```powershell
python -m src.experiments.run_baselines
python -m src.experiments.run_ga
python -m src.experiments.run_hill_climb
python -m src.experiments.run_ga_sweep
python -m src.experiments.compare_best
```

Optional baselines run settings:

```powershell
python -m src.experiments.run_baselines --runs 500 --seed-start 42 --rounds 300
```

---

## 🧠 Testing Different Memory Depths

Single-run depth test:

```powershell
# Depth 3
python -m src.experiments.run_ga --memory-depth 3 --generations 200 --population-size 80 --mutation-rate 0.001 --seed 42 --suffix d3

# Depth 5
python -m src.experiments.run_ga --memory-depth 5 --generations 200 --population-size 80 --mutation-rate 0.001 --seed 42 --suffix d5
```

Depth sweep (recommended for fair comparison):

```powershell
python -m src.experiments.run_ga_depth_sweep --depths 3,5 --seeds 42,43,44 --generations 200 --population-size 80 --mutation-rate 0.001 --tag d3_vs_d5
```

This produces:
- `results/tables/ga_depth_sweep_runs_<tag>.csv`
- `results/tables/ga_depth_sweep_summary_<tag>.csv`
- Per-run histories: `ga_fitness_history_depth<d>_seed<s>_<tag>.csv`

---

## 📁 Folder Structure

```text
.
├── .gitignore
├── README.md
├── baselines_standard.csv
├── baselines_standard_run0.csv
├── baselines_stress_test.csv
├── report/
│   └── optimization.md
├── results/
│   ├── figures/
│   │   └── .gitkeep
│   └── tables/
│       ├── baselines_tournament.csv
│       ├── baselines_tournament_summary.csv
│       ├── comparison.csv
│       ├── ga_best.csv
│       ├── ga_best_d3.csv
│       ├── ga_best_d5.csv
│       ├── ga_best_smoke_d3.csv
│       ├── ga_best_smoke_d5.csv
│       ├── ga_best_vs_baselines.csv
│       ├── ga_depth_sweep_runs_d3_vs_d5.csv
│       ├── ga_depth_sweep_runs_smoke.csv
│       ├── ga_depth_sweep_summary_smoke.csv
│       ├── ga_fitness_history.csv
│       ├── ga_fitness_history_d3.csv
│       ├── ga_fitness_history_d5.csv
│       ├── ga_fitness_history_depth3_seed42_smoke.csv
│       ├── ga_fitness_history_depth5_seed42_smoke.csv
│       ├── ga_fitness_history_run1.csv
│       ├── ga_fitness_history_run2.csv
│       ├── ga_fitness_history_run3.csv
│       ├── ga_fitness_history_smoke_d3.csv
│       ├── ga_fitness_history_smoke_d5.csv
│       ├── ga_runs_summary.csv
│       ├── hill_best.csv
│       ├── hill_history.csv
│       └── ml_dataset.csv
└── src/
    ├── experiments/
    │   ├── compare_best.py
    │   ├── opponent_pool.py
    │   ├── plots.py
    │   ├── run_baselines.py
    │   ├── run_comparisons.py
    │   ├── run_ga.py
    │   ├── run_ga_depth_sweep.py
    │   ├── run_ga_sweep.py
    │   └── run_hill_climb.py
    ├── game/
    │   ├── engine.py
    │   ├── evaluate.py
    │   └── payoff.py
    ├── ml/
    │   └── build_dataset.py
    ├── optim/
    │   ├── genetic_algorithm.py
    │   └── hill_climb.py
    └── strategies/
        ├── baselines.py
        └── lookup_table.py
```

---

## 🧪 Results

Generated experiment outputs are stored in:

```text
results/tables/
```

Common files:
- Baselines: `baselines_tournament.csv`, `baselines_tournament_summary.csv`
- GA: `ga_best.csv`, `ga_fitness_history.csv`, `ga_runs_summary.csv`
- Comparisons: `comparison.csv`, `ga_best_vs_baselines.csv`
- Hill Climb: `hill_best.csv`, `hill_history.csv`
- Depth sweep: `ga_depth_sweep_runs_*.csv`, `ga_depth_sweep_summary_*.csv`

---

## 📌 Notes

- Always run from the **project root** so `src.*` imports resolve.
- GA and Hill Climb are stochastic; set seeds for reproducibility.
- Keep GA settings fixed when comparing memory depths (change only depth + seed).
- For GA-best comparisons vs baselines, use the scripts in `src/experiments/` (e.g., `compare_best.py`, `run_comparisons.py`).

---

## 📄 Report

See: `report/optimization.md`

---

