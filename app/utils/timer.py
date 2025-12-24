import time


class Timer:
    def __init__(self):
        self.start_times = {}
        self.durations = {}

    def start(self, name: str):
        self.start_times[name] = time.time()

    def stop(self, name: str):
        if name in self.start_times:
            self.durations[name] = time.time() - self.start_times[name]

    def report(self):
        print("\n⏱️ Latency Breakdown:")
        total = 0
        for name, duration in self.durations.items():
            print(f"  {name}: {duration:.3f}s")
            total += duration
        print(f"  TOTAL: {total:.3f}s\n")
