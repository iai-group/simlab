Add a new system to SimLab
==========================


All systems (agents and simulators) in SimLab are stored in a Docker registry. To add a new system to SimLab you need to follow the steps below:

1. Implement communication interface for your system

In SimLab, the communication between a conversational agent and user simulator is done over a REST API. This API need to implement the endpoints defined in the template API. See the API specifications for the `agent <../simlab/conversational_agent_api.html>`_ and `simulator <../simlab/user_simulator_api.html>`_ for more information on the endpoints and data formats.

2. Create a Docker image for your system

Your system should be packaged as a Docker image. The image should include all the necessary dependencies to run the system. The naming convention for the Docker image is as follows: [username]/[image-name]:[tag]; where [username] is your SimLab username, [image-name] is the name of the image, and [tag] is the version of the image.
For more information on how to create a Docker image, check the `Docker documentation <https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/>`_.
       
The docker image should include labels to specify the type of system, the system's name, a brief description of the system, and the port number on which the API is running. Other labels to further describe the system are optional. The following labels should be added to the Dockerfile:

.. code-block:: Dockerfile

    LABEL type=[agent/simulator]    # Specify the type of the system
    LABEL name=[system-name]        # Specify the name of the system
    LABEL description=[description] # Specify a brief description of the system
    LABEL port=[port-number]        # Specify the port number on which the API is running

3. Create an archive of your Docker image

You can use the following command to create an archive of your Docker image:

.. code-block:: bash

    docker save [username]/[image-name]:[tag] | gzip > [image-name].tar

4. Submit the archive to SimLab

To add your image to SimLab's registry, login to the SimLab web interface and navigate to the `"Systems" page <https://35.222.6.112/system>`_. Click on the button "ADD NEW SYSTEM", fill in the form with your archive file and the image name before submitting the form. Be aware that the upload process may take a few minutes depending on the size of the image.

Once the upload is complete, your system will be added to the registry and will be available for use in SimLab. If you cannot find your system in the list of available systems, try refreshing the page after a few minutes.
