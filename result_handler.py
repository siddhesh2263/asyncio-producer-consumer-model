import asyncio
from typing import Callable

# The function needs to know what's its going to callback. the task_callback function
# we defined in main, pass it to this async function here, because it needs to know what
# to callback.
# callback -> it takes in a dictionary, and returns None.
async def handle_task_result(result_queue: asyncio.Queue, callback: Callable[[dict], None]):
    
    # It will run indefinetly:
    while True:
        result = await result_queue.get()
        callback(result)
        result_queue.task_done()