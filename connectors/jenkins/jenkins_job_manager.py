"""Jenkins Job Manager Module.

Manages Jenkins server interactions, including job submission and log retrieval.
"""

import os

import jenkins

import xml.etree.ElementTree as ET
from typing import Union


CONFIG_FILE_PATH = "data/jenkins/run_execution/config.xml"
# Environment variables for Jenkins configuration
JENKINS_URI = os.environ.get("JENKINS_URI", "http://localhost:8080")
JENKINS_USERNAME = os.environ.get("JENKINS_USERNAME", "")
JENKINS_PASSWORD = os.environ.get("JENKINS_PASSWORD", "")
# Environment variables for Docker Registry
DOCKER_REGISTRY_URI = os.environ.get("DOCKER_REGISTRY_URI", "")
DOCKER_REGISTRY_USER = os.environ.get("DOCKER_REGISTRY_USER", "")
DOCKER_REGISTRY_PASSWORD = os.environ.get("DOCKER_REGISTRY_PASSWORD", "")


class JenkinsJobManager:
    def __init__(
        self,
        jenkins_uri: str = JENKINS_URI,
        username: str = JENKINS_USERNAME,
        password: str = JENKINS_PASSWORD,
    ) -> None:
        """Initializes the Jenkins VM Manager.

        Args:
            jenkins_uri: Jenkins server URI. Defaults to JENKINS_URI.
            username: Jenkins admin username. Defaults to JENKINS_USERNAME.
            password: Jenkins admin password. Defaults to JENKINS_PASSWORD.
        """
        super().__init__()
        self.server = jenkins.Jenkins(
            jenkins_uri, username=username, password=password
        )

    def check_jenkins_connection(self) -> None:
        """Checks the connection to the Jenkins server."""
        try:
            user = self.server.get_whoami()
            version = self.server.get_version()
            print(f"Connected to Jenkins {version} as {user['fullName']}")
        except Exception as e:
            print(f"Failed to connect to Jenkins: {str(e)}")

    def submit_job(self, job_name: str, run_configuration_path: str) -> None:
        """Submits a Jenkins job after ensuring it does not exist.

        Args:
            job_name: Name of the Jenkins job.
            run_configuration_path: Path of the run configuration file.
        
        Raises:
            RuntimeError: If the job creation or building fails.
        """
        try:
            # Check if the job exists; create it if not
            if not self.server.job_exists(job_name):
                job_config = self._generate_job_config(run_configuration_path)
                self.server.create_job(job_name, job_config)
            # Trigger the job
            self.server.build_job(job_name)
            print(f"Job '{job_name}' submitted successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to submit job: {e}")

    def _generate_job_config(self, run_configuration_path: str) -> str:
        """Generates a Jenkins job configuration.

        Args:
            run_configuration_path: Path of the run configuration file.

        Returns:
            A string representing the Jenkins job configuration XML.
        """
        # TODO: Update the git credentails needed in the config.xml file
        try:
            tree = ET.parse(CONFIG_FILE_PATH)
            root = tree.getroot()

            # Locate and update variables
            for parameter in root.findall(".//hudson.model.StringParameterDefinition"):
                name = parameter.find("name")
                if name is not None and name.text == "REGISTRY_URL":
                    default_value = parameter.find("defaultValue")
                    if default_value is not None:
                        default_value.text = DOCKER_REGISTRY_URI
                if name is not None and name.text == "REGISTRY_USERNAME":
                    default_value = parameter.find("defaultValue")
                    if default_value is not None:
                        default_value.text = DOCKER_REGISTRY_USER
                if name is not None and name.text == "REGISTRY_PASSWORD":
                    default_value = parameter.find("defaultValue")
                    if default_value is not None:
                        default_value.text = DOCKER_REGISTRY_PASSWORD
                if name is not None and name.text == "CONFIG_FILE":
                    default_value = parameter.find("defaultValue")
                    if default_value is not None:
                        default_value.text = run_configuration_path

            # Convert back to a string and return the modified XML content
            return ET.tostring(root, encoding="unicode")
        except Exception as e:
            raise RuntimeError(f"Failed to load or modify config.xml: {e}")

    def get_job_logs(self, job_name: str) -> Union[str, None]:
        """Fetches the logs of a Jenkins job.

        Args:
            job_name: Name of the Jenkins job.

        Returns:
            Logs of the last build of the job, or None if an error occurs.
        """
        try:
            build_number = self.server.get_job_info(job_name)["lastBuild"][
                "number"
            ]
            logs = self.server.get_build_console_output(job_name, build_number)
            return logs
        except Exception as e:
            print(f"Failed to fetch logs: {str(e)}")
            return None
