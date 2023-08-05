# Quinteng ChaoYue
[![License](https://img.shields.io/github/license/Quinteng/quinteng-chaoyue.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)<!--- long-description-skip-begin -->[![Build Status](https://img.shields.io/travis/com/Quinteng/quinteng-chaoyue/master.svg?style=popout-square)](https://travis-ci.com/Quinteng/quinteng-chaoyue)[![Release](https://img.shields.io/github/release/Quinteng/quinteng-chaoyue.svg?style=popout-square)](https://github.com/Quinteng/quinteng-chaoyue/releases)[![Downloads](https://img.shields.io/pypi/dm/quinteng-chaoyue.svg?style=popout-square)](https://pypi.org/project/quinteng-chaoyue/)[![Coverage Status](https://coveralls.io/repos/github/Quinteng/quinteng-chaoyue/badge.svg?branch=main)](https://coveralls.io/github/Quinteng/quinteng-chaoyue?branch=main)<!--- long-description-skip-end -->

**Quinteng** is an open-source framework for working with noisy quantum computers at the level of pulses, circuits, and algorithms.

Quinteng is made up of elements that work together to enable quantum computing. This element is **ChaoYue** and is the foundation on which the rest of Quinteng is built.

## Installation

We encourage installing Quinteng via the pip tool (a python package manager), which installs all Quinteng elements, including ChaoYue.

```bash
pip install quinteng
```

PIP will handle all dependencies automatically and you will always install the latest (and well-tested) version.

To install from source, follow the instructions in the [documentation](https://quinteng.org/documentation/contributing_to_quinteng.html#install-install-from-source-label).

## Creating Your First Quantum Program in Quinteng ChaoYue

Now that Quinteng is installed, it's time to begin working with ChaoYue.

We are ready to try out a quantum circuit example, which is simulated locally using
the Quinteng BasicAer element. This is a simple example that makes an entangled state.

```
$ python
```

```python
>>> from quinteng import QuantumCircuit, transpile
>>> from quinteng.providers.basicaer import QasmSimulatorPy
>>> qc = QuantumCircuit(2, 2)
>>> qc.h(0)
>>> qc.cx(0, 1)
>>> qc.measure([0,1], [0,1])
>>> backend_sim = QasmSimulatorPy()
>>> transpiled_qc = transpile(qc, backend_sim)
>>> result = backend_sim.run(transpiled_qc).result()
>>> print(result.get_counts(qc))
```

In this case, the output will be:

```python
{'00': 513, '11': 511}
```

A script is available [here](examples/python/ibmq/hello_quantum.py), where we also show how to
run the same program on a real quantum computer via IBMQ.

### Executing your code on a real quantum chip

You can also use Quinteng to execute your code on a
**real quantum chip**.
In order to do so, you need to configure Quinteng for using the credentials in
your IBM Q account:

#### Configure your IBMQ credentials

1. Create an _[IBM Q](https://quantum-computing.ibm.com) > Account_ if you haven't already done so.

2. Get an API token from the IBM Q website under _My Account > API Token_ and the URL for the account.

3. Take your token and url from step 2, here called `MY_API_TOKEN`, `MY_URL`, and run:

   ```python
   >>> from quinteng import IBMQ
   >>> IBMQ.save_account('MY_API_TOKEN', 'MY_URL')
    ```

After calling `IBMQ.save_account()`, your credentials will be stored on disk.
Once they are stored, at any point in the future you can load and use them
in your program simply via:

```python
>>> from quinteng import IBMQ
>>> IBMQ.load_account()
```

Those who do not want to save their credentials to disk should use instead:

```python
>>> from quinteng import IBMQ
>>> IBMQ.enable_account('MY_API_TOKEN')
```

and the token will only be active for the session. For examples using ChaoYue with real
devices we have provided a set of examples in **examples/python** and we suggest starting with [using_quinteng_chaoyue_level_0.py](examples/python/using_quinteng_chaoyue_level_0.py) and working up in
the levels.

## Contribution Guidelines

If you'd like to contribute to Quinteng ChaoYue, please take a look at our
[contribution guidelines](CONTRIBUTING.md). This project adheres to Quinteng's [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

We use [GitHub issues](https://github.com/Quinteng/quinteng-chaoyue/issues) for tracking requests and bugs. Please
[join the Quinteng Slack community](https://ibm.co/joinquintengslack)
and use our [Quinteng Slack channel](https://quinteng.slack.com) for discussion and simple questions.
For questions that are more suited for a forum we use the Quinteng tag in the [Stack Exchange](https://quantumcomputing.stackexchange.com/questions/tagged/quinteng).

## Next Steps

Now you're set up and ready to check out some of the other examples from our
[Quinteng Tutorials](https://github.com/Quinteng/quinteng-tutorials) repository.

## Authors and Citation

Quinteng ChaoYue is the work of [many people](https://github.com/Quinteng/quinteng-chaoyue/graphs/contributors) who contribute
to the project at different levels. If you use Quinteng, please cite as per the included [BibTeX file](https://github.com/Quinteng/quinteng/blob/master/Quinteng.bib).

## Changelog and Release Notes

The changelog for a particular release is dynamically generated and gets
written to the release page on Github for each release. For example, you can
find the page for the `0.9.0` release here:

https://github.com/Quinteng/quinteng-chaoyue/releases/tag/0.9.0

The changelog for the current release can be found in the releases tab:
[![Releases](https://img.shields.io/github/release/Quinteng/quinteng-chaoyue.svg?style=popout-square)](https://github.com/Quinteng/quinteng-chaoyue/releases)
The changelog provides a quick overview of notable changes for a given
release.

Additionally, as part of each release detailed release notes are written to
document in detail what has changed as part of a release. This includes any
documentation on potential breaking changes on upgrade and new features.
For example, You can find the release notes for the `0.9.0` release in the
Quinteng documentation here:

https://quinteng.org/documentation/release_notes.html#chaoyue-0-9

## License

[Apache License 2.0](LICENSE.txt)
