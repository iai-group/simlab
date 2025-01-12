"""Jenkins Job Manager Module.

Manages Jenkins server connections and job submissions.
"""

import os
import jenkins

# Environment variables for Jenkins configuration
JENKINS_URI = os.environ.get("JENKINS_URI", "http://localhost:8080")
JENKINS_USERNAME = os.environ.get("JENKINS_USERNAME", "")
JENKINS_PASSWORD = os.environ.get("JENKINS_PASSWORD", "")


class JenkinsJobManager:
    """Manages Jenkins server interactions, including job submission and log retrieval."""

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
        self.server = jenkins.Jenkins(jenkins_uri, username=username, password=password)

    def check_jenkins_connection(self) -> None:
        """Checks the connection to the Jenkins server."""
        try:
            user = self.server.get_whoami()
            version = self.server.get_version()
            print(f"Connected to Jenkins {version} as {user['fullName']}")
        except Exception as e:
            print(f"Failed to connect to Jenkins: {str(e)}")

    def submit_job(
        self,
        job_name: str,
        git_url: str
    ) -> None:
        """Submits a Jenkins job after ensuring it does not exist.

        Args:
            job_name: Name of the Jenkins job.
            git_url: URL of the Git repository to clone.
        """
        try:
            job_config = self._generate_job_config(git_url)
            
            # Check if the job exists; create it if not
            if not self.server.job_exists(job_name):
                self.server.create_job(job_name, job_config)
            # Trigger the job
            self.server.build_job(job_name)
            print(f"Job '{job_name}' submitted successfully.")
        except Exception as e:
            print(f"Failed to submit job: {str(e)}")

    def _generate_job_config(self, git_url: str) -> str:
        """Generates a Jenkins job configuration.

        Args:
            git_url: URL of the Git repository to clone.

        Returns:
            A string representing the Jenkins job configuration XML.
        """
        return f"""
<project>
    <builders>
        <hudson.tasks.Shell>
            <command>
                git clone {git_url}
                cd $(basename {git_url} .git)
                docker build -t evaluation-image .
                docker run evaluation-image
            </command>
        </hudson.tasks.Shell>
    </builders>
</project>
"""

    def get_job_logs(self, job_name: str) -> str | None:
        """Fetches the logs of a Jenkins job.

        Args:
            job_name: Name of the Jenkins job.

        Returns:
            Logs of the last build of the job, or None if an error occurs.
        """
        try:
            build_number = self.server.get_job_info(job_name)["lastBuild"]["number"]
            logs = self.server.get_build_console_output(job_name, build_number)
            return logs
        except Exception as e:
            print(f"Failed to fetch logs: {str(e)}")
            return None
