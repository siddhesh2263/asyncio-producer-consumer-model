# Producer-Consumer model using Python (with AsyncIO)

## Overview

The producer-consumer model is a technique used to perform multiple tasks asynchronously. In this setup, we repeatedly perfom the same type of work, but with different inputs.

For example, making calls to an API endpoint to check car prices is a use case for `asyncio`, and suits our case when we need to run concurrent tasks that are I/O bound. While one request is waiting for the API to complete its I/O operation, we can dispatch another request or process the response we just received.

Launching too many tasks at once can overwhelm the `asyncio` event loop. Do we want to run 1000 tasks simultaneously? Probably not - we will limit concurrent to about 50 tasks for this project.

When we have more work than active async workers, the producer-consumer model helps manage the load effectively. A producer (or multiple producers) submits work items to a queue. One or more workers - say, 50 - watch the queue, and and whenever a work item is available, a worker grabs it and performs the task. Once all producers finish creating work items and the queue is empty, all work is complete.

So in practice, we define:
* Producer tasks that create work items,
* A shared work queue that holds those items,
* Worker taks that process items from the queue.

![alt text](https://github.com/siddhesh2263/asyncio-producer-consumer-model/blob/main/assets/system-1.png?raw=true)

<br>

In the project, we will include function signatures such as `function`, `params`, `callback: task complete`, `callback: job complete`. `callback: task complete` is invoked by the asynchronous operation after receiving and processing the API result (for example.) `callback: job complete` is invoked once all work has finished.

Additionally, instead of having each worker call the `callback: task complete` function directly, workers push the results to a result queue. A dedicated result handler consumes this queue and triggers `callback: task complete`. This design prevents workers from blocking if `callback: task complete` is time-consuming.

Additionally, instead of having each worker call the `callback: task complete` function directly, workers push the results to a result queue. A dedicated result handler consumes this queue and triggers `callback: task complete`. This design prevents workers from blocking if `callback: task complete` is time-consuming.

![alt text](https://github.com/siddhesh2263/asyncio-producer-consumer-model/blob/main/assets/system-2.png?raw=true)

<br>

## Results

In this run, each task had an individual processing time ranging from approximately 0.52 to 1.70 seconds, and if executed sequentially, the total time would have been around 10.76 seconds. However, with the asynchronous producer-consumer model and multiple workers running concurrently, the entire job completed in 2.70 seconds. This shows a clear performance gain—roughly a 4× speedup — due to concurrency, where multiple tasks were handled in overlapping time windows instead of waiting for each to finish before starting the next.

![alt text](https://github.com/siddhesh2263/asyncio-producer-consumer-model/blob/main/assets/terminal-op.png?raw=true)

<br>

## Tradeoff between memory and wait times

In the producer-consumer model, the key trade-off between memory and wait time lies in the size of the shared queue. A larger queue allows producers to quickly offload tasks without waiting, which reduces producer wait time and supports high throughput under bursty workloads. However, this comes at the cost of increased memory usage, as more tasks are held in memory before consumers process them. If consumers fall behind, the queue can grow significantly, potentially leading to high RAM consumption or out-of-memory errors.

On the other hand, a smaller queue constrains memory usage by limiting how many tasks can be buffered. But once the queue reaches capacity, producers are forced to wait, introducing backpressure into the system. This can throttle input and increase overall task latency, especially if consumer throughput is not high enough. Choosing the right queue size involves balancing system responsiveness, memory limits, and how much delay or throttling we're willing to tolerate under load.



<!-- main, producer, consimer, result_handler, controller(_controller last), call main in main.py again. -->