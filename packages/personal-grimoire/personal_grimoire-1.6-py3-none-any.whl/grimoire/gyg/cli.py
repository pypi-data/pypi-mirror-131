#!/usr/bin/env python
import os

from grimoire import s
from grimoire.gyg.es import EsCli
from grimoire.gyg.fishfarm import FishfarmCli
from grimoire.gyg.url import Url


# add: datadog monitor pull
class GygCli:
    """
    Local cli for local machine
    """

    def __init__(self):
        self.es = EsCli
        self.ff = FishfarmCli
        self.url = Url

    def open_tour(self, tour_id):
        os.system(f'browser "https://www.getyourguide.com/-t{tour_id}"')

    def list_fishfarm_jobs_prod(self):
        os.system(" gygkube job get frankfurt1 fishfarm ")

    def download_search_model(self):
        os.system(
            """
          cd /home/jean/projects/fishfarm;
          gygaws login fishfarm;
          AWS_PROFILE=gygservice-fishfarm aws s3 cp s3://gygdata-shared/derived/search_pipelines/gmv_scores/v1/pipeline_outputs/consolidated_outputs/snapshot/part-00000-tid-4042968808802244732-0c031d2d-c417-49dd-bdfc-3c547e533233-888793-1-c000.csv /home/jean/projects/data/minio/gygdata-shared/derived/search_pipelines/gmv_scores/v1/pipeline_outputs/consolidated_outputs/snapshot/
        """
        )
        return {
            "downloaded_location": "/home/jean/projects/data/minio/gygdata-shared/derived/search_pipelines/gmv_scores/v1/pipeline_outputs/consolidated_outputs/snapshot/"
        }

    def tunnels(self):
        os.system("gygdev tunnel reco web 8080:8080 -d")
        os.system("gygdev tunnel reco db-redis 6379:6379 -d")

    def secrets_s3(self):
        os.systemwith_result(f"runFunction terminal_run '{cmd}'")

        return self.run_without_new_window(cmd)

    def run_without_new_window(self, cmd):
        import redis

        red = redis.StrictRedis(
            host="localhost", port=63795, ssl=True, ssl_cert_reqs=None
        )
        red.ping()
        red.execute_command("INFO")

        return "red is the redis connection object, use C-c to exit"

    def _redis_prod_cli(self):
        """
        does not work with ssl
        """
        s.run(
            """

            redis-cli -h localhost -p 63799
              """
        )

    def redis_prod_tunnel(self):
        s.run(
            """
                sudo ssh -4 -N -i ~/.ssh/id_rsa -L63799:master.reco.hkfgbg.euc1.cache.amazonaws.com:6379 jean@bastion.gyg.io &
            """
        )


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(GygCli).start()
