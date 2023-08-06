=========================
Qruise Calibration Web UI
=========================

The Web UI provides convenient way to define optimization parameters, manage API keys and monitor the optimization progress.

..

Experiment List
===============
.. figure :: _static/experiment-list-numbered.png
    :width: 1024
    :alt: Experiments List Page

    *Experiment configurations overview page*

1. Opens online help
2. User avatar (as provided via Open ID Connect Federation). Opens pop-up with user name and 
   logout function, if supported by the Open ID Connect provider)
3. Opens a form to edit a new experiment configuration
4. Reloads the experiment list
5. Opens the experiment configuration edit form
6. Click on experiment name opens the :ref:`Run list`
7. Optional description 
8. Experiment configuration creation time
9. Name of the owner (users can see only own experiments)
10. Download the configuration as a JSON document (for backup and change tracking)
11. Count of experiment runs, the link opens runs overview


Experiment Configuration
========================

.. |add| image:: _static/add-icon.png
  :width: 16
  :height: 16

.. |trash| image:: _static/trash-icon.png
  :width: 16
  :height: 16

.. |expand| image:: _static/expand-icon.png
  :width: 16
  :height: 16

.. |home| image:: _static/home-icon.png
  :width: 16
  :height: 16

.. |edit| image:: _static/edit-icon.png
  :width: 16
  :height: 16

.. |reload| image:: _static/reload-icon.png
  :width: 16
  :height: 16

.. |key| image:: _static/key-icon.png
  :width: 17
  :height: 16

.. |cancel| image:: _static/cancel-icon.png
  :width: 16
  :height: 16

Click on |add| icon shows selection of experiment configuration options

* **Parameter Optimization**: Control actions are defined by a relatively small set of real values in a specified range.
  The algorithm searches for parameter values which minimize the measured figure of merit.

* **Pulse optimization (dCRAB)**: Control action are defined by sampled function, found with dressed chopped random basis algorithm.

Selection one of them brings you to a experiment configuration creation/edit page.


.. figure :: _static/experiment-edit-numbered.png
    :width: 1024

    *Experiment configurations edit page*

1. Saves the configuration to the server and returns to experiment list
2. Restores the values to last saved or to the template set of parameters
3. Cancels edit and return to the experiment list
4. Controls tab, here one can defined the subject of optimization: variable parameters or functions
5. Optimization algorithm setting tab, changes meta-parameter for training
6. Figure of merit setting tab. Here a user can define optional arguments supplied to 
   the figure of merit evaluator evaluator object constructor.


Control
-------
This tab specify the subjects of optimization: parameters and pulses

Pure parameter optimization
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure :: _static/experiment-edit-parameters.png
    :width: 1024

    *Parameter optimization configuration*

This controls area allows to edit a parameters list.
Click on |add| to add a new parameter.
Click on |trash| to remove a parameter.
Click on |expand| (or anywhere outside of text fields) to open details. 

Parameter Fields
""""""""""""""""

* **Name**: the key of the parameter the in dictionary passed to an evaluator
* **Lower Limit, Upper Limit**: limits of possible values
* **Initial value**: Initial value guess
* **Variation**: Initial random variation of the parameter on the early steps of an optimization


Pulse optimization (dCRAB)
""""""""""""""""""""""""""
.. figure :: _static/experiment-edit-pulses.png
    :width: 1024

    *Pulse optimization configuration*

Pulse duration can be optimized separately from a pulse shape and amplitude. Each pulse references a time item,
specifying the pulse length. 
When designing multi-channel control signal (like IQ modulation) both pulses should be in one group, so they share the same
time reference, using identical sample grid. 

Click on |add| to add a new time or pulse.
Click on |trash| to remove a time or pulse.
Click on |expand| (or anywhere outside of text fields) to show details. 

Time Fields
"""""""""""

* **Name**: the key of the parameter in the dictionary passed to an evaluator
* **Initial value**: Initial value guess in arbitrary unit, the actual scaling happens in the client code
* **Optimize**: Whenever the algorithm should try to optimize the value

Pulse Fields
""""""""""""

* **Time**: The time group of the pulse (usually time1)
* **Number of samples**: Number of pulse modelling points on the interval 0...time, 3..2049, default 101
* **Value lower Limit, Value upper Limit**: limit of possible signal amplitudes, values above are clipped
* **Variation**: Initial random variation of the parameter on the early steps of an optimization
* **Basis**: Function bases Fourier or Sigmoid(experimental)
* **Number of basis vectors** subset of randomly selected basis function to fit the function
* **Distribution, Lower Limit, Upper Limit**: Super parameter distribution and bins range, 
  i.e. frequency range for fourier basis. Reduce upper limit to suppress high-frequency harmonics
* **Initial guess**: Initial pulse guess Python lambda function or array of values. Python valid Lambda function with a single parameter 't' 
  can use np (numpy) method and constants
* **Scaling function**: Envelope scaling function applied on a top of a random function i.e. to make sure the pulse starts and ends with 0.  Can be a Python lambda function or array of values. Python valid Lambda function with a single parameter 't' 
  can use np (numpy) method and constants


Optimization
------------


.. figure :: _static/experiment-edit-optimization.png
    :width: 1024

    *Optimization algorithm configuration*

Pure parameter optimization configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Maximal iterations number**: defines the iteration before the optimization is stopped

dCRAB specific parameters
^^^^^^^^^^^^^^^^^^^^^^^^^

`dCRAB algorithm <https://arxiv.org/pdf/1506.04601.pdf>`_ uses a limited set of basis function to model 
an optimal pulse. Since the set function is limited, that suboptimal choice of basis functions results converging 
to a local minimum an a control landscape. dCRAB tries to mitigate it by changing the basis by selecting another 
set of basis functions (super-iteration) and thus changing the control landscape

* **Number of super-iterations**: Number of dCRAB super-iterations
* **Maximum number of iterations per super-iteration**: Number of dCRAB super-iterations

Stopping criteria
^^^^^^^^^^^^^^^^^

* **Absolute error in parameter between iterations**: stops optimization if changes in parameter are below
* **Absolute error in value between iterations**: stops if evaluated FoM value is below
* **Adapt algorithm parameters to dimensionality of problem**: Useful for high-dimensional minimization


Figure Of Merit
---------------

Here one can specify optional parameters supplied to iteration evaluation class constructor. 
The parameters are ignored, if figure-of-merit evaluator is supplied an object

.. figure :: _static/experiment-edit-arguments.png
    :width: 1024

    *Figure of merit constructor arguments*

Run List
========

This page shows the runs of a selected experiment. The last run come first.

.. figure :: _static/run-list-numbered.png

    *Run list page*

1. Click on |home| to return to the :ref:`Experiment List`
2. Name of the selected experiment
3. Click on |edit| to edit the experiment configuration
4. Click on |reload| to reload the runs list
5. Click on|key| to generate and show the run list.
6. Click on creation to navigate to :ref:`Run details`
7. Click on iteration count to navigate to :ref:`Run details`

Run Details
===========

This page shows the details of a run. For currently active run (Finished Time is empty) the page updates automatically to show the optimization progress.
Press |cancel| to force the optimization end

.. figure :: _static/run-details-numbered.png

    *Run details*

1. Click on |home| to return to the :ref:`Experiment List`
2. Click on experiment name to return to :ref:`Run List`
3. This area shows the run summary, including iterations count and best Figure Of Merit (Infidelity value)
4. Configuration as JSON file, for diagnostic purposes
5. Figure of merit chart, showing the development of figure of merit value
6. The content of the pane depends on optimization mode

  * Pure parameter: the evolution of a selected parameter
  * Shape of the selected pulse for last iteration for active run or best iteration for a finished one   
