# gnocpush

A simple service to accept webhook payloads from [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) and to push those alerts on to [GlobalNOC's Alertmon](https://alertmon-stage.grnoc.iu.edu/alertmon2/).

## Alert format

The `gnocpush` input json format is the same as the [Prometheus Alertmanager webhook format](https://prometheus.io/docs/alerting/latest/configuration/#webhook_config).
Labels/annotations are required that match GlocalNOC's required parameter names.

Note that the top level common/group annotations/labels are ignored.

### Required annotations

* `description` - A description of the alert.

### Required labels

* `node_name` - The name of the node that the alert is associated with.
* `service_name` - The name of the service that the alert is associated with.
* `severity` - The severity of the alert. One of: `Critical`, `Major`, `Minor`, `Unknown`, `OK`

### Optional labels

* `device` - The subcomponent of the node that is alarming.
* `start_time` - The time that the alert started.

### Example PrometheusRule

```yaml
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  labels:
    lsst.io/rule: "true"
  name: net
spec:
  groups:
    - name: net.rules
      rules:
        - alert: lhn_interface_up
          annotations:
            description: '{{ $labels.instance }} - {{ $labels.ifName }}|{{ $labels.ifAlias }} is down'
          expr: ifOperStatus{ifAlias=~".*LHN.*"} != 1
          for: 30s
          labels:
            severity: critical
            node_name: '{{ $labels.instance }}'
            device: '{{ $labels.ifName }}'
            service_name: ifInErrors-{{ $labels.ifName}}
            gnoc: "true"
```


### Example Payload

```json
{
  "receiver": "gnocpush",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "ifInErrors",
        "device": "Ethernet17/1",
        "gnoc": "true",
        "ifAlias": "rubinobs-br01 Et17/1 <--SCIENCE #1--> LS-DWDM Linecard001-Port2",
        "ifDescr": "Ethernet17/1",
        "ifIndex": "17001",
        "ifName": "Ethernet17/1",
        "instance": "new-rubinobs-br01",
        "job": "snmp-network",
        "node_name": "new-rubinobs-br01",
        "prom": "dev/ruka",
        "prometheus": "kube-prometheus-stack/kube-prometheus-stack-prometheus",
        "service_name": "ifInErrors-Ethernet17/1",
        "severity": "major",
        "site": "dev"
      },
      "annotations": {
        "description": "new-rubinobs-br01 - Ethernet17/1|rubinobs-br01 Et17/1 <--SCIENCE #1--> LS-DWDM Linecard001-Port2 has 12.2k input errors"
      },
      "startsAt": "2024-04-26T20:46:34.933Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "https://prometheus.example.org/graph?g0.expr=ifInErrors+%3E+1000&g0.tab=1",
      "fingerprint": "46df8c14dbab758c"
    }
  ],
  "groupLabels": {
    "gnoc": "true"
  },
  "commonLabels": {
    "gnoc": "true",
    "job": "snmp-network",
    "prom": "dev/ruka",
    "prometheus": "kube-prometheus-stack/kube-prometheus-stack-prometheus",
    "site": "dev"
  },
  "commonAnnotations": {},
  "externalURL": "https://alertmanager.example.org",
  "version": "4",
  "groupKey": "{}/{gnoc=\"true\"}:{gnoc=\"true\"}",
  "truncatedAlerts": 0
}
```

## Alertmanager Configuration

Note that `gnocpush` does not impose any alert grouping constraints.

```yaml
    config:
      routes:
        - receiver: gnocpush
          continue: true
          repeat_interval: 30s
          group_interval: 30s
          group_wait: 30s
          group_by:
            - gnoc
          matchers:
            - gnoc = "true"
    receivers:
      - name: gnocpush
        webhook_configs:
          - url: http://gnocpush.gnocpush:8080/alerts
```

## Deployment on Kubernetes

```bash
helm upgrade --install \
  gnocpush ./charts/gnocpush \
  --create-namespace --namespace gnocpush \
  -f ./values.yaml
```

### Debugging a Kubernetes Deployment

```bash
k logs alertmanager-kube-prometheus-stack-alertmanager-0 --tail=100 -f

k logs -l app.kubernetes.io/instance=gnocpush -f
```

```bash
k -n gnocpush port-forward gnocpush-dc4d94d8-mqvqq 8080
$ curl localhost:8080/metrics
```

## Development

### Local Development

```bash
virtualenv venv
. venv/bin/activate
pip install --editable .
```

### Testing with the OCI image

```bash
docker run \
  -e GNOC_USERNAME=$GNOC_USERNAME \
  -e GNOC_PASSWORD=$GNOC_PASSWORD \
  -e GNOC_SERVER=$GNOC_SERVER \
  -e GNOC_REALM=$GNOC_REALM \
  --network=host ghcr.io/lsst-it/gnocpush
```

### Testing gnocpush with curl

```bash
curl http://localhost:8080/alerts -v --json @- < alerts.json
```

## Useful GlobalNOC URLs

### Stage

* https://alertmon-stage.grnoc.iu.edu/alertmon2/
* https://mon-classify-stage.grnoc.iu.edu/monitoring-policy/classify-group/
* https://mon-classify-stage.grnoc.iu.edu/monitoring-policy/alertmon-agent-dashboard/

### Prod

* https://alertmon.grnoc.iu.edu/alertmon2/
* https://mon-classify.grnoc.iu.edu/monitoring-policy/classify-group/
* https://mon-classify.grnoc.iu.edu/monitoring-policy/alertmon-agent-dashboard/
