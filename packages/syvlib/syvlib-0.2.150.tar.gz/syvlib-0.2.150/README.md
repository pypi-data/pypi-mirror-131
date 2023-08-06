# SYVLIB #
0.2.150

### Introduction

SYVLIB is an SDK which provides tools for building client applications for the [SYV](https://bitbucket.org/Thomas_Ash/syv/src/main/) server.

### Installation

`pip install syvlib`

### Usage

First you need to open a session with your SYV instance:

```
import syvlib

session = syvlib.Session('https://syv.example.com', 'myusername', 'mypassword')
```

Once you have a session, you can open a cycle on a pump:

```
cycle = session.open('mypump')
```

Depending on the pump's engine type, you may then want to download drops:
```
drops = cycle.pull_drops('input', cycle.drop_uids.get('input'))
```

...or upload drops:
```
import numpy as np

drops = [syvlib.Drop(cycle, {'myarrayspec': np.zeros((64,64))})]
cycle.push_drops('output', drops)
```

...or upload a record:
```
with open('myfile.zip', 'rb') as stream:
    cycle.push_record('input', stream)
```

In any case, you will eventually need to commit the cycle:
```
cycle.commit_and_wait()

if cycle.error is not None:
    raise Exception(cycle.error)
```

Once the cycle has successfully completed the commit process, you may then be able to download a record (again, depending on the engine type):
```
with open('myfile.zip', 'wb') as stream:
    cycle.pull_record('output', stream)
```
