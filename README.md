# GPU Meter

Power Consumption Meter for NVIDIA GPUs.

## Installation

```
pip3 install gpumeter
```

## Usage

```python
# Import the Meter
from gpumeter import Meter

# Initialize with Interval (Seconds)
m = Meter(20) # Get power status per 20 seconds.

# Stop after the time-consuming task finished.
m.stop()

# It will output:
> Total Consumed: 8047.28 Wh
> Your Badge is Ready! See https://img.shields.io/badge/Power%20Consumption-8047.28%20Wh-green
```
