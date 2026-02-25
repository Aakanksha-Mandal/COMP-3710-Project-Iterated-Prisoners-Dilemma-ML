# Iterated Prisoner’s Dilemma + Genetic Algorithm (Python)

A Python project for simulating the **Iterated Prisoner’s Dilemma (IPD)**, evaluating baseline strategies, and evolving lookup-table strategies with a **Genetic Algorithm (GA)**.

---

## Project Goals

- Simulate repeated Prisoner’s Dilemma matches.
- Compare classic baseline strategies (ALLC, ALLD, TFT, etc.).
- Evolve stronger 64-bit lookup-table strategies with GA.
- Provide reusable modules for experiments and ML dataset generation.

---

## Folder Structure

```text
src/
  experiments/
    opponent_pool.py       # Builds baseline + random opponent sets
    run_baselines.py       # Runs baseline-vs-baseline evaluations
    run_ga.py              # Runs GA optimization experiment
  game/
    engine.py              # Match loop and action progression
    evaluate.py            # Fitness/evaluation helpers
    payoff.py              # PD payoff definitions
  ml/
    build_dataset.py       # Dataset generation pipeline
  optim/
    genetic_algorithm.py   # GA operators + training loop
  strategies/
    baselines.py           # Fixed strategy implementations
    lookup_table.py        # 64-bit lookup-table strategy class
```

---

## Requirements

- Python 3.10+ (recommended)
- No external dependencies required unless added later

---

## Run Instructions (Windows / PowerShell)

From repository root:

```powershell
cd C:\Users\user\Downloads\VS\Iterated-Prisoners-Dilemma-ML
```

### 1) Run baseline experiment

```powershell
python -m src.experiments.run_baselines
```

### 2) Run GA experiment

```powershell
python -m src.experiments.run_ga
```

Expected GA outputs include:
- best fitness
- best bitstring/chromosome
- generation progress (if enabled in `genetic_algorithm.py`)

---

## Core Components

### Strategies
- **Baselines**: deterministic and simple adaptive policies (ALLC, ALLD, RAND, TFT, TF2T, STFT).
- **LookupTableStrategy**: uses a 64-bit chromosome to map history states to actions.

### Game Engine
- `engine.py` plays repeated rounds between two strategies.
- `payoff.py` defines reward mapping for (C/D) outcomes.

### Evaluation
- `evaluate.py` computes a strategy’s average score against an opponent pool.

### Optimization
- `genetic_algorithm.py`:
  - initializes random chromosomes
  - evaluates fitness
  - selects parents (tournament)
  - performs crossover + mutation
  - keeps elites
  - returns best strategy and training history

---

## Typical Workflow

1. Build an opponent pool in `experiments/opponent_pool.py`.
2. Run baseline benchmark (`run_baselines.py`) for reference.
3. Run GA (`run_ga.py`) to evolve a stronger lookup-table strategy.
4. Compare GA best fitness against baseline averages.

---

## Common Issues

### `Import "src...." could not be resolved`
- Run scripts from the repository root using `python -m ...`.
- Ensure VS Code opens the project root folder (not a subfolder).

### No output when running a file
- Confirm the file contains:
  ```python
  if __name__ == "__main__":
      main()
  ```

### GA very slow
- Reduce:
  - `population_size`
  - `generations`
  - `rounds`

---

## Suggested Next Improvements

- Save GA `history` to CSV for plotting.
- Add matplotlib learning curve visualization.
- Add unit tests for:
  - payoff correctness
  - engine round accounting
  - mutation/crossover behavior
- Add CLI arguments for experiment configs.

---

