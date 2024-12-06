// Tutorial to add a new system to SimLab registry

const AddSystemTutorial = () => {
  return (
    <>
      <h3>Add a new system to SimLab</h3>

      <p>
        All systems (agents and simulators) in SimLab are stored in a Docker
        registry. To add a new system to SimLab you need to follow the steps
        below:
      </p>

      <h4>Implement communication interface for your system</h4>

      <p>
        In SimLab, the communication between a conversational agent and user
        simulator is done over a REST API. This API need to implement the
        endpoints defined in the template API. The template APIs are available
        here.
      </p>

      <h4>Create a Docker image for your system</h4>

      <p>
        Your system should be packaged as a Docker image. The image should
        include all the necessary dependencies to run the system. For more
        information on how to create a Docker image, check the{" "}
        <a href="https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/">
          Docker documentation
        </a>
        .
      </p>

      <p>
        The docker image should include labels to specify the type of system,
        the system's name, and the tasks supported. Other labels to further
        describe the system are optional. The labels should be added to the
        Dockerfile as follows:
        <pre>LABEL type=[agent/simulator]</pre>
        <pre>LABEL name=[system-name]</pre>
        <pre>LABEL tasks=[task1,task2, ...]</pre>
      </p>

      <h4>Push the Docker image to the Docker registry</h4>

      <p>
        To make your system available in SimLab, you need to push the Docker
        image to the Docker registry. This requires you to have a SimLab
        account.
      </p>

      <p>
        You can use the following command to push the image:
        <pre>docker login [registry-url] -u [username]</pre>
        <pre>docker push [registry-url]/[username]/[image-name]</pre>
      </p>

      <p>
        You can verify that the image has been pushed successfully by running
        this command:
        <pre>
          docker manifest inspect [registry-url]/[username]/[image-name]
        </pre>
      </p>
      <p>
        If the image has been pushed successfully, you should see the manifest,
        otherwise, you will see an error message like:
        <pre>no such manifest: [registry-url]/[username]/[image-name]</pre>
      </p>
    </>
  );
};

export default AddSystemTutorial;
