# Architecture Overview

This document explains how the codebase is organized and how data flows from strategy definitions to final experiment tables.

## 1) System Flow

```text
Strategies + Opponent Pool
        ↓
Game Engine (matches/tournaments)
        ↓
Fitness Evaluation
        ↓
Optimization (GA / Hill Climb)
        ↓
Experiment Runners
        ↓
CSV Outputs in results/tables
        ↓
Plots / Report / Interpretation
```

## 2) Core Modules

### `src/strategies/`
- `baselines.py`: fixed human-designed strategies (`ALLC`, `ALLD`, `RAND`, `TFT`, `TF2T`, `STFT`).
- `lookup_table.py`: parameterized lookup-table strategy. Memory depth `d` maps to chromosome length `4^d`.

### `src/game/`
- `payoff.py`: Prisoner’s Dilemma payoff function.
- `engine.py`: match/tournament simulation loops.
- `evaluate.py`: computes strategy fitness against an opponent pool.

### `src/optim/`
- `genetic_algorithm.py`: GA data model (`GAConfig`) and optimization loop (selection, crossover, mutation, elitism).
- `hill_climb.py`: local-search optimization by bit flips.

### `src/experiments/`
- `opponent_pool.py`: builds consistent test opponents (baselines + random lookup strategies).
- `run_baselines.py`: baseline-only tournament outputs.
- `run_ga.py`: single GA run (supports configurable memory depth).
- `run_ga_sweep.py`: GA hyperparameter sweep (mutation-rate focused).
- `run_ga_depth_sweep.py`: depth/seed sweep for depth 3 vs depth 5 style analysis.
- `run_hill_climb.py`: single hill-climb run.
- `run_comparisons.py` / `compare_best.py`: post-optimization comparisons.
- `plots.py`: chart generation helpers.

### `src/ml/`
- `build_dataset.py`: builds ML-ready dataset tables from evolved strategies/results.

## 3) Data Contracts

Most outputs are CSV files in `results/tables/`.

Key conventions:
- `*_history*.csv`: per-iteration/per-generation traces.
- `*_summary*.csv`: aggregated cross-run metrics.
- `*_best*.csv`: single best strategy metadata + bitstring.

## 4) Memory Depth Design

Lookup-table state size grows exponentially:

$$
\text{chromosome length} = 4^d
$$

Implications:
- `d=3` → 64 bits (faster, smaller search space).
- `d=5` → 1024 bits (richer policy space, harder optimization).

The project now supports running both depths using the same GA pipeline.

## 5) Reproducibility

Reproducibility is controlled by:
- GA seed (`--seed` or sweep seeds)
- Opponent pool seed (`--opponent-pool-seed` in depth sweep)
- Fixed run settings (population, generations, rounds)

To compare methods fairly, hold all settings constant except the variable under study.

## 6) Typical End-to-End Workflow

1. Run baselines.
2. Run GA / Hill.
3. Run sweeps (mutation or depth).
4. Generate comparisons.
5. Interpret CSVs + report conclusions.

See `report/experiment_playbook.md` for exact commands and expected output files.
