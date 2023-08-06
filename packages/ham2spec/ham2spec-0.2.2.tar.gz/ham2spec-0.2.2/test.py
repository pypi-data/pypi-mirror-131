import numpy as np
import ham2spec
from time import perf_counter


def main():
    ham = np.loadtxt("ham.txt", delimiter=",", dtype=np.float32)
    mus = np.loadtxt("pig_mus.txt", dtype=np.float32)
    pos = np.loadtxt("pig_pos.txt", dtype=np.float32)
    n = 100_000
    times = list()
    for _ in range(n):
        t_start = perf_counter()
        _ = ham2spec.compute_stick_spectrum(ham, mus, pos)
        t_stop = perf_counter()
        times.append(t_stop - t_start)
    per_call = sum(times) / n * 1e6
    print(f"{per_call:.3f}us per call")


if __name__ == "__main__":
    main()