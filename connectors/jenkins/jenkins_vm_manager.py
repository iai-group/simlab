import jenkins
import os
# from google.cloud import compute_v1

JENKINS_URI = os.environ.get("JENKINS_URI", "http://localhost:8080")
JENKINS_USERNAME = os.environ.get("JENKINS_USERNAME", "")
JENKINS_PASSWORD = os.environ.get("JENKINS_PASSWORD", "")

class JenkinsVMManager:
    # GCP configuration
    GCP_PROJECT = 'my-gcp-project'
    GCP_ZONE = 'us-central1-a'
    GCP_MACHINE_TYPE = 'n2-standard-2'
    GCP_IMAGE_PROJECT = 'debian-cloud'
    GCP_IMAGE_FAMILY = 'debian-10'

    # VM Limits
    MIN_WORKERS = 6
    MAX_WORKERS = 12

    def __init__(self):
        self.server = jenkins.Jenkins(JENKINS_URI, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        # self.gcp_client = compute_v1.InstancesClient()

    def check_jenkins_connection(self):
        try:
            user = self.server.get_whoami()
            version = self.server.get_version()
            print(f'Connected to Jenkins {version} as {user["fullName"]}')
        except Exception as e:
            print(f'Failed to connect to Jenkins: {str(e)}')

    # def launch_gcp_instances(self, count):
    #     count = max(self.MIN_WORKERS, min(count, self.MAX_WORKERS))
    #     instance_ids = []
    #     for i in range(count):
    #         instance = compute_v1.Instance()
    #         instance.name = f'worker-vm-{i}'
    #         instance.machine_type = f'zones/{self.GCP_ZONE}/machineTypes/{self.GCP_MACHINE_TYPE}'

    #         disk = compute_v1.AttachedDisk()
    #         disk.auto_delete = True
    #         disk.boot = True
    #         disk.initialize_params.source_image = f'projects/{self.GCP_IMAGE_PROJECT}/global/images/family/{self.GCP_IMAGE_FAMILY}'
    #         instance.disks = [disk]

    #         network_interface = compute_v1.NetworkInterface()
    #         network_interface.name = 'default'
    #         instance.network_interfaces = [network_interface]

    #         operation = self.gcp_client.insert(
    #             project=self.GCP_PROJECT, zone=self.GCP_ZONE, instance_resource=instance
    #         )
    #         instance_ids.append(instance.name)
    #     return instance_ids

    def setup_worker_vm(self, instance_ip, git_url):
        setup_script = f'''
        #!/bin/bash
        sudo apt-get update
        sudo apt-get install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        git clone {git_url}
        cd $(basename {git_url} .git)
        docker build -t evaluation-image .
        docker run evaluation-image
        '''
        with open('setup_worker.sh', 'w') as f:
            f.write(setup_script)

        os.system(f'scp setup_worker.sh ubuntu@{instance_ip}:/home/ubuntu/')
        os.system(f'ssh ubuntu@{instance_ip} "bash /home/ubuntu/setup_worker.sh"')

    def submit_job(self, job_name, git_url):
        job_config = self._generate_job_config(git_url)
        try:
            if not self.server.job_exists(job_name):
                self.server.create_job(job_name, job_config)
            self.server.build_job(job_name)
            print(f'Job {job_name} submitted successfully.')
        except Exception as e:
            print(f'Failed to submit job: {str(e)}')

    def _generate_job_config(self, git_url):
        return f'''
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
'''

    def get_job_logs(self, job_name):
        try:
            build_number = self.server.get_job_info(job_name)['lastBuild']['number']
            logs = self.server.get_build_console_output(job_name, build_number)
            return logs
        except Exception as e:
            print(f'Failed to fetch logs: {str(e)}')
            return None
