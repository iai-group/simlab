SimLab
======

This is the central piece of the environment. It comprises a web application and the codebase to perform simulation-based evaluation.

Web application
---------------

The web application includes a :doc:`React-based user interface <../webapp/frontend>` and a :doc:`Flask-based backend <../webapp/backend>`. It is connected to the MongoDB database to store and retrieve data. The web application is the main point of interaction for the users of the platform.

Codebase
--------

The codebase includes the definition of the supported tasks and metrics, and the logic to perform simulation-based evaluation. It is designed to be modular and extensible to support diverse evaluation scenarios.

The workflow of the evaluation process is as follows:

1. A simulation platform is created to facilitate the communication between the different conversational agents and user simulators.
2. For each pair of conversational agent and user simulator, synthetic conversations are generated given the information needs associated with the task. 
3. The synthetic conversations are then evaluated with regards to the specified metrics in the run configuration.
4. The results of the evaluation are stored in the database.

Additional details on implementation can be found in the :doc:`developer documentation <../simlab/index>`.