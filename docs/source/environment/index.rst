Overview
========

The main components of the environment are:

- :doc:`Docker registry <registry>`: serves as a repository for Docker images of conversational agents and user simulators
- :doc:`SimLab <simlab>`: provides web application and codebase to manage the evaluation process
- :doc:`Jenkins cluster <jenkins>`: manages the execution of runs (evaluation tasks)
- NGINX: serves as a reverse proxy to route requests to the appropriate services
- MongoDB: storage for the platform data

.. TODO: Add a diagram to illustrate the environment components


Deployment
----------

The SimLab platform can be deployed locally (testing and development) or in the cloud (production). The deployment process is described in the following sections.

Cloud deployment
^^^^^^^^^^^^^^^^

.. TODO: Add details on cloud-based deployment

Local deployment
^^^^^^^^^^^^^^^^

Before deploying the platform, make sure you have the following prerequisites:

  - Docker
  - Docker Compose
  - SSL certificate and private key should be placed in the folder `nginx/ssl/` with the names `cert.pem` and `privkey.pem` respectively
  - Install requirements for the documentation and build it using Sphinx:
    
.. code-block:: bash

    pip install -r docs_requirements.txt
    sphinx-build -M html docs/source/ build/


**Running SimLab**

To run the platform, execute the following command:

.. code-block:: bash

    docker-compose -f docker-compose.yaml up


This command will start SimLab and make it available at `<https://localhost/>`_.

*Note*: Think of updating the images if you have made changes to the code base.