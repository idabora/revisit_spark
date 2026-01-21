## Apache Spark

![Alt text describing the image](../images/IMG_20260121_141445338~3.jpg.jpeg)


![Alt text describing the image](../images/IMG_20260121_141705119.jpg.jpeg)


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
