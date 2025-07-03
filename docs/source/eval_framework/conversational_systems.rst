Conversational Systems
======================

In SimLab, a conversational system is a piece of software dockerized representing either an agent or a user simulator. It is **required** that a conversational system implements a pre-defined API allowing communication with other systems. 

As the conversational systems are docker images, it is the responsibility of its author to maintain the image and push it to a docker registry. Refer to the :doc:`../guides/add_system_to_registry` guide for more information on how to add a new system to SimLab.

Conversation agent
------------------

The conversational agent is responsible for generating responses to the user simulator messages. The definition of the agent API is available `here <conversational_agent_api.html>`_.

It is important to note that the agent is responsible for ending the conversation by sending a message with a dialogue act indicating the EXIT intent. If this ending dialogue act is not sent, a recursion error will occur as both systems will keep sending messages to each other.

You can access the list of available conversational agents in the SimLab registry at: `<https://35.225.189.238/api/agents>`_.

.. TODO: Add a link to the conversational agent starter pack
.. We provide a starter pack to help you create your own conversational agent.

User simulator
--------------

The user simulator is responsible for generating messages to the conversational agent. In a task-oriented scenario, an information need can be given to the user simulator to guide its responses. The definition of the user simulator API is available `here <user_simulator_api.html>`_.

You can access the list of available user simulators in the SimLab registry at: `<https://35.225.189.238/api/simulators>`_.

.. TODO: Add a link to the user simulator starter pack
.. We provide a starter pack to help you create your own user simulator.
