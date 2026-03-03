# Optimization Methods

To discover high-performing strategies for the Iterated Prisoner’s Dilemma (IPD), we implemented and compared two optimization methods: a Genetic Algorithm (GA) and Hill Climbing.

## Strategy Representation

Strategies are lookup-table policies with configurable memory depth $d$. Each state is a sequence of the previous outcomes (CC, CD, DC, DD), so the chromosome length is:

$$
4^d
$$

- For memory depth 3, this is 64 bits.
- For memory depth 5, this is 1024 bits.

Each bit maps to an action in that state: cooperate (0) or defect (1).

## Fitness Evaluation

Fitness is the average score of a strategy against a fixed opponent pool, with 200 rounds per match.

Opponent pool includes:
- Baselines: ALLC, ALLD, RAND, TFT, TF2T, STFT
- Random lookup-table opponents

## Genetic Algorithm (GA)

GA uses selection, crossover, mutation, and elitism.

Core settings used in the main sweep (`ga_runs_summary.csv`):
- Population size: 80
- Generations: 200
- Crossover rate: 0.8
- Elite size: 2
- Mutation rates tested: 0.0005, 0.001, 0.005

### GA Results Summary (current)

From `results/tables/ga_runs_summary.csv`:
- Best run: mutation rate **0.001** with best fitness **708.8125**
- Other runs:
	- 0.0005 → 672.75
	- 0.005 → 705.1875

This indicates moderate mutation gave the strongest overall result in this setup.

## Hill Climbing

Hill Climbing starts from a random strategy and flips one bit at a time, accepting improving moves.

Current run (`results/tables/hill_best.csv`):
- Iterations: 5000
- Best fitness: **573.5**

## Comparison and Behavior

From `results/tables/comparison.csv`:
- GA_BEST average score: **699.375**
- HILL_BEST average score: **567.75**

So GA outperforms Hill Climbing on this benchmark.

From `results/tables/ga_best_vs_baselines.csv`, GA_BEST is highly exploitative:
- Very strong vs ALLC (+980 total)
- Positive vs TF2T and RAND
- Ties with TFT and STFT
- Slightly loses to ALLD (-20)

This pattern suggests the evolved policy is not purely cooperative; it is closer to opportunistic/defection-heavy behavior.

## Convergence Trend (GA)

Using `ga_fitness_history_run2.csv` (the best GA configuration):
- Rapid gains in early generations
- Improvements slow and mostly plateau after roughly generation 60
- Occasional late spikes, with best observed at generation 123

## Memory Depth 3 vs 5 Status

Depth comparison tooling is now implemented (`run_ga_depth_sweep.py`), but a full multi-seed depth conclusion has not yet been finalized in this report.

To run a fair depth comparison:

```powershell
python -m src.experiments.run_ga_depth_sweep --depths 3,5 --seeds 42,43,44 --generations 200 --population-size 80 --mutation-rate 0.001 --tag d3_vs_d5
```

Then compare:
- `results/tables/ga_depth_sweep_runs_d3_vs_d5.csv`
- `results/tables/ga_depth_sweep_summary_d3_vs_d5.csv`

## Conclusion

Current evidence shows evolutionary optimization is effective for IPD lookup-table strategy discovery, with GA substantially outperforming Hill Climbing under the tested settings. The depth-3 vs depth-5 performance question is now experimentally supported by tooling and should be concluded after full sweep outputs are generated and analyzed.