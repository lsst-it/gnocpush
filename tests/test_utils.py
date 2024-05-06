#!/usr/bin/env python3

import pytest

from gnocpush.utils import sanitize_severity, alertmanager_to_gnoc


@pytest.mark.sanitize_severity
def test_critical():
    words = ["critical", "CRITICAL", "cRiTiCaL", "Critical"]
    for word in words:
        assert sanitize_severity(word) == 'Critical'


def test_major():
    words = ["major", "MAJOR", "mAjOr", "Major"]
    for word in words:
        assert sanitize_severity(word) == 'Major'


def test_minor():
    words = ["minor", "MINOR", "mInOr", "Minor"]
    for word in words:
        assert sanitize_severity(word) == 'Minor'


def test_unknown():
    words = [
        "unknown",
        "UNKNOWN",
        "uNkNoWn",
        "Unknown",
        "foo",
        "bar",
        "baz",
    ]
    for word in words:
        assert sanitize_severity(word) == 'Unknown'


def test_ok():
    words = ["ok", "OK", "oK", "Ok"]
    for word in words:
        assert sanitize_severity(word) == 'OK'


@pytest.mark.alertmanager_to_gnoc
def test_alertmanager_to_gnoc():
    alertmanager_alert = {
        "status": "firing",
        "labels": {
            "alertname": "bogus_critical",
            "device": "faux",
            "gnoc": "true",
            "ifDescr": "Ethernet26",
            "ifIndex": "26",
            "ifName": "Ethernet26",
            "instance": "bdc-b05-lf1",
            "job": "snmp-network",
            "node_name": "bogus_critical",
            "prom": "dev/ruka",
            "prometheus": "kube-prometheus-stack/kube-prometheus-stack-prometheus",  # noqa
            "service_name": "bogons",
            "severity": "Critical",
            "site": "dev"
        },
        "annotations": {
            "description": "Bogus Critical alert"
        },
        "startsAt": "2024-05-06T03:09:33.464Z",
        "endsAt": "0001-01-01T00:00:00Z",
        "generatorURL": "https://ruka.example.org/graph?g0.expr=ifOperStatus%7BifName%3D%22Ethernet26%22%2Cinstance%3D%22bdc-b05-lf1%22%7D+%21%3D+1&g0.tab=1",  # noqa
        "fingerprint": "b6b655ae6855c5ae"
    }

    gnoc_alert = {
        'node_name': 'bogus_critical',
        'device': 'faux',
        'service_name': 'bogons',
        'severity': 'Critical',
        'description': 'Bogus Critical alert',
        'start_time': 1714964973,
    }

    assert alertmanager_to_gnoc(alertmanager_alert) == gnoc_alert
