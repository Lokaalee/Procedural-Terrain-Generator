import time


class PerformanceTester:

    def measure(self, function, *args):

        start = time.perf_counter()

        result = function(*args)

        end = time.perf_counter()

        elapsed = end - start

        return result, elapsed