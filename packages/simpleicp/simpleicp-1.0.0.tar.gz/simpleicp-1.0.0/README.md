# simpleICP

This package contains an implementation of a rather simple version of the [Iterative Closest Point (ICP) algorithm](https://en.wikipedia.org/wiki/Iterative_closest_point).

## Documentation

This python implementation is just one of several (almost identical) implementations in various programming languages. They all share a common documentation here: https://github.com/pglira/simpleICP

## Installation

You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/simpleicp/):

```
pip install simpleicp
```

## How to use

```python
import simpleicp
import numpy as np

# Read fixed and movable point cloud from xyz files into n-by-3 numpy arrays
X_fix = np.genfromtxt("dragon1.xyz")
X_mov = np.genfromtxt("dragon2.xyz")

# Run simpleICP!
H, X_mov_transformed = simpleicp.simpleicp(X_fix, X_mov)
```

``dragon1.xyz`` and ``dragon2.xyz`` are not included in this package. They can be downloaded (among other example files) [here](https://github.com/pglira/simpleICP/tree/master/data).