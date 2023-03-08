#!/usr/bin/env python3

import re
import sys
import typing
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Annotated
from arcaflow_plugin_sdk import plugin, schema, annotations, validation
import subprocess
import datetime
import yaml


@dataclass
class CommonInputParams:
    """
    This is the data structure for the common input parameters for kube-burner and web-burner workloads.
    """

    uuid: typing.Annotated[
        typing.Optional[str],
        schema.name("uuid"),
        schema.description("uuid to be used for the job"),
    ] = None

    qps: typing.Annotated[
        typing.Optional[int],
        schema.name("QPS"),
        schema.description("Max number of queries per second"),
    ] = 20

    burst: typing.Annotated[
        typing.Optional[int],
        schema.name("Burst"),
        schema.description("Maximum burst for throttle"),
    ] = 20

    es_index: typing.Annotated[
        typing.Optional[str],
        schema.name("es-index"),
        schema.description("The ElasticSearch index used to index the metrics"),
    ] = None

    es_server: typing.Annotated[
        typing.Optional[str],
        schema.name("es-server"),
        schema.description("List of ES instances"),
    ] = None


@dataclass
class KubeBurnerInput:
    """
    This is the data structure for the input parameters specific to kube-burner workloads.
    """

    workload: typing.Annotated[
        str,
        schema.name("Name"),
        schema.description("workload name"),
    ]

    kubeconfig: typing.Annotated[
        str,
        schema.name("kubeconfig"),
        schema.description("Openshift cluster kubeconfig file content as a string"),
    ]

    log_level: typing.Annotated[
        typing.Optional[str],
        schema.name("log-level"),
        schema.description("Allowed values: trace, debug, info, warn, error, fatal"),
    ] = "info"

    timeout: typing.Annotated[
        typing.Optional[str],
        schema.name("timeout"),
        schema.description("Benchmark timeout"),
    ] = "2h"

    pods_per_node: typing.Annotated[
        typing.Optional[int],
        schema.name("pods-per-node"),
        schema.description("Pods per node for node-density* workloads"),
    ] = 245

    pod_ready_threshold: typing.Annotated[
        typing.Optional[str],
        schema.name("pod-ready-threshold"),
        schema.description("Pod ready timeout threshold for node-density workload"),
    ] = "5s"

    iterations: typing.Annotated[
        typing.Optional[int],
        schema.name("iterations"),
        schema.description("Cluster-density iterations"),
    ] = 500

    alerting: typing.Annotated[
        typing.Optional[str],
        schema.name("alerting"),
        schema.description("Enable alerting(true/false)"),
    ] = "true"

    gc: typing.Annotated[
        typing.Optional[str],
        schema.name("gc"),
        schema.description("Garbage collect created namespaces(true/false)"),
    ] = "true"

    probes_period: typing.Annotated[
        typing.Optional[int],
        schema.name("probes-period"),
        schema.description("Perf app readiness/livenes probes period in seconds"),
    ] = 10

    network_policies: typing.Annotated[
        typing.Optional[str],
        schema.name("network-policies"),
        schema.description("Enable network policies in the workload"),
    ] = "true"

    churn: typing.Annotated[
        typing.Optional[str],
        schema.name("churn"),
        schema.description("Enable churning(true/false)"),
    ] = "true"

    churn_delay: typing.Annotated[
        typing.Optional[str],
        schema.name("churn-delay"),
        schema.description("Time to wait between each churn"),
    ] = "2m0s"

    churn_duration: typing.Annotated[
        typing.Optional[str],
        schema.name("churn-duration"),
        schema.description("Churn duration"),
    ] = "1h0m0s"

    churn_percent: typing.Annotated[
        typing.Optional[int],
        schema.name("churn-percent"),
        schema.description(
            "Percentage of job iterations that kube-burner will churn each round"
        ),
    ] = 10


@dataclass
class WebBurnerInput:
    """
    This is the data structure for the input parameters specific to web-burner workloads.
    """

    workload_template: typing.Annotated[
        str,
        schema.name("Workload Template"),
        schema.description("Kube-burner Template to use"),
    ]

    kubeconfig: typing.Annotated[
        str,
        schema.name("kubeconfig"),
        schema.description("Openshift cluster kubeconfig file content as a string"),
    ]

    number_of_nodes: typing.Annotated[
        int,
        schema.name("Number of nodes"),
        schema.description("Size of cluster/ number of nodes in the cluster"),
    ]

    scale_factor: typing.Annotated[
        typing.Optional[int],
        schema.name("Scale Factor"),
        schema.description("Scaling factor for the workload"),
    ] = 1

    bfd_enabled: typing.Annotated[
        typing.Optional[str],
        schema.name("BFD"),
        schema.description("Bidirectional Forwarding Detection"),
    ] = "false"

    indexing: typing.Annotated[
        typing.Optional[str],
        schema.name("INDEXING"),
        schema.description(
            "To enable or disable indexing in elasticsearch(true/false)"
        ),
    ] = "false"


@dataclass
class KubeBurnerInputParams(CommonInputParams, KubeBurnerInput):
    """
    This is the data structure for the input parameters for kube-burner workloads.
    """


@dataclass
class WebBurnerInputParams(CommonInputParams, WebBurnerInput):
    """
    This is the data structure for the input parameters for web-burner workloads.
    """


@dataclass
class SuccessOutput:
    """
    This is the data structure for output returned by kube-burner workloads.
    """

    uuid: typing.Annotated[
        str, schema.name("UUID"), schema.description("UUID used for this workload run")
    ]

    output: typing.Annotated[
        str,
        schema.name("Kube burner workload output"),
        schema.description("Output generated by the kube burner workload"),
    ]


@dataclass
class ErrorOutput:
    """
    This is the output data structure in the error case.
    """

    exit_code: typing.Annotated[
        int,
        schema.name("Exit Code"),
        schema.description("Exit code returned by the program in case of a failure"),
    ]

    error: typing.Annotated[
        str,
        schema.name("Failure Error"),
        schema.description("Reason for failure"),
    ]


kube_burner_input_schema = plugin.build_object_schema(KubeBurnerInputParams)
web_burner_input_schema = plugin.build_object_schema(WebBurnerInputParams)
output_schema = plugin.build_object_schema(SuccessOutput)
node_density_params = [
    "uuid",
    "qps",
    "burst",
    "es_index",
    "es_server",
    "log_level",
    "timeout",
    "pods_per_node",
    "pod_ready_threshold",
    "alerting",
    "gc",
]
node_density_cni_params = [
    "uuid",
    "qps",
    "burst",
    "es_index",
    "es_server",
    "log_level",
    "timeout",
    "pods_per_node",
    "alerting",
    "gc",
]
node_density_heavy_params = [
    "uuid",
    "qps",
    "burst",
    "es_index",
    "es_server",
    "log_level",
    "timeout",
    "pods_per_node",
    "pod_ready_threshold",
    "probes_period" "alerting",
    "gc",
]
cluster_density_params = [
    "uuid",
    "qps",
    "burst",
    "es_index",
    "es_server",
    "log_level",
    "iterations",
    "timeout",
    "alerting",
    "gc",
    "churn",
    "churn_delay",
    "churn_duration",
    "churn_percent",
]
