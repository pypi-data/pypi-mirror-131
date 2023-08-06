from grimoire.config import Configuration
from grimoire.git import get_commit_hash

config = Configuration()


class Info:
    PROJECT_ID = "thematic-gift-297917"
    GCLOUD_PROJECT_ID = PROJECT_ID
    LOCAL_IMAGE_NAME = f"grimoire:{get_commit_hash()}"
    APP_NAME = "grimoire-app"
    GCLOUD_CLUSTER_NAME = "grimoire-cluster"
    CLUSTER_NAME = GCLOUD_CLUSTER_NAME
    ECR_NAME_GCLOUD = f"gcr.io/{GCLOUD_PROJECT_ID}/grimoire-app:{get_commit_hash()}"
    ECR_NAME_DOCKER_HUB = f"jeancarlomachado/grimoire:{get_commit_hash()}"
    ECR_NAME_DIGITAL_OCEAN = "registry.digitalocean.com/grimoire/grimoire"
    ECR_NAME = ECR_NAME_GCLOUD
    EMAIL = "personalgrimoire@gmail.com"
    ACCOUNT = EMAIL
    WEBSERVICE_PORT = config.API_PORT
    COMPUTE_ZONE = "europe-west3-a"
