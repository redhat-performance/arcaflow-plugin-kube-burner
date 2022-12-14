#!/usr/bin/env python3

import sys
import typing
from dataclasses import dataclass, field
from arcaflow_plugin_sdk import plugin, validation,schema
from typing import List,Dict
import subprocess
import datetime
import yaml
from kubeburner_schema import KubeBurnerInputParams, SuccessOutput, ErrorOutput, kube_burner_output_schema, kube_burner_input_schema,node_density_params,cluster_density_params



@plugin.step(
    id="kube-burner",
    name="Kube-Burner Workload",
    description="Kube-burner Workload which stresses the cluster by creating sleep pods. Creates a single namespace with a number of Deployments proportional to the calculated number of pod.",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def RunKubeBurner(params: KubeBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Kube Burner {} Workload ...".format(params.workload))
    
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



if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                RunKubeBurner,
            )
        )
    )
