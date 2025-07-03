Propose new task
================

New tasks can be proposed by the community by following the steps below:

1. **Create a new issue** in the `SimLab repository <https://github.com/iai-group/simlab>`_ with the following information:

    - A brief description of the task
    - A brief description of the domain to which the task belongs and the associated item collection(s)
    - Rationale for adding the task
    - Any relevant references or resources that support the task
    - Any additional information that may be useful for the implementation of the task
    - Tag one maintainer of the repository to review the issue

2. **Implement the task** in your fork of the repository and include unit tests

    - The task should be implemented as a class that inherits from the base class :py:class:`simlab.tasks.task.Task`

3. **Submit a pull request** including:

    - YAML file with the task definition
    - YAML file with the domain definition
    - Link to data collection(s) used in the task if applicable
    - Task implementation
    - Unit tests
    - Documentation updates if necessary
    - Ask for a review from one maintainer of the repository

For now, at least one of SimLab's maintainers should review the proposed tasks and ensure that their implementation follows the guidelines and best practices of the project. Note that the community is also encouraged to participate in the review process and provide feedback on the proposed tasks.