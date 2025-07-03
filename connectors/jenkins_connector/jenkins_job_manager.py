"""Jenkins Job Manager Module.

Manages Jenkins server interactions, including job submission and log
retrieval.
"""

import os
from typing import Optional

import jenkins

# Environment variables for Jenkins configuration
JENKINS_URI = os.environ.get("JENKINS_URI", "http://localhost:8080")
JENKINS_USERNAME = os.environ.get("JENKINS_USERNAME", "")
JENKINS_PASSWORD = os.environ.get("JENKINS_PASSWORD", "")


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
        self.server = jenkins.Jenkins(  # type: ignore[attr-defined]
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

    def submit_job(
        self, run_configuration_path: str, job_name: str = "run_execution"
    ) -> None:
        """Submits a Jenkins job after ensuring it does not exist.

        Args:
            run_configuration_path: Path to run configuration file.
            job_name: Name of the Jenkins job. Defaults to "run_execution".

        Raises:
            RuntimeError: If the job submission fails.
        """
        # Check if the job exists
        if not self.server.job_exists(job_name):
            raise RuntimeError(f"Job '{job_name}' does not exist.")

        params = {
            "CONFIG_FILE_PATH_PARAM": run_configuration_path,
        }

        try:
            # Trigger the job
            self.server.build_job(job_name, params)
            print(f"Job '{job_name}' submitted successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to submit job: {e}")

    def get_build_log(
        self, job_name: str, run_configuration_path: str
    ) -> Optional[str]:
        """Fetches the logs of a Jenkins build.

        Args:
            job_name: Name of the Jenkins job.
            run_configuration_path: Path to run configuration file.

        Returns:
            Logs of the last build with matching configuration file.
        """
        logs = None
        try:
            builds = self.server.get_job_info(job_name).get("builds", [])
            if not builds:
                raise RuntimeError(f"No builds found for job '{job_name}'.")

            for build in builds:
                build_number = build["number"]
                build_info = self.server.get_build_info(job_name, build_number)
                build_params = build_info.get("actions", [{}])[0].get(
                    "parameters", []
                )
                for param in build_params:
                    if (
                        param["name"] == "CONFIG_FILE_PATH_PARAM"
                        and param["value"] == run_configuration_path
                    ):
                        logs = self.server.get_build_console_output(
                            job_name, build_number
                        )
                        return logs
        except Exception as e:
            print(f"Failed to fetch logs: {str(e)}")
        return logs
