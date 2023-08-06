from grimoire.cicd import Test
from grimoire.cicd.config import Info
from grimoire.config import GRIMOIRE_PROJECT_ROOT
from grimoire.git import get_commit_hash
from grimoire.shell import shell as s

s.enable_exception_on_failure()
s.enable_print_command()


class CICD:
    def __init__(self):
        self.test = Test
        self.info = Info
        self.ecr = ECR()
        self.disable_sdk_inject = False

    def build_and_deploy(self):
        self.debug_system()
        self.build()
        self.ecr.push()
        self.deploy()

    def authenticate(self, disable_sdk_inject=None):
        if disable_sdk_inject != None:
            self.disable_sdk_inject = disable_sdk_inject

        self._run_with_sdk("kubectl config view")

        self._run_with_sdk(
            f"gcloud auth activate-service-account --key-file={GRIMOIRE_PROJECT_ROOT}gcloud_credentials.json"
        )
        self._run_with_sdk("gcloud auth configure-docker --quiet")
        self._run_with_sdk(f"gcloud config set project '{Info.PROJECT_ID}'")
        self._run_with_sdk(f"gcloud config set compute/zone '{Info.COMPUTE_ZONE}'")

        self.get_credentials()
        self._run_with_sdk("gcloud container clusters list")

    def get_credentials(self):
        self._run_with_sdk(
            f"gcloud container clusters get-credentials {Info.CLUSTER_NAME}"
        )

    def _run_with_sdk(self, cmd):
        if self.disable_sdk_inject:
            return s.run(f"{cmd}")

        return s.run(f"{self._append_sdk_to_path()} {cmd}")

    def _append_sdk_to_path(self):
        return 'PATH="$PATH:$(pwd)/google-cloud-sdk/bin"'

    def deploy(self):
        self._run_with_sdk(
            f"kubectl set image deployment/{Info.APP_NAME} {Info.APP_NAME}={Info.ECR_NAME}"
        )

    def debug_system(self) -> None:
        s.run(
            [
                "env",
                "pwd",
                "kubectl config view",
                "gcloud compute instances list",
                "gcloud container clusters list",
                "kubectl config current-context",
            ]
        )

    def build(self):
        s.run(f"docker build . -t {Info.LOCAL_IMAGE_NAME} ", verbose=True)
        self.ecr.tag()

    def deploy_watch(self):
        s.run(f"watch kubectl get pods", verbose=True)

    def browser_web_app(self):
        s.run(f"browser {self.get_public_ip()} ")

    def build_and_run(self):
        self.build()
        self.run()

    def get_current_version(self):
        return get_commit_hash()

    def run(self):
        """
        runs the container locally
        """
        s.run(f"docker run -it {Info.LOCAL_IMAGE_NAME}")

    def shell(self):
        """
        runs the container locally
        """
        s.run(f"docker run -it {Info.LOCAL_IMAGE_NAME} bash")

    def clean(self):
        s.run(f"docker rmi $(docker images |grep '{Info.LOCAL_IMAGE_NAME}')")

    def size(self):
        s.run("docker images | grep -i grimoire")

    def cluster_create(self):
        s.run(f'gcloud container clusters create "{Info.GCLOUD_CLUSTER_NAME}"')

    def deploy_create(self):
        s.run(
            f"kubectl create deployment grimoire-app --image={Info.ECR_NAME}",
            verbose=True,
        )

    def cluster_expose(self):
        s.run(
            f"kubectl expose deployment {Info.APP_NAME} --name={Info.APP_NAME}-service --type=LoadBalancer --port 80 --target-port {Info.WEBSERVICE_PORT}"
        )
        # returns the ip
        return self.get_public_ip()

    def get_public_ip(self):
        return s.run_with_result(
            f"kubectl get service | grep -i {Info.APP_NAME}-service | cut -d ' ' -f10",
            verbose=False,
        )

    def cluster_down(self):
        s.run(
            f'gcloud container clusters resize "{Info.GCLOUD_CLUSTER_NAME}" --num-nodes=0'
        )

    def configure_gcloud(self):
        s.run(f"gcloud auth login")
        s.run(f"gcloud config set project {Info.GCLOUD_PROJECT_ID}")
        s.run(f"gcloud config set compute/zone {Info.COMPUTE_ZONE}")


class ECR:
    def pull(self):
        s.run(
            f"docker pull {Info.ECR_NAME}",
            verbose=True,
        )

    def tag(self):
        s.run(
            f"docker tag {Info.LOCAL_IMAGE_NAME} {Info.ECR_NAME}",
            verbose=True,
        )

    def push(self):
        s.run(
            f"docker push {Info.ECR_NAME}",
            verbose=True,
        )
