import subprocess
import os
import sys
import time
from kubeburner_schema import ErrorOutput


def safe_open(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, "w")


def readkubeconfig(kubeconfig):
    path = "./kubeconfig"
    with safe_open(str(path)) as file:
        file.write(kubeconfig)


def get_prometheus_creds():
    cmd = [
        "oc", "get", "route", "prometheus-k8s",
        "-n", "openshift-monitoring",
        "-o", 'jsonpath="{.spec.host}"',
    ]
    prom_url = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    prom_url = prom_url.decode("utf-8")
    prom_url = prom_url.strip('\"')
    prom_url = "https://" + prom_url
    prom_token = ""

    try:
        cmd = [
            "oc", "create", "token", "prometheus-k8s",
            "-n", "openshift-monitoring", "--duration=6h",
        ]
        prom_token = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        prom_token = prom_token.decode("utf-8")
    except subprocess.CalledProcessError:
        try:
            cmd = [
                "oc", "sa", "new-token", "prometheus-k8s",
                "-n", "openshift-monitoring",
            ]
            prom_token = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            prom_token = prom_token.decode("utf-8")
        except subprocess.CalledProcessError as error:
            return "error", ErrorOutput(
                error.returncode,
                "{} failed with return code {}:\n{}".format(
                    error.cmd[0], error.returncode, error.output
                ),
            )

    return prom_url, prom_token


def calculate_normal_limit_count(cluster_size):
    count = (35 * cluster_size) // 120
    return count


def create_kubeconfig_secret():
    cmd = [
        'oc', 'create', 'secret', 'generic',
        'kubeconfig', '--from-file=kubeconfig',
        '--dry-run=client', '--output=yaml'
    ]
    secret = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    secret = secret.decode("utf-8")
    sys.stdout = open('objectTemplates/secret_kubeconfig.yml', 'w')
    print(secret)

    time.sleep(10)
