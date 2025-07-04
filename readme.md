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

In the project, we will include function signatures such as `function`, `params`, `callback: task complete`, `callback: job complete`. `callback: task complete` is invoked by the asynchronous operation after receiving and processing the API result (for example.) `callback: job complete` is invoked once all work has finished.

Additionally, instead of having each worker call the `callback: task complete` function directly, workers push the results to a result queue. A dedicated result handler consumes this queue and triggers `callback: task complete`. This design prevents workers from blocking if `callback: task complete` is time-consuming.

![alt text](https://github.com/siddhesh2263/asyncio-producer-consumer-model/blob/main/assets/system-1.png?raw=true)

![alt text](https://github.com/siddhesh2263/asyncio-producer-consumer-model/blob/main/assets/system-2.png?raw=true)

---

tradeoff between memory, wait time, 

main, producer, consimer, result_handler, controller(_controller last), call main in main.py again.