# Experiment Playbook

This playbook gives copy-paste commands, expected outputs, and what each run is used for.

## Run from Project Root

All commands below assume current directory is the repository root.

## 1) Baseline Tournament

```powershell
python -m src.experiments.run_baselines
```

Optional heavier run:

```powershell
python -m src.experiments.run_baselines --runs 500 --seed-start 42 --rounds 300
```

Expected outputs (examples):
- `results/tables/baselines_tournament.csv`
- `results/tables/baselines_tournament_summary.csv`

Use when:
- You want reference performance before optimization.

## 2) Single GA Run

```powershell
python -m src.experiments.run_ga
```

Depth-specific examples:

```powershell
python -m src.experiments.run_ga --memory-depth 3 --generations 200 --population-size 80 --mutation-rate 0.001 --seed 42 --suffix d3
python -m src.experiments.run_ga --memory-depth 5 --generations 200 --population-size 80 --mutation-rate 0.001 --seed 42 --suffix d5
```

Expected outputs:
- `results/tables/ga_best*.csv`
- `results/tables/ga_fitness_history*.csv`

Use when:
- You want one optimized strategy and its convergence trace.

## 3) GA Mutation-Rate Sweep

```powershell
python -m src.experiments.run_ga_sweep
```

Expected outputs:
- `results/tables/ga_runs_summary.csv`
- `results/tables/ga_fitness_history_run1.csv`, `run2.csv`, `run3.csv`

Use when:
- You want to tune GA mutation rate.

## 4) GA Depth Sweep (3 vs 5)

```powershell
python -m src.experiments.run_ga_depth_sweep --depths 3,5 --seeds 42,43,44 --generations 200 --population-size 80 --mutation-rate 0.001 --tag d3_vs_d5
```

Expected outputs:
- `results/tables/ga_depth_sweep_runs_d3_vs_d5.csv`
- `results/tables/ga_depth_sweep_summary_d3_vs_d5.csv`
- `results/tables/ga_fitness_history_depth3_seed42_d3_vs_d5.csv` (and other seed/depth variants)

Use when:
- You need fair depth comparisons across seeds.

## 5) Hill Climb

```powershell
python -m src.experiments.run_hill_climb
```

Expected outputs:
- `results/tables/hill_best.csv`
- `results/tables/hill_history.csv`

Use when:
- You want a local-search baseline against GA.

## 6) Method Comparisons

```powershell
python -m src.experiments.run_comparisons
python -m src.experiments.compare_best
```

Expected outputs (common):
- `results/tables/comparison.csv`
- `results/tables/ga_best_vs_baselines.csv`

Use when:
- You want method-level ranking and matchup behavior.

## 7) ML Dataset Build

```powershell
python -m src.ml.build_dataset
```

Expected output:
- `results/tables/ml_dataset.csv`

Use when:
- You want feature/label data for ML experiments.

## Common Troubleshooting

- Import errors: ensure you run from repository root.
- Inconsistent comparisons: verify same rounds/population/settings except the variable under test.
- Missing summary files: rerun command with the same `--tag` and confirm process completes.
