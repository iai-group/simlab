Deployment
==========

This guide provides instructions to deploy the infrastructure on Google Cloud Platform (GCP).

Prerequisites
-------------

- Minimal understanding of GCP
- GCP account with billing enabled
- Project in GCP
- GitHub account

Resources
---------

The infrastructure comprises a set of minimal resources:

- Storage

- Compute Engines

    - Jenkins Server
    - Web Application

- Registry

With these resources, SimLab can be deployed and run on GCP in an idle state; it will accept experiment submissions but not execute them. To enable experiment execution, a cluster of compute engines is required.

Jenkins Server
""""""""""""""

To install Jenkins on a GCP VM, follow the guide :doc:`jenkins_docker_setup`. After the installation, you can customize Jenkins by following the guide :doc:`jenkins_customization`.


.. TODO: Add guide for deploying the web application.

