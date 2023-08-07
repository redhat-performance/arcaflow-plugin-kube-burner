#!/usr/bin/env python3

import sys
import os
import typing
from arcaflow_plugin_sdk import plugin
import subprocess
import time
from kubeburner_schema import (
    KubeBurnerInputParams,
    WebBurnerInputParams,
    SuccessOutput,
    ErrorOutput,
    kube_burner_input_schema,
    node_density_params,
    cluster_density_params,
    node_density_cni_params,
    node_density_heavy_params,
)
from helper_functions import (
    get_prometheus_creds,
    readkubeconfig,
    calculate_normal_limit_count,
    create_kubeconfig_secret,
)


@plugin.step(
    id="kube-burner",
    name="Kube-Burner Workload",
    description="""Kube-burner Workloads: node-density, node-density-cni,
                node-density-heavy, cluster-density, cluster-density-v2, cluster-density-ms """,
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def RunKubeBurner(
    params: KubeBurnerInputParams,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    print("==>> Running Kube Burner {} Workload ...".format(params.workload))

    readkubeconfig(params.kubeconfig)
    os.environ["KUBECONFIG"] = "./kubeconfig"

    serialized_params = kube_burner_input_schema.serialize(params)

    if params.workload == "node-density":
        param_list = node_density_params
    elif params.workload == "node-density-cni":
        param_list = node_density_cni_params
    elif params.workload == "node-density-heavy":
        param_list = node_density_heavy_params
    elif "cluster-density" in params.workload:
        param_list = cluster_density_params
    else:
        param_list = ["--help"]

    flags = []
    for param, value in serialized_params.items():
        if param in param_list:
            if "_" in param:
                param = param.replace("_", "-")
            flags.append(f"--{param}={value}")

    try:
        cmd = ["./kube-burner", "ocp", str(params.workload)] + flags
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(
            error.returncode,
            "{} failed with return code {}:\n{}".format(
                error.cmd[0], error.returncode, error.output
            ),
        )

    output = process_out.decode("utf-8")

    print("==>> Kube Burner {} Workload complete!".format(params.workload))
    return "success", SuccessOutput(params.uuid, output)


@plugin.step(
    id="run-web-burner",
    name="Web-Burner Workload",
    description="Plugin to run the Web-burner workload",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def RunWebBurner(
    params: WebBurnerInputParams,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    print("==>> Running Web Burner {} Workload ...".format(params.workload_template))

    readkubeconfig(params.kubeconfig)
    os.environ["KUBECONFIG"] = "./kubeconfig"
    create_kubeconfig_secret()
    # exporting these vars as they are read by the kube-burner templates
    os.environ["SCALE"] = str(params.scale_factor)
    os.environ["BFD"] = params.bfd_enabled
    os.environ["QPS"] = str(params.qps)
    os.environ["BURST"] = str(params.burst)
    os.environ["INDEXING"] = params.indexing
    os.environ["LIMITCOUNT"] = str(
        calculate_normal_limit_count(params.number_of_nodes)
    )
    os.environ["ES_SERVER"] = str(params.es_server)
    os.environ["ES_INDEX"] = str(params.es_index)
    os.environ["SRIOV"] = str(params.sriov)
    os.environ["BRIDGE"] = str(params.bridge)
    prom_url, prom_token = get_prometheus_creds()

    try:
        print("Creating the SPK pods..")
        cmd = [
            "./kube-burner-wb", "init",
            "-c", "workload/cfg_icni2_serving_resource_init.yml",
            "-t", str(prom_token),
            "--uuid", "1234",
        ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(
            error.returncode,
            "{} failed with return code {}:\n{}".format(
                error.cmd[0], error.returncode, error.output
            ),
        )

    print("Pausing for a minute..")
    time.sleep(60)

    try:
        print("Creating the ICNI2 workload..", params.uuid)
        cmd = [
            "./kube-burner-wb", "init",
            "-c", "workload/" + params.workload_template,
            "-t", str(prom_token),
            "--uuid", str(params.uuid),
            "--prometheus-url", str(prom_url),
            "-m", "workload/metrics_full.yml",
        ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(
            error.returncode,
            "{} failed with return code {}:\n{}".format(
                error.cmd[0], error.returncode, error.output
            ),
        )

    output = process_out.decode("utf-8")

    print("==>> Web Burner {} Workload complete!".format(params.workload_template))
    return "success", SuccessOutput(params.uuid, output)


@plugin.step(
    id="delete-web-burner",
    name="Web-Burner Workload",
    description="Plugin to delete resources created by the web-burner workload",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def DeleteWebBurner(
    params: WebBurnerInputParams,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    print("==>> Running Web Burner {} Workload ...".format(params.workload_template))

    readkubeconfig(params.kubeconfig)
    os.environ["KUBECONFIG"] = "./kubeconfig"
    # exporting these vars as they are read by the kube-burner templates
    os.environ["SCALE"] = str(params.scale_factor)
    os.environ["BFD"] = params.bfd_enabled
    os.environ["QPS"] = str(params.qps)
    os.environ["BURST"] = str(params.burst)
    os.environ["ES_SERVER"] = str(params.es_server)
    os.environ["ES_INDEX"] = str(params.es_index)
    os.environ["LIMITCOUNT"] = str(
        calculate_normal_limit_count(params.number_of_nodes)
    )
    os.environ["SRIOV"] = str(params.sriov)
    os.environ["BRIDGE"] = str(params.bridge)
    prom_url, prom_token = get_prometheus_creds()

    try:
        print("Deleting the ICNI2 workload..")
        cmd = [
            "./kube-burner-wb", "init",
            "-c", "workload/" + params.workload_template,
            "-t", str(prom_token),
            "--uuid", str(params.uuid),
            "--prometheus-url", str(prom_url),
            "-m", "workload/metrics_full.yml",
        ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(
            error.returncode,
            "{} failed with return code {}:\n{}".format(
                error.cmd[0], error.returncode, error.output
            ),
        )

    print("Pausing for a minute..")
    time.sleep(60)

    try:
        print("Deleting the SPK pods..", params.uuid)
        cmd = [
            "./kube-burner-wb", "init",
            "-c", "workload/cfg_delete_icni2_serving_resource.yml",
            "-t", str(prom_token),
            "--uuid", "1234",
        ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(
            error.returncode,
            "{} failed with return code {}:\n{}".format(
                error.cmd[0], error.returncode, error.output
            ),
        )

    output = process_out.decode("utf-8")

    print("==>> Web Burner {} Workload complete!".format(params.workload_template))
    return "success", SuccessOutput(params.uuid, output)


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                RunKubeBurner,
                RunWebBurner,
                DeleteWebBurner,
            )
        )
    )
