from grimoire import s


class FishfarmCli:
    def __init__(self):
        self.api = FishfarmAPI

    def run_cronjob_from_pod(self):
        return "run_php /var/www/getyourguide.com/current/gyg/gyg/cron_jobs/execute_cron_job_by_slug_k8s.php update_rank_experiments_metrics"

    def shell(self):
        return s.run("gygdev shell fishfarm web")

    def db_tunnel(self):
        s.run("gygdev tunnel fishfarm db-aurora-mysql -d 3308:3306 || true")


class FishfarmAPI:
    def get_location_cards(self, location_id=3224, env="prod"):
        """
        Use like: grimoire gyg ff api get_location_cards | jq '.activities.items[]|.id,.title'
        or
        grimoire gyg ff api get_location_cards 2600 dev | jq '.activities.items[]|.id,.title'
        """
        if env == "dev":
            host = "https://travelers-api.gygdev.gygtest.com"
        else:
            host = "https://travelers-api.getyourguide.com"

        s.run(f"curl '{host}/locations/{location_id}/activity-cards'")
