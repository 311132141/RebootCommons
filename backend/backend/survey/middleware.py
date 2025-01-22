import os
import psutil

class MemoryUsageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get memory usage before processing
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 ** 2  # Convert to MB

        response = self.get_response(request)

        # Get memory usage after processing
        mem_after = process.memory_info().rss / 1024 ** 2  # Convert to MB
        print(f"Memory Usage: {mem_before:.2f} MB -> {mem_after:.2f} MB")

        return response
