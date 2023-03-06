#!/usr/bin/env python3

import re
import unittest
import kubeburner_plugin
from arcaflow_plugin_sdk import plugin


class KubeburnerPluginTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            kubeburner_plugin.KubeBurnerInputParams(
                workload='node-density',
                es_server="https://search-dev-chm.west-2.es.amazonaws.com:443",
                es_index="index",
                kubeconfig="abc"
                )
        )

        plugin.test_object_serialization(
            kubeburner_plugin.ErrorOutput(
                exit_code=1,
                error="This is an error"
            )
        )

        plugin.test_object_serialization(
            kubeburner_plugin.SuccessOutput(
            uuid="ertf-34ft-2edw-iojh",
            output="abcdefghijklmnopqrstuvwxyz"
            )
        )

        plugin.test_object_serialization(
            kubeburner_plugin.WebBurnerInputParams(
            kubeconfig="abc",
            number_of_nodes=50,
            workload_template="cfg_icni1_f5_node_density.yml",
            scale_factor=2,
            bfd_enabled='false'
            )
        )
      


if __name__ == '__main__':
    unittest.main()
