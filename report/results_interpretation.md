# Results Interpretation Guide

This guide explains how to read the main result files and translate numbers into conclusions.

## 1) Baseline Files

### `baselines_tournament.csv`
- Raw tournament-level outcomes.
- Use this to inspect per-strategy totals and match-level behavior.

### `baselines_tournament_summary.csv`
- Aggregated baseline ranking.
- Use this as the non-optimized reference point.

## 2) GA Files

### `ga_best.csv` / `ga_best_*.csv`
- Best discovered bitstring and run configuration.
- Important columns: `best_fitness`, `best_bitstring`, GA settings.

### `ga_fitness_history.csv` / `ga_fitness_history_*.csv`
- Per-generation metrics:
  - `best_fitness`
  - `avg_fitness`
- Typical pattern:
  - fast early gains,
  - slower mid-stage improvement,
  - plateau with occasional spikes.

### `ga_runs_summary.csv`
- Mutation-rate sweep summary.
- Compare rows by `best_fitness` and `final_avg_fitness`.

## 3) Depth Sweep Files

### `ga_depth_sweep_runs_<tag>.csv`
- One row per `(depth, seed)` run.
- Use for variability analysis and fairness checks.

### `ga_depth_sweep_summary_<tag>.csv`
- Aggregated by depth.
- Key columns:
  - `mean_best_fitness_overall`
  - `mean_final_best_fitness`
  - `mean_final_avg_fitness`
  - convergence proxies (`mean_first_gen_reach_99pct_best`, `mean_last_improvement_generation`)

Interpretation:
- Higher mean fitness indicates better average performance.
- Lower “first reach 99%” indicates faster convergence.
- Compare both quality and stability across seeds.

## 4) Hill Climb Files

### `hill_best.csv`
- Best hill-climb solution and final score.

### `hill_history.csv`
- Iteration-level hill-climb progress.
- Watch for long flat regions (local optima behavior).

## 5) Cross-Method Comparison Files

### `comparison.csv`
- Method-level ranking (GA best vs hill best vs baselines).
- Use this for headline conclusions.

### `ga_best_vs_baselines.csv`
- Matchup-level behavior of GA best against each baseline.
- Useful for characterizing strategy style:
  - exploitative (dominates ALLC),
  - robust/cooperative (strong vs TFT-like),
  - vulnerable (loses to ALLD), etc.

## 6) Turning Results into Report Statements

Use this pattern:

1. State setup (rounds, seeds, key hyperparameters).
2. Report aggregate metric(s) from summary CSV.
3. Mention stability/variability across seeds.
4. Mention behavior evidence from matchup CSV.
5. Add limitation (e.g., depth comparison only valid for tested settings).

Example template:

- "Under fixed settings (population 80, 200 generations, mutation 0.001), depth 5 achieved a higher mean best fitness than depth 3 across seeds 42,43,44."
- "However, depth 5 converged later on average, suggesting a richer but harder search space."

## 7) Common Pitfalls

- Comparing runs with different rounds/population/generation values.
- Using a single seed to claim one depth is universally better.
- Interpreting one matchup as overall strategy quality.
- Ignoring convergence speed while focusing only on final best score.
