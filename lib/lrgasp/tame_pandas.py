# this prevents errors like:
#   OpenBLAS blas_thread_init: RLIMIT_NPROC 4096 current, 6191196 max
#   OpenBLAS blas_thread_init: pthread_create failed for thread 2 of 64: Resource temporarily unavailable

# although it didn't help enough or work right or something

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import pandas  # noqa: F401
