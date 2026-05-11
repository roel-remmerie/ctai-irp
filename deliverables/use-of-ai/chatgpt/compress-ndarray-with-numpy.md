using numpy, I want to compress an ndarray by adding corresponding cells along the 0 axis

What you’re describing is essentially summing (or reducing) along axis 0. NumPy already gives you a clean, efficient way to do that.

If you have an array like this:

import numpy as np

arr = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

and you want to “compress” it by adding corresponding cells along axis 0 (i.e., summing each column), just do:

compressed = np.sum(arr, axis=0)

Result:

array([12, 15, 18])

That works because:

    axis=0 means “collapse rows” (operate down the rows, per column)

    So each position is the sum of all values in that column

If you want to keep the dimensionality (e.g., shape (1, n) instead of (n,)), you can do:

compressed = np.sum(arr, axis=0, keepdims=True)

If you meant something slightly different—like summing in chunks along axis 0 (e.g., every 2 rows)—say so and I can show how to reshape or group before summing.


