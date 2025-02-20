Jenkins cluster
===============

The Jenkins cluster consists of a master that manages the execution of simulation-based evaluation experiments (jobs) on a set of worker nodes. It dynamically schedules the jobs on the available workers and monitors their execution. Note that the workers are automatically provisioned and deprovisioned by the Jenkins master.

The simulation-based evaluation job consists of four steps:

1. **Prepare the environment**: Install the evaluation framework on the node and instantiate the evaluation tasks, along with the evaluation metrics and information needs.
2. **Evaluation**: For each agent-simulator pair, run the simulation-based evaluation process. That is starting the systems, generating synthetic conversations, and evaluating the performance of the agents.
3. **Results storage**: Store the results of the evaluation in the database and the conversations in the file system.
4. **Cleanup**: Delete the environment.