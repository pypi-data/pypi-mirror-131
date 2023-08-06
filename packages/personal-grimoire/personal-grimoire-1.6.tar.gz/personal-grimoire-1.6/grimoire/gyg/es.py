import logging
import os

from grimoire.desktop.browser import Browser
from grimoire.desktop.dmenu import Dmenu

LOCATIONS = {
    "es": {"testing10": "https://es7-travelers-search.testing10.gygkube.com"},
}


class EsCli:
    def browser(self):
        return os.system(
            """
                browser "https://es7.gygdev.gygtest.com/_cat/indices"
          """
        )

    def indices(self):
        return os.system(
            """
            curl https://es7.gygdev.gygtest.com/_cat/indices
          """
        )

    def openurl(self, cluster):
        url = "https://es7.gygdev.gygtest.com"

        if cluster == "testing":
            url = LOCATIONS["es"]["testing10"]

        search_uri = "gyg_activity_en_live/_search"

        return os.system(f'browser "{url}/{search_uri}"')

    def getrandomdocs(self, cluster):

        url = "https://es7.gygdev.gygtest.com"

        if cluster == "testing":
            url = LOCATIONS["es"]["testing10"]

        logging.info(f"URL: {url}")
        search_uri = "gyg_activity_en_live/_search"
        return os.system(
            """
            curl -X POST -H "Content-Type: application/json" '%s/%s' -d '{ "query": { "match_all": {} } }'
        """
            % (url, search_uri)
        )

    def follow_indexing_interactive(self, enviroment="testing10"):
        job_id = Dmenu(title="Give job id:").rofi()
        self.follow_indexing(job_id)

    def follow_indexing(self, job_id):
        """
        follows the web web container for the given job
        job_id = sandbox-1203125523538516
        """
        url = f"https://logging.frankfurt1.gygkube.com/app/kibana#/discover?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-13m,to:now))&_a=(columns:!(message.txt),filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:d97605b0-eb37-11e9-a1fb-b7711e994354,key:kubernetes.container_name,negate:!f,params:(query:job-sandbox),type:phrase,value:job-sandbox),query:(match:(kubernetes.container_name:(query:job-sandbox,type:phrase))))),index:d97605b0-eb37-11e9-a1fb-b7711e994354,interval:auto,query:(language:kuery,query:%22{job_id}%22),sort:!(!(_score,desc)))"
        Browser().open(url)
