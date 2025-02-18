Overview
========

The main components of the environment are:

- :doc:`Docker registry <registry>`: serves as a repository for Docker images of conversational agents and user simulators
- :doc:`Web application <webapp>`: serves as the main interface for users to interact with the platform
- :doc:`Evaluation framework <eval_framework>`: contains the codebase for the evaluation framework
- :doc:`Jenkins cluster <jenkins>`: manages the execution of runs (evaluation tasks)
- NGINX: serves as a reverse proxy to route requests to the appropriate services
- Prometheus and Grafana: monitor the platform's performances
- MongoDB: storage for the platform data

.. image:: ../_static/SimLab_Platform.pdf
    :align: center
    :width: 700px
    :alt: Overview of SimLab platform
