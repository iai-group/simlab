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
- `gcsfuse` installed on the VM to mount Google Cloud Storage (GCS) buckets. See `official documentation <https://cloud.google.com/storage/docs/cloud-storage-fuse/install>`_ for installation instructions.

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
    GCS_BUCKET_NAME=
    GOOGLE_APPLICATION_CREDENTIALS=
    
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

Mount GCS Bucket
----------------

Before mounting the GCS bucket, ensure that you have the right access permissions. That is, the service account used by the VM should have access to the GCS bucket and the VM should have full access to the *Storage* API. After, you can mount the GCS bucket used the commands below:

.. code-block:: bash

   MOUNT_DIR=<your-mount-directory>  # e.g., /mnt/simlab_data_mount

   sudo mkdir -p "${MOUNT_DIR}"      
   sudo chown -R $(whoami):$(id -gn) "${MOUNT_DIR}" 

   BUCKET_NAME=<your-bucket-name>  # e.g., simlab_data
   gcsfuse --file-mode=664 --dir-mode=775 --implicit-dirs "${BUCKET_NAME}" "${MOUNT_DIR}"

Note that this bucket stores data from the `data` directory of the repository.

Firewall Configuration in your Cloud provider
---------------------------------------------

Ensure that the ports used by Mongo DB (i.e. 27017) is open internally for the other services to communicate with it.

1. For GCP Firewall:

   .. code-block:: bash

      gcloud compute firewall-rules create allow-mongodb --allow tcp:27017 --target-tags=mongodb --description="Allow access to MongoDB" --source-ranges=<your_vm_internal_ip>/32

   Add the tag to your VM:

   .. code-block:: bash

      gcloud compute instances add-tags <your-vm-name> --tags=mongodb --zone=<your-vm-zone>