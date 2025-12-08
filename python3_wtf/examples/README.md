# Examples

This directory contains example scripts demonstrating various features of python3_wtf.

## compare_runners.py

Compares the performance of `ThreadRunner` vs `AsyncRunner` with real plugins.

### Usage

```bash
# Compare with 20 plugins (default)
python compare_runners.py

# Compare with 50 plugins
python compare_runners.py 50

# Compare with 10 plugins
python compare_runners.py 10
```

### What It Shows

- Execution time comparison
- Success rate for each runner
- Memory usage estimation
- Speedup factor

### Example Output

```
=== Comparing Runners with 20 Plugins ===

Testing with 20 plugin instances
Unique plugins: {'PsPlugin', 'DfPlugin', 'FreePlugin', 'UptimePlugin'}

--- Testing ThreadRunner ---
ThreadRunner completed in 3.45s
Success: 20/20

--- Testing AsyncRunner ---
AsyncRunner completed in 2.87s
Success: 20/20

--- Testing AsyncRunnerAdvanced ---
Progress: 5/20 (25.0%) - Completed: PsPlugin
Progress: 10/20 (50.0%) - Completed: DfPlugin
Progress: 15/20 (75.0%) - Completed: FreePlugin
Progress: 20/20 (100.0%) - Completed: UptimePlugin
AsyncRunnerAdvanced completed in 2.91s
Success: 20/20

=== Summary ===
ThreadRunner:        3.45s
AsyncRunner:         2.87s
AsyncRunnerAdvanced: 2.91s

AsyncRunner is 1.20x faster!

Estimated Memory Usage:
ThreadRunner:  ~160MB
AsyncRunner:   ~20KB
Memory saved:  ~8192x
```

## Requirements

- Python 3.7+
- python3_wtf installed
- Linux system with debugging tools (ps, df, free, etc.)
