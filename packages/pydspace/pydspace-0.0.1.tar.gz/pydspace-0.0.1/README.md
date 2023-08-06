# WIP
Python interface for interoperability with dSpace running in Matlab.

# Dependencies
- python >= 3.6
- numpy
- matlabengineforpython

# Installation
```shell
pip install pydspace
```

# Example

```python
import pydspace
import numpy as np

dspace_path = "YOUR PATH TO MATLAB DSPACE"

M1 = np.random.rand(100,100)
M2 = np.random.rand(100,100
M_no_name = np.random.rand(100,100)

pydspace.dspace("matrix1", M1, "matrix2", M2, M_no_name, path=dspace_path)
```
