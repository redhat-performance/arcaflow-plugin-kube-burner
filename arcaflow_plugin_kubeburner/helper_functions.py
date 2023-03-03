import subprocess, os
from kubeburner_schema import ErrorOutput


def safe_open(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')

def readkubeconfig(kubeconfig):
    path="./kubeconfig"
    with safe_open(str(path)) as file:
     file.write(kubeconfig)

def get_prometheus_creds():
    cmd=['oc', 'get', 'route', '-n', 'openshift-monitoring', 'prometheus-k8s', '-o', 'jsonpath="{.spec.host}"' ]
    prom_url= subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    prom_url = prom_url.decode("utf-8")
    prom_url = prom_url.strip('\"')
    prom_url="https://"+prom_url
    prom_token = ''

    try:
        cmd=['oc', 'create', 'token', '-n', 'openshift-monitoring', 'prometheus-k8s', '--duration=6h' ]
        prom_token= subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        prom_token = prom_token.decode("utf-8")
    except subprocess.CalledProcessError as error:
        try:
            cmd=['oc', '-n', 'openshift-monitoring', 'sa', 'new-token', 'prometheus-k8s' ]
            prom_token= subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            prom_token = prom_token.decode("utf-8")
        except subprocess.CalledProcessError as error:
                return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    return prom_url,prom_token




