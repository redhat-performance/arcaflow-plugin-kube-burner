#!/usr/bin/env python3

import sys, os
import typing
from dataclasses import dataclass, field
from arcaflow_plugin_sdk import plugin, validation,schema
from typing import List,Dict
import subprocess
import datetime
import yaml
import time
from kubeburner_schema import KubeBurnerInputParams, WebBurnerInputParams, SuccessOutput, ErrorOutput, kube_burner_output_schema, kube_burner_input_schema,node_density_params,cluster_density_params

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

@plugin.step(
    id="kube-burner",
    name="Kube-Burner Workload",
    description="Kube-burner Workload which stresses the cluster. Creates a single namespace with a number of Deployments",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def RunKubeBurner(params: KubeBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Kube Burner {} Workload ...".format(params.workload))
    
    readkubeconfig(params.kubeconfig)
    os.environ['KUBECONFIG'] = "./kubeconfig"

    serialized_params = kube_burner_input_schema.serialize(params)

    if 'node-density' in params.workload:
        param_list=node_density_params
    else: 
        param_list=cluster_density_params
    
    flags = []
    for param, value in serialized_params.items():
        if param in param_list:
            if '_' in param:
                param = param.replace("_", "-")
            flags.append(f"--{param}={value}")


    try:
        cmd=['./kube-burner', 'ocp', str(params.workload)] + flags 
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    output = process_out.decode("utf-8")

    print("==>> Kube Burner {} Workload complete!".format(params.workload))    
    return "success", SuccessOutput(params.uuid,output)

@plugin.step(
    id="run-web-burner",
    name="Web-Burner Workload",
    description="Web-burner Workload which uses kube-burner templates to create the workload",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def CreateWebBurner(params: WebBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Web Burner {} Workload ...".format(params.workload))
    
    readkubeconfig(params.kubeconfig)
    os.environ['KUBECONFIG'] = "./kubeconfig"
    os.environ['SCALE'] = params.scale_factor
    os.environ['BFD'] = params.bfd_enabled
    prom_url , prom_token = get_prometheus_creds()

    try:
        print("Creating the SPK pods..")
        cmd=['./kube-burner', 'init', '-c', 'workload/cfg_icni2_serving_resource_init.yml', '-t', str(prom_token), '--uuid', '1234' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    time.sleep(60)

    try:
        print("Creating the ICNI2 workload..", params.uuid)
        cmd=['./kube-burner', 'init', '-c', 'workload/'+params.workload_template , '-t', str(prom_token), '--uuid', str(params.uuid), '--prometheus-url', str(prom_url), '-m', 'workload/metrics_full.yaml' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))


    output = process_out.decode("utf-8")

    print("==>> Web Burner {} Workload complete!".format(params.workload))    
    return "success", SuccessOutput(params.uuid,output)

@plugin.step(
    id="delete-web-burner",
    name="Web-Burner Workload",
    description="Web-burner Workload which uses kube-burner templates to delete the workload",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def DeleteWebBurner(params: WebBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Kube Burner {} Workload ...".format(params.workload))
    
    readkubeconfig(params.kubeconfig)
    os.environ['KUBECONFIG'] = "./kubeconfig"
    os.environ['SCALE'] = params.scale_factor
    os.environ['BFD'] = params.bfd_enabled
    prom_url , prom_token = get_prometheus_creds()

    try:
        print("Deleting the ICNI2 workload..")
        cmd=['./kube-burner', 'init', '-c', 'workload/'+params.workload_template , '-t', str(prom_token), '--uuid', str(params.uuid), '--prometheus-url', str(prom_url), '-m', 'workload/metrics_full.yaml' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    time.sleep(60)

    try:
        print("Deleting the SPK pods..", params.uuid)
        cmd=['./kube-burner', 'init', '-c', 'workload/cfg_delete_icni2_serving_resource.yml', '-t', str(prom_token), '--uuid', '1234' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))


    output = process_out.decode("utf-8")

    print("==>> Web Burner {} Workload complete!".format(params.workload))    
    return "success", SuccessOutput(params.uuid,output)



if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                RunKubeBurner,
                CreateWebBurner,
                DeleteWebBurner
            )
        )
    )
