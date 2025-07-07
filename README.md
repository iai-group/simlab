![backend](https://img.shields.io/badge/backend-112%25-brightgreen)
# SimLab

![Python version](https://img.shields.io/badge/python-3.9-blue)

**Code coverage**

![backend](https://img.shields.io/)
![simlab](https://img.shields.io/badge/simlab-136%25-brightgreen)

This repository contains the code for the SimLab platform. SimLab is a cloud-based platform for benchmarking user simulators and conversational recommender systems. The platform is designed to allow researchers/contributors to easily evaluate their systems (i.e., simulator or conversational recommender) on different tasks.

## Envisioned Features

  * Contributors can upload their system (simulator or conversational recommender) as docker images to the platform's docker registry.
    - The submitted system should implement a REST API that can be used to interact with the system. A template for the API will be provided.
  * Users can create an experiment by submitting a configuration file that specifies the systems to be evaluated, the evaluation task and metrics.
  * The platform automatically runs the experiment and provides the results to the user.
  * The platform provides a dashboard for users to visualize the results of their experiments.

## Repository Structure

The repository is structured as follows:

  * `data`: Contains the data files used by the platform.
  * `grafana`: Contains the configuration files for the Grafana dashboard.
  * `prometheus`: Contains the configuration files for the Prometheus monitoring system.
  * `nginx`: Contains the configuration files for the Nginx reverse proxy.
  * `registry`: Contains the configuration files for the Docker registry and the authentication service.
  * `connectors`: Contains the code base for the external connectors to MongoDB and the Docker registry.
  * `simlab`: Contains the code base to run the experiments and manage the platform.
  * `webapp`: Contains the code base for the web application, it includes the frontend and backend code in folders with the same name.
  * `tests`: Contains the unit tests for the code base and web application.
  * `infrastructure.yaml` and `docker-compose.yaml`: Contains the docker stack configuration for the platform.

## Getting Started

**Prerequisites**

  * Docker
  * Docker Compose
  * SSL certificate and private key should be placed in the folder `nginx/ssl/` with the names `cert.pem` and `privkey.pem` respectively.
  * Build Sphinx documentation with the command `sphinx-build -M html docs/source/ build/`.

**Running SimLab**

To run the platform, execute the following command:

```bash
docker-compose -f docker-compose.yaml up
```

This command will start SimLab and make it available at `https://localhost/`.

*Note*: Think of updating the images if you have made changes to the code base.

## Internal Documentation

The internal documentation for the code base can be found in the `docs` folder.

Steps to generate the internal documentation with Sphinx:

1. Install documentation related requirements:

```bash
pip install -r doc_requirements.txt
```

2. Run the following command to generate the documentation:

```bash
sphinx-build -M html docs/source/ build/
```

The generated documentation will be available in the `build` folder. You can open the `index.html` file in a browser to view the documentation.
