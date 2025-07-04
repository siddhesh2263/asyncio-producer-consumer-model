import asyncio
from time import perf_counter
from typing import Callable, List

import consumer, producer, result_handler

# We will set some configuration parameters to state how many workers we have,
# how many result handlers, size of the queues. Instead of hardcoding, can tweak
# them from here.

NUM_WORKERS = 50
WORK_QUEUE_MAX_SIZE = 200

# If the workers aren't keepin up, the queue can get filled up, and producers will
# wait to put items into the queue.

NUM_RESULT_HANDLERS = 50
RESULT_QUEUE_MAX_SIZE = 200

# We will write our controller, which will be an async function.
# _ means it is private to this module, or pseudo private according to convention.
async def _controller(batch: List[dict], task_completed_callback: Callable, job_completed_callback: Callable) -> None:
    start = perf_counter()
    
    work_queue = asyncio.Queue(maxsize=WORK_QUEUE_MAX_SIZE)
    result_queue = asyncio.Queue(maxsize=RESULT_QUEUE_MAX_SIZE)

    tasks = []

    producer_completed = asyncio.Event()
    producer_completed.clear()  # set it to False when we start off.
    tasks.append(
        asyncio.create_task(producer.produce_work(batch, work_queue, producer_completed))
    )

    for _ in range(NUM_WORKERS):
        tasks.append(
            asyncio.create_task(consumer.do_work(work_queue, result_queue))
        )
    
    for _ in range(NUM_RESULT_HANDLERS):
        tasks.append(
            asyncio.create_task(result_handler.handle_task_result(result_queue, task_completed_callback))
        )
    
    # Now, we need to wait for things to happen:
    await producer_completed.wait() # Wait for the producer completed event to finish.
    await work_queue.join() # We need to wait and ensure that the work queue is empty, and done
    await result_queue.join()# We need to await and ensure the job is done.

    # Now since job is done, we need to cancel them:
    for task in tasks:
        task.cancel()
    
    end = perf_counter()
    job_completed_callback({"elapsed_sec": end - start})

# This doesn't have to be async. It will do something to kick off the async process.
def run_job(batch: List[dict], task_completed_callback: Callable, job_completed_callback: Callable) -> None:
    # We need asyncio to run the async function:
    asyncio.run(_controller(batch, task_completed_callback, job_completed_callback))
    # All this is required to kick off the asynchronous process.