import numpy as np
import time

size = 1000000
# Create a 1D array of zeros
zeros_array = np.array(range(size))
print("1D array of zeros:")
print(zeros_array)

l1= list(range(size))
l2= list(range(size))
start_time = time.time()
l3 = [x+y for x,y in zip(l1,l2)]
print("1D array of zeros:")
print(l3)
end_time = time.time()
print(f"Time taken for list addition: {end_time - start_time} seconds")

n1 = np.arange(size)
n2 = np.arange(size)
start_time = time.time()
n3 = n1 + n2
print("1D array of zeros:")
print(n3)
end_time = time.time()
print(f"Time taken for numpy addition: {end_time - start_time} seconds")

rev_q1= np.array([12, 15, 14, 10, 8])
print(rev_q1.ndim)  # Output: 1
rev = np.array([[12, 15, 14], [10, 8, 9]])
print(rev.ndim)  # Output: 2
print(rev[1,0])
print(rev.dtype)  # Output: int64