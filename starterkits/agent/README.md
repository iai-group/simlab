# Conversational Agent Starter Kit

This starter kit provides a template to create a compatible conversational agent and its associated image for SimLab.

## Structure

The starter kit is organized as follows:

  * `Dockerfile.temp`: A template with placeholders to build the agent's Docker image.
  * `src/`: Provides templates with placeholder implementation for the communication API. The different templates correspond to different languages and frameworks.
    - `src/api_template_flask.py`: A template for a Flask-based API.
    - `src/api_template_fastapi.py`: A template for a FastAPI-based API.

## Getting Started

**Prerequisites:**

  * Familiarity with the communication API of SimLab. See the [specification](https://github.com/iai-group/simlab/blob/main/docs/source/eval_framework/specs/conv_agent_api.yaml) for details.
  * Basic knowledge of Docker and how to build Docker images.

To create a new conversational agent, you need to:

1. **Create a new repository**.
2. **Copy the starter kit** into your new repository.

Then you can start the implementation of your agent by modifying the templates in the `src/` directory and the `Dockerfile.temp`. Explanations on how to proceed are provided in the following sections.

## Implementation

### Communication API

In `src/`, you will find templates for the communication API in different languages and frameworks. You can choose the one that best fits your needs and preferences. The templates include placeholders and comments to guide you through the implementation process.

Placeholders in the templates include:

  * Implementation of the logic to handle the reception and response to incoming user messages in `receive_message()`. Note that the different elements of the response are set to `None` by default and should be replaced with the actual implementation.
  * Implementation of the logic to validate the agent's configuration in `configure()`. That is, making sure that the `agent_id` and `parameters` are valid and that the agent can be configured with the provided parameters.
  * Implementation of the logic to configure the agent based on the provided parameters in `configure()`.

### Dockerfile

Start by renaming the `Dockerfile.temp` to `Dockerfile`. Then, you can edit the file based on the different placeholders and comments provided in the file. Please note that additional modifications may be required to adapt the Dockerfile to your specific agent's requirements.

In its current state, the template provides the list of labels required by SimLab, as well as commands to copy the source code and expose the port used by the communication API.

Placeholders in the Dockerfile include:

  * `<base_image>`: The base image to use for your agent. You can choose a base image that fits your needs, such as `python:3.9-slim` or `ubuntu:20.04`.
  * Labels to provide metadata about your agent, such as:
    - `<agent_name>`
    - `<agent_description>`
    - `<author_name>`
    - `<version_number>`
    - `<tag>`
  * Commands to install the necessary dependencies for your agent, such as:
    - `pip install -r requirements.txt` for Python-based agents.
    - `apt-get install -y <package>` for system-level dependencies.
  * Commands to copy files required to run your agent, such as:
    - `COPY data/ data/` to copy data files.
    - `COPY configuration.yaml configuration.yaml` to copy configuration files.
  * Command to run your agent, such as:
    - `CMD ["python", "src/api_template_flask.py"]` for a Flask-based agent.

## Docker Image

You can build the Docker image for your agent using the following command from the root of your repository:

```bash
docker build -t [username]/[name]:[tag] .
```

Then, you can create the archive for your agent using the following command:

```bash
docker save [username]/[name]:[tag] | gzip > [archive-name].tar.gz
```

Replace `[username]`, `[name]`, and `[tag]` with your SimLab username, the name of your agent, and the tag of the image, respectively.
