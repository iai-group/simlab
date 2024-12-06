// Tutorial to submit a run to SimLab

const SubmitRunTutorial = () => {
  return (
    <>
      <h4>Submit a run to SimLab</h4>

      <p>
        A run corresponds to a simulation-based evaluation of a set of
        conversational agents with a set of user simulators with regards to a
        task and metrics. To submit a run to SimLab, you need to provide a
        configuration file that specifies the systems to use, the task, and the
        metrics. The configuration file should be in the JSON format
      </p>

      <p>
        If you want to use your own systems, please make sure to add them to
        SimLab registry first. See the <a>Add a system tutorial</a> for more
        information.
      </p>

      <h4>Run configuration</h4>

      <p>The schema of the run configuration file is as follows:</p>

      <ul>
        <li>
          <p>
            <pre>task</pre> Corresponds to the name of the evaluation task. A
            list of supported tasks can be found in the{" "}
            <a>tasks documentation</a>.
          </p>
        </li>
        <li>
          <p>
            <pre>agents</pre> A list of conversational agents to evaluate. Each
            agent should be specified by its Docker image name.
          </p>
        </li>
        <li>
          <p>
            <pre>user_simulators</pre> A list of user simulators to use. Each
            user simulator should be specified by its Docker image name.
          </p>
        </li>
        <li>
          <p>
            <pre>metrics</pre> A list of metrics to use. Each metric should be
            specified by its name (i.e., the name of the Python class)
          </p>
        </li>
      </ul>

      <h5>Example configuration for CRS task</h5>

      <p>
        The following example configuration file specifies a run for the CRS
        task with two agents and one user simulator:
      </p>

      <pre>{/* TODO: Add example configuration */}</pre>

      <h4>Submit a run</h4>

      <p>
        To submit a run to SimLab, you can use the related form{" "}
        <a href="/experiment">here</a>.
      </p>
    </>
  );
};

export default SubmitRunTutorial;
