import asyncio
from typing import Any, Coroutine

async def with_timeout(coro: Coroutine[Any, Any, Any], seconds: int):
    return await asyncio.wait_for(coro, timeout=seconds)
