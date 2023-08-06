===========================
Qruise Calibrate Remote API
===========================

A client library for runnig a control optimization with qruise calibrate software


Note
====

The API is experimental and subject to change without a prior notice


Description
===========

The qcalibrateremote package provides interface to QCalibrate optimization service, providing algorithms helping to define optimal control for quantum system.
The actual optimization algorithm runs on the server, supplying the set of parameters and/or PWC pulses to client side. The client code evaluates the parameters 
by deriving and applying control signals to a system under control, performing measurement, calcualates and returns the figure of merit (infidelity) value. 
The algorithm tries different parameters in order to find optimal values to achieve minimal infidelity. Live progress of optimization can be observed in the in web UI, 
given opportunity to finish the optimization, before the optimization stopping criteria are achieved.

Currently two optimization modes are supported.

- pure parameter optimization 
- Random chopped base PWC function optimization (Fourier and Sigmoid bases)

Installing
===========

Install with **pip**:

.. code-block:: console

    $ pip install qcalibrateremote

for conda environment install grcpio explicitly

.. code-block:: console

    $ conda install grpcio 


Usage
=====

Prerequisits
------------

- Python 3.8+ (developed and tested with 3.8.5)
- Qruise Calibrate account (contact r.razilov@fz-juelich.de for details)
- Direct internet connection to server (may require VPN access)

Experiment
----------
Experiment defines is a set of meta-parameters controlling the optimization
Use use API or Web UI to create an experiment and define optimization parameters. Use online help to get learn about details.
The evaluation of figure of merit class can be supplied as class :code:`evaluate_fom_class=..` or object :code:`evaluate_fom_object=..`

Pure parameter optimization example
-----------------------------------

.. code-block:: python
    :name: parameter-optimizaton.py
    
    # import dependencies
    from typing import Dict

    from qcalibrateremote import (
        EvaluateFigureOfMerit,
        FigureOfMerit,
        create_optimizer_client,
    )

    # setup client connection (copy form web UI: https://www.qcalibrate.staging.optimal-control.net:31603)
    experiment_id="0xabcd"
    token=("ey...")

    optimizer_client = create_optimizer_client(
        host="grpc.qcalibrate.staging.optimal-control.net", port=31603, token=token)

    # define infidelity evaluation class
    class DistanceFom(EvaluateFigureOfMerit):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__()

        def infidelity(self, param1, param2) -> float:
            return (param1 - 0.55)**2 + (param2 - 0.33)**2

        def evaluate(self, parameters: Dict[str, float], **kwargs) -> FigureOfMerit:
            """Abstract method for figure of merit evaluation"""
            # print(parameters)
            return FigureOfMerit(self.infidelity(**parameters), '')

    # run optimization
    optimization_result = optimizer_client.run(experiment_id=experiment_id, evaluate_fom_class=DistanceFom)

    # best fitting parameters
    optimization_result.top[0].parameters 

Rather than create a completely new configuration, one can update an existing experiment configuration

.. code-block:: python

    with optimizer_client.update_experiment(experiment_id) as experiment_builder:
        with experiment_builder.configuration() as configuration:
            with configuration.parameter("param1") as param1:
                param1.initial_value = 0.7
        

    optimization_result = optimizer_client.run(
        experiment_id=experiment_id, evaluate_fom_class=DistanceFom)

    # best fitting parameters
    optimization_result.top[0].parameters 


Pulse optimization example
--------------------------

.. code-block:: python
    :name: pulse-optimizaton.ipynb
    
    # import dependencies
    from typing import Dict

    from qcalibrateremote import (
        EvaluateFigureOfMerit,
        FigureOfMerit,
        create_optimizer_client,
        Pulse,
    )

    # setup client connection (copy form web UI: https://www.qcalibrate.staging.optimal-control.net:31603)
    token=("ey...")

    optimizer_client = create_optimizer_client(
        host="grpc.qcalibrate.staging.optimal-control.net", port=31603, token=token)

    experiment_builder = optimizer_client.create_pulse_optimization_experiment("Pulse optimization", "Created by " + __file__)

    # define configuration

    with experiment_builder.configuration() as configuration:
        
        with configuration.time("time1") as time1:
            time1.initial_value = 1
            time1.optimize = False
        
        with configuration.pulse("pulse1") as pulse1:
            pulse1.time_name = "time1"
            pulse1.lower_limit = -1
            pulse1.upper_limit = 1
            pulse1.bins_number = 21       
            with pulse1.fourier_basis() as fourier_basis:
                fourier_basis.basis_vector_number = 5
                with fourier_basis.uniform_super_parameter_distribution() as uniform_super_parameter_distribution:
                    uniform_super_parameter_distribution.lower_limit = 0.01
                    uniform_super_parameter_distribution.upper_limit = 5
            
            with pulse1.initial_guess() as initial_guess:
                initial_guess.function = "lambda t: 1"
            with pulse1.scaling_function() as scaling_function:
                scaling_function.function = "lambda t: np.exp(-(t - 0.5)**2/(2*0.2**2))"
                
        with configuration.dcrab_settings() as dcrab_settings:
            dcrab_settings.maximum_iterations_per_super_iteration = 50
            dcrab_settings.super_iteration_number = 6
            
    experiment_id = optimizer_client.add_experiment(experiment_builder)

    # define infidelity evaluation class
    def expected_pulse(t):
        return np.sin(2*np.pi*t)**4

    class SineFom(EvaluateFigureOfMerit):

        def evaluate(self, parameters: Dict[str, float], pulses: Dict[str, Pulse], **kwargs) -> FigureOfMerit:
            pulse1 = pulses["pulse1"]

            inf = np.sum((expected_pulse(pulse1.times) - pulse1.values)**2)

            return FigureOfMerit(inf, '{}')

    # run optimization
    optimization_result = optimizer_client.run(experiment_id=experiment_id, evaluate_fom_object=SineFom())

    # plot best fitting pulse
    pulse1 = optimization_result.top[0].pulses["pulse1"]
    import matplotlib.pyplot as plt

    plt.plot(pulse1.times, expected_pulse(pulse1.times))
    plt.plot(pulse1.times, pulse1.values)


