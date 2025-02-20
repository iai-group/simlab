Jenkins Installation on a VM
============================

This guide provides step-by-step instructions for installing Jenkins on a Virtual Machine (VM) running Debian OS.

Prerequisites
-------------

Before you begin, ensure you have the following:

- A Debian-based Virtual Machine (VM).
- Sudo/root access to the VM.
- Docker installed on the VM. Follow the guide :doc:`docker_installation` to install Docker.

Update and Upgrade the System
-----------------------------

Update the package list and upgrade existing packages:

.. code-block:: bash

    sudo apt update && sudo apt upgrade -y

Install Jenkins
---------------

1. Install Java (required for Jenkins):

   .. code-block:: bash

       sudo apt update
       sudo apt install -y openjdk-17-jdk

2. Add Jenkins repository key and source:

   .. code-block:: bash

       curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
       echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

3. Install Jenkins:

   .. code-block:: bash

       sudo apt update
       sudo apt install -y jenkins

4. Start and enable Jenkins:

   .. code-block:: bash

       sudo systemctl start jenkins
       sudo systemctl enable jenkins

5. Verify Jenkins status:

   .. code-block:: bash

       sudo systemctl status jenkins


Configure Jenkins
-----------------

1. Access Jenkins in a web browser:

   - URL: ``http://<your_vm_external_ip>:8080``
   - To get your external IP:

     .. code-block:: bash

         curl ifconfig.me

2. Retrieve the initial admin password:

   .. code-block:: bash

       sudo cat /var/lib/jenkins/secrets/initialAdminPassword

3. Complete Jenkins setup in the browser.


Firewall Configuration in your Cloud provider
---------------------------------------------

Ensure port 8080 (Jenkins) and required Docker ports are open:

1. For GCP Firewall:

   .. code-block:: bash

       gcloud compute firewall-rules create allow-jenkins --allow tcp:8080 --target-tags=jenkins --description="Allow Jenkins traffic"

   Add the tag to your VM:

   .. code-block:: bash

       gcloud compute instances add-tags <your-vm-name> --tags=jenkins --zone=<your-vm-zone>


Verify Installation
-------------------

1. Test Docker functionality:

   .. code-block:: bash

       docker run hello-world

2. Test Jenkins by accessing the URL:

   ``http://<your_vm_external_ip>:8080``

Troubleshooting
---------------

You may encounter the following issue during the installation process:

- Error when adding a firewall rule for Jenkins:

  .. code-block:: bash

      gcloud compute firewall-rules create allow-jenkins --allow tcp:8080 --target-tags=jenkins --description="Allow Jenkins traffic"

      ERROR: (gcloud.compute.firewall-rules.create) Could not fetch resource:
       - Request had insufficient authentication scopes.

To fix this issue, update the authentication scopes by running the following command:

.. code-block:: bash

    gcloud auth login --update-adc