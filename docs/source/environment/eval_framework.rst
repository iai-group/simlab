Evaluation framework
====================

The framework includes the definition of the supported tasks and metrics, and the logic to perform simulation-based evaluation. It is designed to be modular and extensible to support diverse evaluation scenarios.

The workflow of the evaluation process is illustrated in the following diagram:

.. image:: ../_static/SimBased_Eval_UML.png
    :align: center
    :width: 400px
    :alt: UML activity diagram of the simulation-based evaluation process. The experiment data, highlighted in green boxes, is saved in the storage. It is assumed that the systems are available in the systems registry.

Additional details on implementation can be found in the :doc:`developer documentation <../eval_framework/index>`.