Metric
======

A metric is a **quantitative** measure that is used to evaluate a conversation between a conversational agent and a user simulator. The overall performance of a conversational agent with regards to the metric is computed by aggregating the scores of the conversations between the agent and user simulator.

The metric class, :py:class:`simlab.metrics.metric.Metric`, is designed to be generic and flexible to support a wide range of evaluation scenarios. New metrics may be added to SimLab by inheriting from this class and implementing the additional functionalities required for the specific evaluation scenario.

.. TODO: Update link to production URL
A list of supported metrics is available at: `<https://localhost/api/metrics>`_.