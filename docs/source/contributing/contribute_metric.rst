Propose new metric
==================

Everyone is welcome to propose new metrics to be added to SimLab by following the steps below:

1. **Create a new issue** in the `SimLab repository <https://github.com/iai-group/simlab>`_ with the following information:
   - A brief description of the metric
   - Rationale for adding the metric
   - Any relevant references or resources that support the metric
   - Any additional information that may be useful for the implementation of the metric
   - Tag one maintainer of the repository to review the issue
2. **Implement the metric** in your fork of the repository and include unit tests
   - The metric should be implemented as a class that inherits from the base class :py:class:`simlab.metrics.metric.Metric`
3. **Submit a pull request** including:
    - YAML file with the metric definition
    - Metric implementation
    - Unit tests
    - Documentation updates if necessary
    - Ask for a review from one maintainer of the repository

The maintainers of SimLab are responsible for reviewing the proposed metrics and ensuring that their implementation follows the guidelines and best practices of the project. Note that the community is also encouraged to participate in the review process and provide feedback on the proposed metrics.