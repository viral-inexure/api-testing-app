import time
import asyncio
import selectors
import contextlib


class TimedSelector(selectors.DefaultSelector):
    select_time = 0.

    def reset_select_time(self):
        self.select_time = 0.

    def select(self, timeout=None):
        if timeout <= 0:
            return super().select(timeout)
        start = time.time()
        try:
            return super().select(timeout)
        finally:
            self.select_time += time.time() - start


class TimedEventLoopPolicy(asyncio.DefaultEventLoopPolicy):

    def new_event_loop(self):
        selector = TimedSelector()
        return asyncio.DefaultEventLoopPolicy._loop_factory(selector)


@contextlib.contextmanager
def print_timing():
    asyncio.get_event_loop()._selector.reset_select_time()
    real_time = time.time()
    process_time = time.process_time()
    yield
    real_time = time.time() - real_time
    cpu_time = time.process_time() - process_time
    select_time = asyncio.get_event_loop()._selector.select_time
    other_io_time = max(0., real_time - cpu_time - select_time)
    print(f"CPU time:      {cpu_time:.3f} s")
    print(f"Select time:   {select_time:.3f} s")
    print(f"Other IO time: {other_io_time:.3f} s")
    print(f"Real time:     {real_time:.3f} s")


# Testing

async def main():
    print("~ Correct IO management ~")
    with print_timing():
        await asyncio.sleep(1)
        sum(range(10 ** 6))
    print()

    print("~ Incorrect IO management ~")
    with print_timing():
        time.sleep(0.2)
        await asyncio.sleep(0.8)
        sum(range(10 ** 6))
    print()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(TimedEventLoopPolicy())
    asyncio.run(main())
