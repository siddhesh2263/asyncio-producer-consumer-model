import asyncio
from random import random
from time import perf_counter

# We are not creating the actual `work` function, which would do API calls and all.

async def do_work(work_queue: asyncio.Queue, result_queue: asyncio.Queue):

    # This function is not responsible for stopping itself, the controller would do that.
    while True:
        task_data = await work_queue.get()
        
        task_id = task_data['task_id']
        number = task_data['number']

        start = perf_counter()
        await asyncio.sleep(random() * 2)   # Has to be a asycnio sleep, otherwise it will be blocking.
        result = number * number
        end = perf_counter()

        # The result_queue will be limited in size, so we have to wait until it has
        # space. And as it is asynchronous, some other task could be doing some other
        # work at the same time, or instead, since we have concurrency, not parallelism.
        await result_queue.put(
            {
                "task_id": task_id,
                "result": result,
                "time_secs": end - start
            }
        )

        work_queue.task_done()  # We need to tell the work queue we're done with this item.

