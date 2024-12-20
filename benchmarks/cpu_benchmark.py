import time
import os
import concurrent.futures
from tqdm import tqdm

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def cpu_stress_test_single_threaded(duration=60, update_callback=None):
    """Single-threaded stress test by calculating prime numbers for a given duration."""
    start_time = time.time()
    end_time = start_time + duration
    prime_count = 0
    num = 2

    with tqdm(total=duration, desc="Single-threaded Progress", unit="s") as pbar:
        while time.time() < end_time:
            if is_prime(num):
                prime_count += 1
            num += 1
            if update_callback:
                update_callback(prime_count)
            elapsed_time = int(time.time() - start_time)
            pbar.n = elapsed_time
            pbar.refresh()

    return prime_count

def cpu_stress_test_multi_threaded(duration=60, update_callback=None):
    """Multi-threaded stress test by calculating prime numbers for a given duration."""
    num_threads = os.cpu_count()
    start_time = time.time()
    end_time = start_time + duration
    prime_counts = [0] * num_threads

    def worker(start_num, thread_index):
        local_prime_count = 0
        num = start_num
        while time.time() < end_time:
            if is_prime(num):
                local_prime_count += 1
            num += num_threads
            prime_counts[thread_index] = local_prime_count
            if update_callback:
                update_callback(sum(prime_counts))

    with tqdm(total=duration, desc="Multi-threaded Progress", unit="s") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, i, i) for i in range(num_threads)]
            while not all(f.done() for f in futures):
                elapsed_time = int(time.time() - start_time)
                pbar.n = elapsed_time
                pbar.refresh()
                time.sleep(0.1)  # Sleep briefly to avoid excessive CPU usage in the main thread

    return sum(prime_counts)

def run_benchmark_and_display():
    single_threaded_score = [0]
    multi_threaded_score = [0]

    def update_single_threaded_progress(prime_count):
        single_threaded_score[0] = prime_count

    def update_multi_threaded_progress(prime_count):
        multi_threaded_score[0] = prime_count

    print("Starting single-threaded stress test...")
    single_threaded_score[0] = cpu_stress_test_single_threaded(update_callback=update_single_threaded_progress)
    print(f"Single-threaded CPU Benchmark Score: {single_threaded_score[0]} primes")

    print("\nStarting multi-threaded stress test...")
    multi_threaded_score[0] = cpu_stress_test_multi_threaded(update_callback=update_multi_threaded_progress)
    print(f"Multi-threaded CPU Benchmark Score: {multi_threaded_score[0]} primes")

    return single_threaded_score[0], multi_threaded_score[0]

# Example usage
if __name__ == "__main__":
    single_threaded_score, multi_threaded_score = run_benchmark_and_display()
    print(f"Single-threaded Score: {single_threaded_score}")
    print(f"Multi-threaded Score: {multi_threaded_score}")