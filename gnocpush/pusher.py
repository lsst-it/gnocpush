import logging

from gnocpush.utils import alertmanager_to_gnoc
from globalnoc_alertmon_agent import AlertMonAgent, Alert

log = logging.getLogger(__name__)


class Pusher:
    def __init__(self, config):
        self.config = config
        self.agent  = AlertMonAgent(
            username = config['username'],
            password = config['password'],
            server   = config['server'],
            realm    = config['realm']
        )

    def push(self, alerts):
        for alert in alerts:
            data = alertmanager_to_gnoc(alert)

            log.debug(f"Pushing alert: {data}")

            self.agent.add_alert(Alert(
                start_time   = data.get('start_time'),
                node_name    = data.get('node_name'),
                device       = data.get('device'),
                service_name = data.get('service_name'),
                description  = data.get('description'),
                severity     = data.get('severity')
            ))

        self.agent.send_alerts()
