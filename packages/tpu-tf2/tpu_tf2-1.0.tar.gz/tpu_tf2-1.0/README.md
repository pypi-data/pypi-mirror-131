# TPU usage in colab with single line of code

## Installation

To install the package from the PyPi repository you can execute the following
command:
```sh
pip install tpu_tf2
```
If you prefer, you can clone it and run the setup.py file. Use the following commands to get a copy from GitHub and install all dependencies:
```bash
git clone https://github.com/ashishpatel26/regressionmetrics.git
cd tpu_tf2
pip install .
```
## Usage

> usage in colab :

```python
from tpu_tf2.tpu_tf2 import strategy
strategy.num_replicas_in_sync

> output : 8
```

💁 Thanks for reading and forking.
---
