import asyncio

SIGNAL = None


async def zoxide_producer(queue: asyncio.Queue):
    args = ("zoxide", "query", "--list")
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    assert proc.stdout
    async for line in proc.stdout:
        str_line = line.decode().strip()
        await queue.put(str_line)


async def fd_producer(queue: asyncio.Queue):
    args = ("fd", "--search-path", "/home/paolo", "-d", "1")
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    assert proc.stdout
    async for line in proc.stdout:
        str_line = line.decode().strip()
        await queue.put(str_line)


async def fzf_consumer(queue: asyncio.Queue) -> list[str]:
    args = ("fzf", "-m")
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )

    assert proc.stdin
    while True:
        item = await queue.get()
        if item is SIGNAL:
            queue.task_done()
            break

        proc.stdin.write(f"{item}\n".encode())
        await proc.stdin.drain()
        queue.task_done()

    proc.stdin.write_eof()

    # process consumer output and return
    assert proc.stdout
    output = []
    async for line in proc.stdout:
        output.append(line.decode().strip())

    return output


async def main():
    queue = asyncio.Queue()

    consumer_tasks = asyncio.create_task(fzf_consumer(queue))
    producer_tasks = [
        asyncio.create_task(fd_producer(queue)),
        asyncio.create_task(zoxide_producer(queue)),
    ]

    await asyncio.gather(*producer_tasks)

    # signal consumer to stop looking at the queue
    await queue.put(SIGNAL)
    await queue.join()

    # retrieve output
    output = await asyncio.gather(consumer_tasks)
    print(output)


asyncio.run(main())
