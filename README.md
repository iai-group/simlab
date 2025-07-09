# SimLab

![Python version](https://img.shields.io/badge/python-3.9-blue)

**Code coverage**

![backend](https://img.shields.io/badge/backend-112%25-brightgreen)
![simlab](https://img.shields.io/badge/simlab-136%25-brightgreen)

This repository contains the code for the SimLab platform. SimLab is a cloud-based platform for benchmarking user simulators and conversational recommender systems. The platform is designed to allow researchers/contributors to easily evaluate their systems (i.e., simulator or conversational recommender) on different tasks.

SimLab is currently deployed at [iai-group.github.io/simlab/](iai-group.github.io/simlab/). 

## Envisioned Features

  * Contributors can upload their system (simulator or conversational recommender) as docker images to the platform's docker registry.
    - The submitted system should implement a REST API that can be used to interact with the system. A template for the API will be provided.
  * Users can create an experiment by submitting a configuration file that specifies the systems to be evaluated and the evaluation task.
  * The platform automatically runs the experiment and provides the results to the user.
  * The platform provides a dashboard for users to visualize the results of their experiments.

## Repository Structure

The repository is structured as follows:

  * `data`: Contains the data files used by the platform.
  * `docs`: Contains the documentation files for the platform.
  * `grafana`: Contains the configuration files for the Grafana dashboard.
  * `jenkins`: Contains the configuration file for the pipeline.
  * `prometheus`: Contains the configuration files for the Prometheus monitoring system.
  * `nginx`: Contains the configuration files for the Nginx reverse proxy.
  * `connectors`: Contains the code base for the external connectors to MongoDB and the Docker registry.
  * `simlab`: Contains the code base to run the experiments and manage the platform.
  * `webapp`: Contains the code base for the web application, it includes the frontend and backend code in folders with the same name.
  * `tests`: Contains the unit tests for the code base and web application.
  * `infrastructure.yaml` and `docker-compose.yaml`: Contains the docker stack configuration for the platform.

## Contributions

We welcome contributions both on the high level (feedback and ideas) as well as on the more technical level (pull requests). See our [contribution guidelines](https://github.com/iai-group/guidelines/blob/main/github/Contribution.md) for more details.

## Citation

If you are using our platform, please cite the following paper:

```
@misc{Bernard:2025:arXiv,
      title={SimLab: A Platform for Simulation-based Evaluation of Conversational Information Access Systems}, 
      author={Nolwenn Bernard and Sharath Chandra Etagi Suresh and Krisztian Balog and ChengXiang Zhai},
      year={2025},
      eprint={2507.04888},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
}
```
