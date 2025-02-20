Docker Installation on a VM
===========================

This guide provides instructions to install Docker on a Debian-based Virtual Machine (VM).

Prerequisites
-------------

Before you begin, ensure you have the following:

- A Debian-based Virtual Machine (VM).
- Sudo/root access to the VM.


Update and Upgrade the System
-----------------------------

Update the package list and upgrade existing packages:

.. code-block:: bash

    sudo apt update && sudo apt upgrade -y


Install Docker
--------------

1. Install prerequisites:

   .. code-block:: bash

       sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

2. Add Docker's GPG key and repository:

   .. code-block:: bash

       curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
       echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

3. Install Docker:

   .. code-block:: bash

       sudo apt install -y docker-ce docker-ce-cli containerd.io

4. Verify Docker installation:

   .. code-block:: bash

       docker --version

Troubleshooting
---------------

You may encounter the following issue during the installation process:

- Error when adding Docker's GPG key and repository:

  .. code-block:: bash

      curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

This is likely the output of the command: ``lsb_release -cs``, that is not parsed correctly. To fix this issue, first check the output of the command and then replace it in the command above. 
