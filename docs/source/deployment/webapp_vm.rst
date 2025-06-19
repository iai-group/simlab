Web Application VM Setup
========================

This guide provides instructions to set up the VM for the web application on Google Cloud Platform (GCP).

Prerequisites
-------------

Before you begin, ensure you have the following:

- A Debian-based Virtual Machine (VM).
- Sudo/root access to the VM.
- Docker installed on the VM. Follow the guide :doc:`docker_installation` to install Docker.
- Conda or Miniconda installed on the VM.

Update and Upgrade the System
-----------------------------

Update the package list and upgrade existing packages:

.. code-block:: bash

    sudo apt update && sudo apt upgrade -y

Start the Web Application
-------------------------

Before starting the web application, you need to execute the following steps:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/iai-group/simlab

2. Navigate to the repository:

   .. code-block:: bash

      cd simlab

3. Create a virtual environment and install the dependencies:

   .. code-block:: bash

    conda create -n myenv python=3.9
    conda activate myenv
    pip install -r requirements.txt

4. Build documentation:

    .. code-block:: bash
    
     pip install -r doc_requirements.txt
     sphinx-build -M html docs/source/ build/
      
5. Add SSL certificates and private key under the directory `nginx/ssl/`, the files should be named `cert.pem` and `privkey.pem` respectively. Otherwise, you need to update the file `nginx/nginx.conf` and `docker-compose.yaml` with the correct file names.
6. Create a `.env` file with the following environment variables in the directory `webapp/backend/`:

   .. code-block:: bash

    FLASK_HOST=
    FLASK_PORT=
    JENKINS_URI=
    JENKINS_USERNAME=
    JENKINS_PASSWORD=
    MONGO_URI=
    DOCKER_BASE_URL=
    DOCKER_REGISTRY_URI=
    DOCKER_USERNAME=
    DOCKER_PASSWORD_FILE=
    DOCKER_REPOSITORY=
    CELERY_BROKER_URL=
    CELERY_RESULT_BACKEND=

7. Create a `.env` file with the following environment variables in the directory `webapp/frontend/`:

   .. code-block:: bash

    REACT_APP_API_URL=

8. Double-check the other environment variables in the file `infrastructure.yaml` and update them if necessary.
9. Start the web application:

   .. code-block:: bash

      docker-compose up -d

10. Verify the web application is running either by accessing the URL `http://<your_vm_external_ip>/` or checking the running containers:

   .. code-block:: bash

      docker container ps

