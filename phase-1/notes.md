## Apache Spark

![Alt text describing the image](../images/IMG_20260121_141445338~3.jpg.jpeg)


![Alt text describing the image](../images/IMG_20260121_141705119~2.jpg.jpeg)


### Why Spark exists (Problems with MapReduce)
   " Spark exists to overcome MapReduce's slowness, primarily because MapReduce constantly writes intermediate data to disk, creating heavy I/O 
    overhead, while Spark processes data in-memory, making it significantly faster (up to 100x) for iterative tasks like machine learning and 
    real-time analytics, while also offering simpler APIs and unified processing for batch, streaming, and graph data."

### Problems with MapReduce (Why Spark was needed)
- Disk I/O Bottleneck: MapReduce writes intermediate data to disk after every map and reduce step, causing significant delays.
    
- Slow for Iterative Tasks: Its disk-based approach makes it inefficient for algorithms that repeatedly process the same data, like machine 
    learning or graph processing.
    
- Batch-Focused: Primarily designed for large-scale batch processing, lacking native support for real-time or interactive analysis.
    
- Complex for Many Use Cases: Required more boilerplate code compared to Spark's richer APIs (SQL, Streaming, MLlib). 

### How Spark Solves These Problems
- In-Memory Processing: Spark keeps data in RAM (memory) across multiple operations, drastically reducing disk I/O.
    
- Directed Acyclic Graph (DAG) Execution: It creates a DAG, optimizing the flow of operations and performing efficient multi-stage computations.
    
- Unified Engine: Offers built-in libraries (Spark SQL, Spark Streaming, MLlib, GraphX) for diverse tasks (SQL, streaming, ML, graph analytics) within one framework.
    
- Faster Performance: Achieves much faster speeds, especially for iterative and interactive workloads, making near real-time insights possible. 

### Q. where does the intermediate results being stored in spark?

In Spark, **intermediate results do not have a single storage location**. Where they live depends on *what kind* of intermediate data you are dealing with and *how Spark is configured*.

---

## 1. Default case: In Memory (RAM)

By design, Spark stores intermediate results **in executor memory**.

These include:
- Cached / persisted RDDs and DataFrames
- Intermediate stage outputs reused by downstream stages
- Shuffle buffers (before spilling)

Key points:
- Stored in **executor JVM heap and off-heap memory**
- Managed by Spark’s **unified memory manager**
- Automatically evicted when memory pressure increases

If it fits in memory → **no disk I/O**.

---

## 2. When memory is insufficient: Spill to Local Disk

Spark spills data to disk when memory is not enough.

Spill happens for:
- Shuffles
- Sorts
- Aggregations
- Joins

Where it spills:
- **Local disk on executor nodes**
- Configured via `spark.local.dir` (default often `/tmp`)

Important:
- This is **not HDFS or S3**
- Data is **temporary**
- Deleted after the job or executor exits

---

## 3. Shuffle Data (Special Case)

Shuffle data is **always written to local disk** at some point.

Why:
- Shuffles can be very large
- Executors need to fetch data from other executors
- Data must survive task retries

Process:
- Map task output → local disk
- Reduce task fetches data over the network

This is unavoidable in distributed systems.

---

## 4. Persisted / Cached Data (Explicit Storage Levels)

If you explicitly persist data:

```python
df.persist(StorageLevel.MEMORY_ONLY)
```

#### Q. First: What is “Distributed Computing”?
"Doing one computation by splitting the work across multiple machines (or CPUs) at the same time, instead of using only one machine."

So instead of:
- 1 computer
- 1 CPU / limited memory
- Processing everything sequentially

We use:
- Many machines (nodes)
- Many CPUs + combined memory
- Processing in parallel

**Think of it as teamwork for computers.**

## Why Normal (Single-Machine) Computing Breaks Down

Let’s start with a real problem.
Example:
- You have:
    500 GB of log data
    A normal laptop has:
    8–16 GB RAM
    1 CPU (or a few cores)

- What happens?

    ❌ Problem 1: Memory Limit
        You cannot load 500 GB into RAM
        Disk-based processing becomes extremely slow

    ❌ Problem 2: Time
        Even if you process line by line:
        One CPU
        Sequential execution
        It may take hours or days

    ❌ Problem 3: CPU Bottleneck
        Only one machine is doing all the work
        Other CPUs in the world are idle

👉 Conclusion: Single-machine computing does not scale.

## Distributed Computing Solves This

- Now imagine: 10 machines
- Each machine has:
    16 GB RAM
    4 CPU cores
- Combined Power:
    160 GB RAM
    40 CPU cores
Instead of:
    One machine processes 500 GB
We do:
    Each machine processes 50 GB
    
🔥 Same logic, but 10× faster and possible to run

This is distributed computing.

# Spark driver — entry point, planning, and execution (concise reference)

This note explains the role of the Spark driver, how it fits with SparkSession / SparkContext, and the execution lifecycle of a Spark job. It is written to improve readability and quick understanding.

---

## SparkSession vs SparkContext

- SparkSession
  - The unified entry point for Spark functionality (introduced in Spark 2.x).
  - Provides a single object to interact with Spark SQL, DataFrame, Dataset, and streaming APIs.
  - Internally manages a SparkContext and other contexts (SQLContext, HiveContext).

- SparkContext
  - The original low-level entry point (pre-Spark 2.0).
  - Represents the connection to a Spark cluster, manages resources and coordinates task execution.
  - Still accessible via `spark.sparkContext` when you create a SparkSession.

---

## How the driver is launched

When you run:
```bash
spark-submit python job.py
```
Spark launches a JVM process that runs the Driver. The driver:
- Runs your `main()` program.
- Creates the `SparkSession` / `SparkContext`.
- Registers the application with the cluster manager (YARN, Kubernetes, Standalone).
- Builds the logical plan for transformations (lazy evaluation).

---

## Example (Python)
```python
df = spark.read.csv("s3://data")
df2 = df.filter("price > 100").groupBy("category").count()

# action
df2.show()
```

---

## Driver responsibilities — execution lifecycle

1. Logical plan creation (lazy)
   - Transformations build a logical DAG (no execution yet).

2. Action triggers execution (driver wakes up)
   - Example: `df2.show()` or `df.collect()`.

3. Planning phase (all in driver)
   - Logical Plan → Optimized Logical Plan
     - Catalyst optimizer applies rules (pushdown filters, project pruning, etc.).
   - Optimized Plan → Physical Plan
     - Planner decides physical operators (join types, scans, etc.).
   - Physical Plan → Stages
     - Split the physical plan at shuffle boundaries into stages.

4. Scheduling
   - DAG Scheduler (in driver)
     - Breaks job into stages.
     - Determines dependencies and which stages can run in parallel.
     - Example stages:
       - Stage 0: Read CSV + filter
       - Stage 1: Shuffle + aggregation

5. Task creation & distribution
   - For each stage the driver:
     - Splits work into tasks (usually 1 task per partition).
     - Submits serialized tasks to executors via the cluster manager.
     - Tracks task status, failures, retries (TaskScheduler functionality).

6. Communication with executors
   - Driver sends serialized tasks.
   - Executors run tasks and return:
     - Task completion events
     - Metrics
     - Shuffle metadata
     - Failure reports

7. Result collection
   - When you call `df.collect()`:
     - Executors send partition results back to the driver.
     - The driver pulls, deserializes, and holds results in its memory.
   - Warning: `collect()` can OOM the driver if the result set is large.

---

## Executors — what they do
- Executors are worker processes that run tasks.
- They are mostly “dumb” workers: run the task given, manage task-local memory and storage, and report results and metrics to the driver.
- Shuffle services and block managers on executors coordinate shuffle and cached data.

---

## Important tips & best practices
- Avoid `collect()` on large datasets. Use `show(n)` or `take(n)` for previews.
- Tune driver memory (e.g., `--driver-memory`) if you need to collect larger results.
- Persist/cache intermediate datasets (`df.persist()`) to avoid recomputation.
- Tune number of partitions to balance parallelism and task overhead.
- Use broadcast joins for small dimension tables to avoid expensive shuffles.
- Monitor driver logs and the Spark UI to understand stages, tasks, and bottlenecks.

---

## Quick checklist when debugging driver issues
- Is the action causing a lot of data to be pulled to driver? (look for `collect`, `toLocalIterator`, `show` on full dataset)
- Are there many small partitions or too few large partitions?
- Are there repeated re-computations caused by missing persistence?
- Do driver logs show OOM, long GC pauses, or scheduling delays?
- Inspect Spark UI: DAG visualization, stage breakdowns, task metrics.

---

## Key takeaways
- SparkSession is the modern unified API — it creates/owns the SparkContext (cluster connection).
- The driver builds and optimizes the query plan, then schedules stages and tasks.
- Executors execute tasks; the driver orchestrates and collects results — be careful with operations that pull large results into the driver.

```