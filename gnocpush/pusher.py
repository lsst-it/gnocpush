import logging

from gnocpush.utils import sanitize_severity
from dateutil import parser
from globalnoc_alertmon_agent import AlertMonAgent, Alert

log = logging.getLogger(__name__)

class Pusher:
    def __init__(self, config):
        self.config = config
        self.agent = AlertMonAgent(
            username    = config['username'],
            password    = config['password'],
            server      = config['server'],
            realm       = config['realm']
        )

    def push(self, alerts):
        for alert in alerts:
            data = {
                'node_name': alert['labels'].get('node_name', 'Unknown'),
                'device':  alert['labels'].get('device'),
                'service_name': alert['labels'].get('service_name', 'Unknown'),
                'severity': sanitize_severity(alert['labels'].get('severity', 'Unknown')),
                'description': alert['annotations'].get('description', 'Unknown'),
                'start_time': parser.isoparse(alert['startsAt']).timestamp()
            }

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
