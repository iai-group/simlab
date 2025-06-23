Jenkins Job Configuration
=========================

This guide details how to create and configure a Jenkins job that automatically runs the simulation-based evaluation in a virtual machine (VM) provided by GCP.

Prerequisites
-------------

Before you begin, ensure you have the following:

- A Jenkins server running and accessible.
- The Google Compute Engine Plugin installed in Jenkins. Follow the guide :doc:`jenkins_customization` to install and configure the plugin.
- Google storage buckets `simlab_data`and `dialogue_export`. (Note that if you use different names for your buckets, you need to update the pipeline configuration accordingly.)

Custom Image Preparation
------------------------

To facilitate the process, you need to prepare a custom image with pre-installed libraries and tools required to run the simulation-based evaluation. This image serves as a base for the VMs provided by GCP.

1. In GCP, create a new VM instance with the same configuration as the one used for the simulation-based evaluation.

2. SSH into the VM and install the necessary libraries and tools required for the evaluation.

    - Install docker. See the guide on :doc:`docker_installation` for detailed steps.
    - Install Python:

    .. code-block:: bash

        sudo apt update
        sudo apt install python3 python3-pip -y

    - Install Google cloud storage FUSE:

    .. code-block:: bash

        export GCSFUSE_REPO=gcsfuse-$(lsb_release -c -s)
        echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list

        curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

        sudo apt update
        sudo apt install gcsfuse -y

    - Install miniconda:

    .. code-block:: bash

        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh

        sudo chmod +x /tmp/miniconda.sh
        sudo /tmp/miniconda.sh -b -p /opt/miniconda3

        sudo bash -c 'cat > /etc/profile.d/init_conda.sh <<EOF
        #!/bin/bash
        # Initialize Miniconda for all interactive and non-interactive shells
        # Ensure that the conda executable is in the PATH

        if [ -d "/opt/miniconda3" ]; then
        if ! echo "$PATH" | grep -q "/opt/miniconda3/bin"; then
            export PATH="/opt/miniconda3/bin:$PATH"
        fi

        # This makes the 'conda' command and functions like 'activate' available.
        if [ -f "/opt/miniconda3/etc/profile.d/conda.sh" ]; then
            . "/opt/miniconda3/etc/profile.d/conda.sh"
        else
            # Fallback for older conda versions or different installations
            eval "$(CONDA_EXE="/opt/miniconda3/bin/conda" "/opt/miniconda3/bin/conda" shell.bash hook)"
        fi
        fi
        EOF'
        sudo chmod +x /etc/profile.d/init_conda.sh

        /opt/miniconda3/bin/conda config --set auto_activate_base true

        rm /tmp/miniconda.sh

3. Stop the VM instance.
4. Create a custom image from the VM instance:

    - In the GCP Console, navigate to **Compute Engine** > **Images**.
    - Click on **Create Image**.
    - Select the source as the VM instance you just prepared.
    - Name your image (e.g., `simlab-evaluation-image`).
    - Optionally, you can add labels or descriptions for better identification.

Update Cloud Configuration
--------------------------

You need to update the cloud configuration in Jenkins to use the custom image to create new VMs for running the simulation-based evaluation.

1. In Jenkins, navigate to **Manage Jenkins** > **Clouds**.
2. Select the cloud configuration you created for GCP.
3. In the **Instance Configurations** section, update the initial configuration as follows:

    - **Labels**: simlab worker
    - In advanced settings, **Boot Disk** - **Image name**: `simlab-evaluation-image` (or the name you chose for your custom image).

4. Save the changes.

Create Jenkins Pipeline Job
---------------------------

The pipeline job is responsible for running simulation-based evaluation in the VM provided by GCP. In Jenkins, apply the following steps to create the pipeline job:

1. Navigate to **New Item** in Jenkins.
2. Enter a name for the job (e.g., `simlab-evaluation-pipeline`).
3. Select **Pipeline** as the job type.
4. Configure the pipeline as follows:

    - Add a description for the job.
    - Check the **This project is parameterised** option and the string parameter `CONFIG_FILE_PATH_PARAM` with a default value.
    - In the **Triggers** section, check the **Trigger builds remotely** option and set a token that should be defined in the `.env` file of the backend.
    - In the **Pipeline** section, select **Pipeline script from SCM**.
    
        - Choose **Git** as the SCM and provide the repository URL: `https://github.com/iai-group/simlab`.
        - Specify the path to the Jenkinsfile in the repository: `jenkins/Jenkinsfile`.
        - Specify the branch to use.

Jenkins will automatically pull the Jenkinsfile from the specified branch and use it to configure the pipeline.

The Jenkinsfile contains 4 stages:

1. **Partial Clone and Prepare Workspace**: Performs a partial clone of the repository to reduce the amount of data transferred and prepares the workspace for the simulation-based evaluation.
2. **Mount GCP Buckets**: Mounts the Google Cloud Storage buckets `simlab_data` and `dialogue_export` to the VM, allowing access to the necessary data (including the configuration files).
3. **Install Python Requirements**: Installs the required Python packages to run the simulation-based evaluation.
4. **Run Python Main Script**: Executes the main Python script for the simulation-based evaluation using the specified configuration file.

As a post-execution step, the pipeline will automatically unmount the GCP buckets to ensure that the VM is cleaned up after the evaluation is complete.