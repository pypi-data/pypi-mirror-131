.. _quickstart:

========================================
Quickstart: Single Parameter Calibration
========================================

This is a minimal optimization task for a simple single parameter problem in a python script. Alternatively you can run the code will work an Jupyter Python Notebook.

Prerequisites
=============

* Access to an installed software instance with url i.e. 
    * https://www.qcalibrate.beta.optimal-control.net:31603 (external)
    * https://www.qcalibrate.beta.optimal-control.net:31603 (FZ Jülich network)
* LDAP account in the FZJ network or a GitHub account. To get the authorization please register yourself on https://iffgit.fz-juelich.de/ using FZJ LDAP or GitHub.com account  
  and then contact :email:`Roman Razilov <r.razilov@fz-juelich.de>`.
* Python 3.8 or higher

Client environment
==================

* We recommend to use `virtual environment <https://docs.python.org/3/library/venv.html>`_ to avoid dependency conflicts
* Install qcalibrateremote library in your environment with **pip**.
    .. code-block:: console

        (.venv)$ pip install -U qcalibrateremote

**-U** forces upgrade to the latest version

* For *conda* environment install *grcpio* explicitly.
    .. code-block:: console

        (.venv)$ conda install grpcio 


Client Code
===========

Optimization parameters must be specified in order to start an optimization. The configuration can be defined via web UI or using the API


* Create a client script:

    .. code-block:: python
        :name: qcalibrateremote-quickstart.py
        
        from qcalibrateremote import EvaluateFigureOfMerit, FigureOfMerit, create_optimizer_client

        token=("ey...")

        optimizer_client = create_optimizer_client(
            host="grpc.qcalibrate.beta.optimal-control.net", port=31603, token=token)

        # create optimization experiment
        experiment_builder = optimizer_client.create_parameter_optimization_experiment("Quickstart parameter optimization")

        with experiment_builder.configuration() as configuration:
            # optimize parameter x in range 0..1 with initial value 0.5
            with configuration.parameter("x") as x:
                x.lower_limit = 0
                x.upper_limit = 1
                x.initial_value = 0.5
                x.initial_variation = 0.3
                               
            with configuration.direct_search_method_settings() as dsm_settings:
                with dsm_settings.stopping_criteria() as stopping_criteria:
                    stopping_criteria.iterations_number = 100

        experiment_id = optimizer_client.add_experiment(experiment_builder)

        print(experiment_id)

        # define FigureOfMerit (loss) evaluation class
        class QuickstartFom(EvaluateFigureOfMerit):

            def __init__(self, *args, **kwargs) -> None:
                super().__init__()

            def infidelity(self, x) -> float:
                return (x - 0.33)**2

            def evaluate(self, parameters: Dict[str, float], **kwargs) -> FigureOfMerit:
                """Abstract method for figure of merit evaluation"""
                return FigureOfMerit(self.infidelity(**parameters), '')


        # run optimization 
        optimization_result = optimizer_client.run(
            experiment_id=experiment_id, evaluate_fom_object=QuickstartFom())

        print(optimization_result.top[0].parameters["x"])

* Open the web UI

.. |key| image:: _static/key-icon.png
  :width: 17
  :height: 16

* Create an access token by click on the |key| icon

    .. figure :: _static/quickstart-API-key.png
        
        *Getting API token*

* paste  token to your script

Running Optimization
====================

* run the script

* while the optimization run you can observe the progress by selecting the last run of your last experiment

Results
=======

* The :meth:`qcalibrateremote.QOptimizerClient.run` method returns a :class:`qcalibrateremote.OptimizationResultCollector` object,
  containing initial parameters and configuration, all iterations and the iteration with best (lowest) figure-of-merit value 
  (:attr:`qcalibrateremote.OptimizationResultCollector.top`).

.. raw:: latex

    \clearpage