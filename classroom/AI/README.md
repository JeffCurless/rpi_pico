# AI — Genetic Algorithm Maze Solver

Educational skeleton for a Genetic Algorithm (GA) that solves a maze. Students implement the core GA functions; the maze definition and GA loop are provided.

## Files

### ga_test.py

Defines a 10×10 maze and the overall GA structure.

**Parameters:**

| Constant | Value | Description |
|---|---|---|
| `MAX_GENERATIONS` | 1000 | Maximum number of GA iterations |
| `MAX_POPULATION` | 100 | Number of candidate solutions per generation |
| `MUTATION_RATE` | 0.01 | Probability of a gene mutating |

**Functions for students to implement:**

| Function | Description |
|---|---|
| `createInitialPopulation()` | Generate the starting population of random paths |
| `fitness(individual)` | Score a candidate solution based on maze progress |
| `mutateSingle(individual)` | Apply a random mutation to one candidate |
| `selectParents(population)` | Choose two parents for reproduction |
| `reproduceAndMutate(p1, p2)` | Crossover and mutate to produce offspring |
| `determineSolution(population)` | Check whether a solution has been found |

## Running

Pure Python — no hardware or Pimoroni libraries required. Run on a desktop Python interpreter or in the Pico REPL:

```
python3 ga_test.py
```

## Parent

See [classroom/](../README.md) for other classroom projects.
