Task
====

A task represents the simulation-based evaluation of conversational agents, such as conversational recommender or conversational search systems. A task is defined by different elements:

- A name that identifies the task.
- A description that explains the purpose of the task.
- A domain that specifies the context in which the task is defined. See domain documentation for more information.
- A list of metrics that are used to evaluate the performance of the agents on the task. See metric documentation for more information.
- A list of information needs that are used to generate synthetic conversations for each agent to evaluate. See information need documentation for more information.

The task class, :py:class:`simlab.tasks.task.Task`, is designed to be generic and flexible to support a wide range of evaluation scenarios. New tasks may be added to SimLab by inheriting from this class and implementing the additional functionalities required for the specific evaluation scenario.
