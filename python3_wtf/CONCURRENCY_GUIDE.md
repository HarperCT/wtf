# Concurrency Guide: Understanding the Limits

## TL;DR

**AsyncRunner is memory-efficient but still needs limits to prevent subprocess explosion.**

## The Two Types of Resources

### 1. Memory (Coroutines) ✅ No Problem
```python
1 asyncio coroutine = ~1KB memory
1000 coroutines = ~1MB memory
```
**Asyncio handles this beautifully!**

### 2. Subprocesses ⚠️ Still a Concern
```python
1 plugin = 1 subprocess (ps, top, lsof, etc.)
50 plugins = 50 subprocesses running simultaneously
```
**This can overwhelm your system!**

## Why We Still Need Limits

Even though asyncio coroutines are lightweight, each plugin spawns a **real OS subprocess**:

```
Without Limit (50 plugins):
┌─────────────────────────────────────┐
│ AsyncRunner (1 thread)              │
│  ├─ 50 coroutines (~50KB) ✅        │
│  └─ Spawns:                         │
│      ├─ ps aux (subprocess)         │
│      ├─ top -b (subprocess)         │
│      ├─ lsof (subprocess)           │
│      ├─ dmesg (subprocess)          │
│      ├─ ... 46 more subprocesses    │
└─────────────────────────────────────┘
         ↓
    System Impact:
    - 50 processes competing for CPU
    - All reading /proc simultaneously
    - Context switching overhead
    - Potential resource locks
```

## Default Limits (Smart Auto-Scaling)

```python
runner = AsyncRunner(timeout=5.0, plugins=plugins)
# Auto-calculates: cpu_count × 3, max 32
```

| System | CPU Cores | Default Limit | Reasoning |
|--------|-----------|---------------|-----------|
| Weak | 2 | 6 | Conservative |
| Normal | 4 | 12 | Balanced |
| Good | 8 | 24 | Aggressive |
| Powerful | 16+ | 32 (capped) | Very aggressive |

## Custom Limits

### Conservative (Weak Systems)
```python
runner = AsyncRunner(timeout=5.0, plugins=plugins, max_concurrent=4)
```
**Use when:**
- Raspberry Pi or embedded systems
- Limited CPU (1-2 cores)
- Running alongside other services
- Plugins include heavy tools

### Balanced (Default)
```python
runner = AsyncRunner(timeout=5.0, plugins=plugins)
# Auto: cpu_count × 3
```
**Use when:**
- Normal desktop/server
- Mixed plugin workload
- Unsure about system capacity

### Aggressive (Powerful Systems)
```python
runner = AsyncRunner(timeout=5.0, plugins=plugins, max_concurrent=64)
```
**Use when:**
- High-end server (16+ cores)
- Plugins are mostly lightweight
- Need maximum speed
- System is dedicated to this task

### Unlimited (Use with Caution!)
```python
runner = AsyncRunner(timeout=5.0, plugins=plugins, max_concurrent=0)
# Spawns ALL plugins simultaneously
```
**⚠️ Warning:** This runs ALL plugins at once!

**Only use when:**
- All plugins are lightweight (`uname`, `hostname`, `uptime`)
- Powerful system (16+ cores)
- You've tested and monitored
- Plugins don't compete for resources

**Don't use when:**
- Plugins include `lsof`, `top`, `tcpdump`, `strace`
- Weak/embedded system
- Untested plugin combinations
- Production environment (without testing)

## Plugin Weight Classification

### Lightweight (Safe for High Concurrency)
```python
✅ uname, hostname, uptime
✅ df, free
✅ ip addr, ss (quick)
✅ dmesg (read-only)
```
**These can run 20-30+ simultaneously**

### Medium (Moderate Concurrency)
```python
⚠️ ps aux
⚠️ lscpu, lsmem
⚠️ lspci, lsusb
⚠️ netstat
```
**Limit to 10-20 simultaneously**

### Heavy (Low Concurrency)
```python
🔴 lsof (scans all file descriptors)
🔴 top -b (CPU intensive)
🔴 tcpdump, tshark (network capture)
🔴 strace (system call tracing)
🔴 iostat, vmstat (continuous monitoring)
```
**Limit to 4-8 simultaneously**

## Practical Examples

### Example 1: Mixed Workload (Recommended)
```python
plugins = [
    # 10 lightweight
    UnamePlugin(), HostnamePlugin(), UptimePlugin(),
    DfPlugin(), FreePlugin(), IpPlugin(),
    # 5 medium
    PsPlugin(), LscpuPlugin(), LsmemPlugin(),
    # 2 heavy
    LsofPlugin(), TopPlugin()
]

# Use default auto-scaling (safe for mixed workload)
runner = AsyncRunner(timeout=5.0, plugins=plugins)
# On 4-core: runs 12 at a time
```

### Example 2: All Lightweight (Can Be Aggressive)
```python
lightweight_plugins = [
    UnamePlugin(), HostnamePlugin(), UptimePlugin(),
    DfPlugin(), FreePlugin(), IpPlugin(),
    DmesgPlugin(), SsPlugin()
]

# Can use higher concurrency or even unlimited
runner = AsyncRunner(timeout=5.0, plugins=lightweight_plugins, max_concurrent=32)
# Or even: max_concurrent=0 for unlimited
```

### Example 3: Heavy Plugins (Be Conservative)
```python
heavy_plugins = [
    LsofPlugin(), TopPlugin(), TsharkPlugin(),
    TcpdumpPlugin(), StracePlugin()
]

# Use lower limit
runner = AsyncRunner(timeout=5.0, plugins=heavy_plugins, max_concurrent=4)
```

## Monitoring and Tuning

### How to Find Your Optimal Limit

1. **Start with default** (auto-scaling)
2. **Monitor system load** during execution
3. **Adjust based on results:**
   - System sluggish? → Decrease limit
   - CPU underutilized? → Increase limit
   - Plugins timing out? → Decrease limit
   - Fast completion? → Current limit is good

### Monitoring Commands
```bash
# Watch CPU usage during execution
htop

# Monitor process count
watch -n 1 'ps aux | wc -l'

# Check system load
uptime
```

## Summary

| Scenario | Recommended Limit | Reasoning |
|----------|------------------|-----------|
| Default (unknown) | Auto (cpu × 3) | Safe for most cases |
| Weak system | 4 | Prevent overload |
| Normal system | 12-24 | Balanced performance |
| Powerful system | 32-64 | Maximize throughput |
| All lightweight | 32 or unlimited | Safe to be aggressive |
| Any heavy plugins | 4-8 | Prevent resource contention |
| Production | Auto or tested | Don't guess in prod |

**Bottom Line:** The limit isn't about memory (asyncio handles that), it's about preventing too many subprocesses from overwhelming your CPU and I/O subsystems.
