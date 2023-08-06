# Python Application Heartbeats

[![Documentation Status](https://readthedocs.org/projects/apphb-python/badge/?version=latest)](https://apphb-python.readthedocs.io/en/latest/?badge=latest)

A Python application-level heartbeats interface.


## Installing

The `apphb` package is published in the Python Package Index and installable with pip:

```sh
pip install apphb
```

To install from source:

```sh
pip install .
```


## Usage

The core component is the `Heartbeat` class.
The user defines a window period (`window_size`) that specifies a sliding window length over which performance is computed.
Users may optionally specify other fields to compute sums and rates for.

For example:

```Python
total_iters = 10
window_size = 2
hbt = Heartbeat(window_size)
for tag in range(total_iters):
    start_time = time.monotonic()
    application_kernel()
    end_time = time.monotonic()
    hbt.heartbeat(tag, (end_time - start_time,))
    print(str(tag) + ': Instant performance: ' + str(hbt.get_instant_rate()))
    print(str(tag) + ': Window performance: ' + str(hbt.get_window_rate()))
print('Global performance: ' + str(hbt.get_global_rate()))
```

See the `examples` directory for more detailed use cases, including specifying custom fields.


## Project Source

Find this and related project sources at the [libheartbeats organization on GitHub](https://github.com/libheartbeats).  
This project originates at: https://github.com/libheartbeats/apphb-python

Bug reports and pull requests for bug fixes and enhancements are welcome.
