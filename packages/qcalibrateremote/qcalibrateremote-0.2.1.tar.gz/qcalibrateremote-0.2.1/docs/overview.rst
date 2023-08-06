=====================
Architecture Overview 
=====================

The software consists of a software service
and a **qcalibrateremote** client library.
The deployed software service is a Kubernetes application and uses `gRPC<https://grpc.io/>`_
for client-server communication. The application is federated with an `OpenID Connect <https://openid.net/connect/>`_
server for user authentication and authorization. 


Optimization
------------

The following sequence :numref:`interaction` describes a typical calibrations sequence.
The client code, developed and maintained by the user is responsible for interacting with controlled system, and for applying control signals
parameterized with parameters and pulse shapes supplied by the optimization service, performing measurement and calculating the infidelity value.
The interface to the optimization service provided by a python library.

.. _interaction:
.. mermaid:: interaction.mmd
    :caption: Calibration sequence diagram

.. raw:: latex

    \clearpage

Data Model
----------
Users, defined by their account are isolated and see only own data. 
The optimization service database stores intermediate results to enable live monitoring, review of optimization experiments.

The user defines and manages experiments which define the optimization parameters, algorithms and stopping criteria.

The data model schema is shown on the diagram :numref:`data-model`

.. _data-model:
.. mermaid:: data-model.mmd
    :caption: Calibration entity model

.. raw:: latex

    \clearpage