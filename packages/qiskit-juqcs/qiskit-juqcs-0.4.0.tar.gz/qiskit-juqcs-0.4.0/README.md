# qiskit-juqcs
> Qiskit provider for JUQCS (Juelich Universal Quantum Computer Simulator).

<!---[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]--->

This package allows a user with valid [Judoor](https://judoor.fz-juelich.de/) credentials to use [JUQCS](https://arxiv.org/abs/1805.04708) (Juelich Universal Quantum Computer Simulator)
for simulating quantum circuits of up to 40 qubits on HPC systems of the Juelich Supercomputing Center.

Currently two modes of operation are supported by the JUQCS simulator:
   * Sampling mode (```qasm_simulator```): up to 100.000 shots and up to 40 qubits.
   * Statevector mode (```statevector_simulator```): up to 20 qubits.

<!---![](header.png)--->

## Installation

<!---```sh
pip intall qiskit-juqcs
```--->
```sh
pip install git+https://jugit.fz-juelich.de/qip/juniq-platform/qiskit-juqcs.git
```
or
```sh
pip install git+ssh://git@jugit.fz-juelich.de/qip/juniq-platform/qiskit-juqcs.git
```

## First steps

If you are using this package from JUNIQ-Cloud this step will be taken care of automatically, you may skip to the next section.

If you are manually installing this package on your local machine you will be prompted to provide your [Judoor](judoor.fz-juelich.de/) username and password when first importing the module. These credentials will be stored in your machine so authentication against JUNIQ-service will happen automatically the next time. Every time it is imported, the package checks with JUNIQ-service if the credentials are valid. In case you provided the wrong credentials or you have updated them since the last time you used the package you will be prompted to provide them again.

---
**NOTE**

The credentials will not be updated until you import the module again in a new Python session.

---
<!---_For more examples and usage, please refer to the [Wiki][wiki]._--->

## Usage example

This section shows how to submit a circuit for simulation to JUQCS.

1. Import Qiskit and create the circuit which we want to simulate: 
   
    ```py
    import qiskit

    circuit = qiskit.QuantumCircuit(5)
    circuit.h(0)
    circuit.cx(0,1)
    circuit.cx(0,2)
    circuit.measure_all()
    ```
2. Import the Juqcs provider and choose a backend from `'statevector_simulator'` or `'qasm_simulator'`:

    ```py
    from juqcs import Juqcs
    backend = Juqcs.get_backend('qasm_simulator')
    ```
    ---
    **NOTE**

    Since each simulator returns a different type of output, different limitations for the maximum qubit size apply (20 qubits for `'statevector_simulator'` and 40 qubits for `'qasm_simulator'`).

    ---

3. So far the process has not deviated from the usage of a typical Qiskit backend, but the following step is unique to the JUQCS backends:

    ```py
    backend.allocate(minutes=30, max_qubits=5, reservation=None)
    ```
    ---
    **NOTE**
    This function may take a few minutes to return, depending largely on the load of the HPC system at the time of submission.

    ---

    Since the JUQCS simulator is deployed on an HPC system whose compute resources are shared with many other users, we now need to request the HPC system for permission to simulate our circuits. In this step we are making two "promises" to the HPC system, and the success of our simulation experiment depends on us keeping these promises:
        
    * We promise that the biggest circuit that we want to simulate under this allocation will have at most `int(max_qubits)` qubits. If we try to submit a bigger circuit the HPC system would not have allocated sufficient compute resources for us, so the simulation would fail. We only need to include this parameter if we want to simulate circuits larger than 32 qubits, since any circuit up to and including this size requires exactly the same amount of compute resources.

    * We promise that we will be done with our simulation experiments within `int(minutes)` minutes. By default, this parameter is set to 60 minutes, and the longest running allocation we can create is 24 hours (=1440 minutes). After this time is exceeded our allocation will expire, so circuit simulation submissions beyond this point would fail. In order to fix this we would need to create a new allocation. 

    ---
    **NOTE**
    Optionally we can pass `str(reservation)` to our allocation request if we have been given an HPC reservation ID (e.g. when attending a training course at JSC). If you do not have a reservation ID do not worry, JUQCS will work without one too.

    ---

4. We can make sure that the allocation has been successfully created for us by calling `backend.status().status_msg`. If a valid allocation is available, we will see a message like `'Resource allocation #{allocation ID} of {number} qubits available until {expiration time}.'`.

5. Now we can use our JUQCS backend just as any other typical Qiskit backend, e.g.:

    ```py
    job = qiskit.execute(circuit, backend=backend, shots=1000, seed=10)
    result = job.result()
    print(result.get_counts())
    ```
    When ```job.result()``` is called with ```partial=True``` as argument, this method will attempt to retrieve partial results of failed jobs. In this case, precaution should be taken when accessing individual experiments, as doing so might cause an exception. The ```success``` attribute of the returned Result instance can be used to verify whether it contains partial results.

6. Once we are finished with our experiments it is good practice to call `backend.deallocate()`. 
   
   In case our allocation is still running this will revoke the allocation, so that we only get charged for the time our allocation was running, instead of for the time we promised the HPC system we would need the allocation for. If the allocation is not running anymore this function will not have any effect, so it's better to call it anyway to be on the safe side!


## Release History
* 0.4.0
    - Client-side changes to execute JUQCS on JURECA-dc.
* 0.3.0
    - Now using juniq-service:juqcs-service script bundle.
    - Authentication mechanism reworked.
    - Improved error handling and reporting.
    - Several bugs fixed.
* 0.2.0
    - First public release.


## Meta

Carlos Gonzalez Calaza - c.gonzalez.calaza@fz-juelich.de

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://gitlab.com/juniq-platform/qiskit-juqcs](https://gitlab.com/juniq-platform/qiskit-juqcs)




<!---
## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
--->
<!-- Markdown link & img dfn's -->
<!---[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki--->
