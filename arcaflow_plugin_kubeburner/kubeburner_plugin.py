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
from kubeburner_schema import KubeBurnerInputParams, WebBurnerInputParams, SuccessOutput, ErrorOutput, output_schema, kube_burner_input_schema, web_burner_input_schema ,node_density_params,cluster_density_params, node_density_cni_params, node_density_heavy_params
from helper_functions import get_prometheus_creds, safe_open, readkubeconfig, calculate_normal_limit_count

@plugin.step(
    id="kube-burner",
    name="Kube-Burner Workload",
    description="Kube-burner Workloads: node-density, node-density-cni, node-density-heavy, cluster-density, cluster-density-v2",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def RunKubeBurner(params: KubeBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Kube Burner {} Workload ...".format(params.workload))
    
    readkubeconfig(params.kubeconfig)
    os.environ['KUBECONFIG'] = "./kubeconfig"

    serialized_params = kube_burner_input_schema.serialize(params)

    if params.workload == "node-density":
        param_list=node_density_params
    elif params.workload == "node-density-cni":
        param_list=node_density_cni_params
    elif params.workload == "node-density-heavy":
        param_list=node_density_heavy_params
    elif "cluster-density" in params.workload:
        param_list=cluster_density_params
    else: 
        param_list= ['--help']
    
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
def RunWebBurner(params: WebBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Web Burner {} Workload ...".format(params.workload_template))
    
    readkubeconfig(params.kubeconfig)
    os.environ['KUBECONFIG'] = "./kubeconfig"
    os.environ['SCALE'] = str(params.scale_factor)  #exporting these vars as they are read by the kube-burner templates
    os.environ['BFD'] = params.bfd_enabled
    os.environ['QPS'] = str(params.qps)
    os.environ['BURST'] = str(params.burst)
    os.environ['INDEXING'] = params.indexing
    os.environ['NORMAL_LIMIT_COUNT'] = str(calculate_normal_limit_count(params.number_of_nodes))
    prom_url , prom_token = get_prometheus_creds()

    try:
        print("Creating the SPK pods..")
        cmd=['./kube-burner-0.14.2', 'init', '-c', 'workload/cfg_icni2_serving_resource_init.yml', '-t', str(prom_token), '--uuid', '1234' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    print("Pausing for a minute..")
    time.sleep(60)

    try:
        print("Creating the ICNI2 workload..", params.uuid)
        cmd=['./kube-burner-0.14.2', 'init', '-c', 'workload/'+params.workload_template , '-t', str(prom_token), '--uuid', str(params.uuid), '--prometheus-url', str(prom_url), '-m', 'workload/metrics_full.yaml' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))


    output = process_out.decode("utf-8")

    print("==>> Web Burner {} Workload complete!".format(params.workload_template))    
    return "success", SuccessOutput(params.uuid,output)

@plugin.step(
    id="delete-web-burner",
    name="Web-Burner Workload",
    description="Web-burner Workload which uses kube-burner templates to delete the workload",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def DeleteWebBurner(params: WebBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Kube Burner {} Workload ...".format(params.workload_template))
    
    readkubeconfig(params.kubeconfig)
    os.environ['KUBECONFIG'] = "./kubeconfig"
    os.environ['SCALE'] = str(params.scale_factor)
    os.environ['BFD'] = params.bfd_enabled
    os.environ['QPS'] = str(params.qps)
    os.environ['BURST'] = str(params.burst)
    prom_url , prom_token = get_prometheus_creds()

    try:
        print("Deleting the ICNI2 workload..")
        cmd=['./kube-burner-0.14.2', 'init', '-c', 'workload/'+params.workload_template , '-t', str(prom_token), '--uuid', str(params.uuid), '--prometheus-url', str(prom_url), '-m', 'workload/metrics_full.yaml' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    print("Pausing for a minute..")
    time.sleep(60)

    try:
        print("Deleting the SPK pods..", params.uuid)
        cmd=['./kube-burner-0.14.2', 'init', '-c', 'workload/cfg_delete_icni2_serving_resource.yml', '-t', str(prom_token), '--uuid', '1234' ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))


    output = process_out.decode("utf-8")

    print("==>> Web Burner {} Workload complete!".format(params.workload_template))    
    return "success", SuccessOutput(params.uuid,output)



if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                RunKubeBurner,
                RunWebBurner,
                DeleteWebBurner
            )
        )
    )
