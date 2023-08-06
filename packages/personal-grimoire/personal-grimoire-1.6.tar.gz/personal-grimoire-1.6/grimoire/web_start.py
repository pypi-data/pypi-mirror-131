from grimoire import s
from grimoire.config import GRIMOIRE_PROJECT_ROOT, Configuration

config = Configuration()


class Api:
    def serve(self):
        s.run(
            f"""cd {GRIMOIRE_PROJECT_ROOT}; \
                DD_SERVICE="grimoire_webservice" DD_ENV="local" DD_LOGS_INJECTION=true\
                DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true \
                ddtrace-run gunicorn --error-logfile - --log-file - --log-level info \
                --reload --timeout 60 \
                --graceful-timeout 65 -w 2 --bind 0.0.0.0:{config.API_PORT} grimoire.web_application:app
            """
        )

    def serve_development(self):
        """
        To customize the port use like this: API_PORT=5008 grimoire api serve_development
        """
        s.run(
            f"""cd {GRIMOIRE_PROJECT_ROOT}; \
                gunicorn --error-logfile - --log-file - --log-level info \
                --reload --timeout 60 \
                --graceful-timeout 65 -w 1 --bind 0.0.0.0:{config.API_PORT} grimoire.web_application:app
            """
        )

    def flask_api(self):
        # s.run(f' (sleep 5; browser "https://app.getpocket.com/") & ')
        s.run(
            f"cd {GRIMOIRE_PROJECT_ROOT}; FLASK_APP=api FLASK_RUN_PORT={config.API_PORT} flask run"
        )
