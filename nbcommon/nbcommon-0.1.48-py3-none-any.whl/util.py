import asyncio

"""
table_split helps calculating  a large horizontal * vertical using multiple batches currently with func(horizontal, vertical) => List[List[result]]
verticle: list/slice length of m
horizontal: list/slice length of n
func: awaitable
result: 2d array of dimention m*n
"""


async def table_split(vertical, horizontal, func, unit=100, return_exceptions=False):
    async def executor(vi, hi):
        is_crt = asyncio.iscoroutinefunction(func)
        r = None
        if is_crt:
            r = await func(vertical[vi:vi + unit], horizontal[hi:hi + unit])
        else:
            r = func(vertical[vi:vi + unit], horizontal[hi:hi + unit])

        for i in range(0, len(r)):
            for j in range(0, len(r[i])):
                result[vi + i][hi + j] = r[i][j]
    result = [[None for j in range(0, len(horizontal))] for i in range(0, len(vertical))]
    vi = 0
    execs = []
    while vi < len(vertical):
        hi = 0
        while hi < len(horizontal):
            execs.append(executor(vi, hi))
            hi += unit
        vi += unit
    await asyncio.gather(*execs, return_exceptions=return_exceptions)
    return result
