# gnocpush

## Development

```bash
virtualenv venv
. venv/bin/activate
pip install --editable .
```

```bash
docker build -t lsstit/gnocpush .
docker push lsstit/gnocpush
```

## Testing with OCI image

```bash
docker run -e GNOC_USERNAME=$GNOC_USERNAME -e GNOC_PASSWORD=$GNOC_PASSWORD -e GNOC_SERVER=$GNOC_SERVER -e GNOC_REALM=$GNOC_REALM --network=host lsstit/gnocpush
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
