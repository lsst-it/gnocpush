# gnocpush

## Development

```bash
virtualenv venv
. venv/bin/activate
pip install --editable .
```

## Testing gnocgateway with curl

```bash
curl http://localhost:8080/push -v --json @- -u alertmanager:hello < alerts.json
```

## Testing gnocgateway with curl

### without auth

```bash
curl http://localhost:8080/alerts -v --json @- < alerts.json
```

## URLs

### Stage

* https://alertmon-stage.grnoc.iu.edu/alertmon2/
* https://mon-classify-stage.grnoc.iu.edu/monitoring-policy/classify-group/
* https://mon-classify-stage.grnoc.iu.edu/monitoring-policy/alertmon-agent-dashboard/

### Prod

* https://alertmon.grnoc.iu.edu/alertmon2/
* https://mon-classify.grnoc.iu.edu/monitoring-policy/classify-group/
* https://mon-classify.grnoc.iu.edu/monitoring-policy/alertmon-agent-dashboard/
