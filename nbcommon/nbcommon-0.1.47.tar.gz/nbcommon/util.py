import asyncio

"""
table_split helps calculating  a large horizontal * vertical using multiple batches currently with func(horizontal, vertical) => List[List[result]]
verticle: list/slice length of m
horizontal: list/slice length of n
func: awaitable
result: 2d array of dimention m*n
"""
_unit = 100


async def table_split(vertical, horizontal, func):
    async def executor(vi, hi):
        is_crt = asyncio.iscoroutinefunction(func)
        r = None
        if is_crt:
            r = await func(vertical[vi:vi + _unit], horizontal[hi:hi + _unit])
        else:
            r = func(vertical[vi:vi + _unit], horizontal[hi:hi + _unit])

        for i in range(0, len(r)):
            for j in range(0, len(r[i])):
                result[vi + i][hi + j] = r[i][j]
    result = [[None for j in range(0, len(horizontal))] for i in range(0, len(vertical))]
    vi = 0
    hi = 0
    execs = []
    while vi < len(vertical):
        while hi < len(horizontal):
            execs.append(executor(vi, hi))
            hi += _unit
        vi += _unit
    await asyncio.gather(*execs)
    return result
