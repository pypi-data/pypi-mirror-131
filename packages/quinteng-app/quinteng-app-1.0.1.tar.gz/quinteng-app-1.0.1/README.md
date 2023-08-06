# Quinteng App

[![License](https://img.shields.io/github/license/Quinteng/quinteng-app.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)[![Build Status](https://img.shields.io/travis/com/Quinteng/quinteng-app/master.svg?style=popout-square)](https://travis-ci.com/Quinteng/quinteng-app)[![](https://img.shields.io/github/release/Quinteng/quinteng-app.svg?style=popout-square)](https://github.com/Quinteng/quinteng-app/releases)[![](https://img.shields.io/pypi/dm/quinteng-app.svg?style=popout-square)](https://pypi.org/project/quinteng-app/)

**Quinteng** is an open-source framework for working with noisy quantum computers at the level of pulses, circuits, and algorithms.

Quinteng is made up of elements that each work together to enable quantum computing. This element is **App**, which provides high-performance quantum computing simulators with realistic noise models.

## Installation

We encourage installing Quinteng via the PIP tool (a python package manager), which installs all Quinteng elements, including this one.

```bash
pip install quinteng
```

PIP will handle all dependencies automatically for us and you will always install the latest (and well-tested) version.

To install from source, follow the instructions in the [contribution guidelines](https://github.com/Quinteng/quinteng-app/blob/master/CONTRIBUTING.md).

## Installing GPU support

In order to install and run the GPU supported simulators on Linux, you need CUDA&reg; 10.1 or newer previously installed.
CUDA&reg; itself would require a set of specific GPU drivers. Please follow CUDA&reg; installation procedure in the NVIDIA&reg; [web](https://www.nvidia.com/drivers).

If you want to install our GPU supported simulators, you have to install this other package:

```bash
pip install quinteng-app-gpu
```

This will overwrite your current `quinteng-app` package installation giving you
the same functionality found in the canonical `quinteng-app` package, plus the
ability to run the GPU supported simulators: statevector, density matrix, and unitary.

**Note**: This package is only available on x86_64 Linux. For other platforms
that have CUDA support you will have to build from source. You can refer to
the [contributing guide](https://github.com/Quinteng/quinteng-app/blob/master/CONTRIBUTING.md#building-with-gpu-support)
for instructions on doing this.

## Simulating your first quantum program with Quinteng App
Now that you have Quinteng App installed, you can start simulating quantum circuits with noise. Here is a basic example:

```
$ python
```

```python
import quinteng
from quinteng import IBMQ
from quinteng.providers.app import AppSimulator

# Generate 3-qubit GHZ state
circ = quinteng.QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure_all()

# Construct an ideal simulator
appsim = AppSimulator()

# Perform an ideal simulation
result_ideal = quinteng.execute(circ, appsim).result()
counts_ideal = result_ideal.get_counts(0)
print('Counts(ideal):', counts_ideal)
# Counts(ideal): {'000': 493, '111': 531}

# Construct a noisy simulator backend from an IBMQ backend
# This simulator backend will be automatically configured
# using the device configuration and noise model 
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_athens')
appsim_backend = AppSimulator.from_backend(backend)

# Perform noisy simulation
result_noise = quinteng.execute(circ, appsim_backend).result()
counts_noise = result_noise.get_counts(0)

print('Counts(noise):', counts_noise)
# Counts(noise): {'000': 492, '001': 6, '010': 8, '011': 14, '100': 3, '101': 14, '110': 18, '111': 469}
```

## Contribution Guidelines

If you'd like to contribute to Quinteng, please take a look at our
[contribution guidelines](https://github.com/Quinteng/quinteng-app/blob/master/CONTRIBUTING.md). This project adheres to Quinteng's [code of conduct](https://github.com/Quinteng/quinteng-app/blob/master/CODE_OF_CONDUCT.md). By participating, you are expect to uphold to this code.

We use [GitHub issues](https://github.com/Quinteng/quinteng-app/issues) for tracking requests and bugs. Please use our [slack](https://quinteng.slack.com) for discussion and simple questions. To join our Slack community use the [link](https://quinteng.slack.com/join/shared_invite/zt-fybmq791-hYRopcSH6YetxycNPXgv~A#/). For questions that are more suited for a forum we use the Quinteng tag in the [Stack Exchange](https://quantumcomputing.stackexchange.com/questions/tagged/quinteng).

## Next Steps

Now you're set up and ready to check out some of the other examples from our
[Quinteng IQX Tutorials](https://github.com/Quinteng/quinteng-tutorials/tree/master/tutorials/simulators) or [Quinteng Community Tutorials](https://github.com/Quinteng/quinteng-community-tutorials/tree/master/app) repositories.

## Authors and Citation

Quinteng App is the work of [many people](https://github.com/Quinteng/quinteng-app/graphs/contributors) who contribute
to the project at different levels. If you use Quinteng, please cite as per the included [BibTeX file](https://github.com/Quinteng/quinteng/blob/master/Quinteng.bib).

## License

[Apache License 2.0](LICENSE.txt)
