Add a new system to SimLab
==========================


All systems (agents and simulators) in SimLab are stored in a Docker registry. To add a new system to SimLab you need to follow the steps below:

1. Implement communication interface for your system

In SimLab, the communication between a conversational agent and user simulator is done over a REST API. This API need to implement the endpoints defined in the template API. 
.. Include link to the template APIs

2. Create a Docker image for your system

Your system should be packaged as a Docker image. The image should include all the necessary dependencies to run the system. For more information on how to create a Docker image, check the `Docker documentation <https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/>`_.
       
The docker image should include labels to specify the type of system, the system's name, and the tasks supported. Other labels to further describe the system are optional. The labels should be added to the Dockerfile as follows:

.. code-block:: Dockerfile

    LABEL type=[agent/simulator]
    LABEL name=[system-name]
    LABEL tasks=[task1,task2, ...]

3. Push the Docker image to the registry

To make your system available in SimLab, you need to push the Docker image to the Docker registry. This requires you to have a SimLab account.

You can use the following command to push the image:

.. code-block:: bash

    docker login [registry-url] -u [username]
    docker push [registry-url]/[username]/[image-name]:[tag]

You can verify that the image has been pushed successfully by running this command:

.. code-block:: bash

    docker pull [registry-url]/[username]/[image-name]:[tag]

If the image has been pushed successfully, you should see the manifest, otherwise, you will see an error message like: "no such manifest: [registry-url]/[username]/[image-name]:[tag]"