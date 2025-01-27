==============================================================
Jenkins Plugin Customization for GCP
==============================================================

This guide provides steps to install and configure the Google Compute Engine Plugin for Jenkins.

SSH into the VM and login to Jenkins before the below steps.

Install GCP Plugin
-------------------

1. Navigate to **Manage Jenkins**:
   - Open your Jenkins dashboard.
   - Click on **Manage Jenkins** from the left-hand menu.

2. Access the Plugin Manager:
   - Click on **Manage Plugins**.

3. Search for the Plugin:
   - Go to the **Available Plugins** tab.
   - In the search bar, type **Google Compute Engine Plugin**.

4. Verify the Plugin:
   - Ensure the plugin matches the official documentation:
    `Google Compute Engine Plugin <https://plugins.jenkins.io/google-compute-engine/>`_

5. Install the Plugin:
   - Check the box next to the plugin.
   - Click **Install without restart** or **Install and restart Jenkins** if needed.


Add Cloud Configuration
------------------------

1. Access Cloud Configuration:
   - In Jenkins, go to **Manage Jenkins**.
   - Select **Configure System**.

2. Follow the Official Guide:
   - Refer to the detailed guide for configuring the cloud and setting up a service account:
    `Google Compute Engine Plugin Configuration Guide <https://github.com/jenkinsci/google-compute-engine-plugin/blob/develop/docs/Home.md>`_

3. Steps in the Guide:
   - Create a Google Cloud service account.
   - Provide necessary permissions for the service account.
   - Add the service account credentials to Jenkins.
   - Configure the Google Compute Engine cloud in Jenkins.


Conclusion
----------

You have successfully installed and configured the Google Compute Engine Plugin for Jenkins. This integration allows Jenkins to manage Google Cloud resources efficiently for CI/CD pipelines.
