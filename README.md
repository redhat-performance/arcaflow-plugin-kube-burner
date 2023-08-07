# Kube-burner workload plugin for Arcaflow

arca-kube-burner is a workload plugin which can run [kube-burner](https://github.com/cloud-bulldozer/kube-burner) benchmarks or the [web-burner](https://github.com/redhat-performance/web-burner) workloads
using the [Arcaflow python SDK](https://github.com/arcalot/arcaflow-plugin-sdk-python).

Documentation for Kube-burner workloads can be found here: [Workloads Documentation](https://github.com/cloud-bulldozer/e2e-benchmarking/blob/master/workloads/kube-burner/README.md)

Documentation for web-burner workloads can be found here: [Workloads Documentation](https://github.com/redhat-performance/web-burner)

## To test:

In order to run the [kube-burner plugin](arcaflow_plugin_kubeburner/kubeburner_plugin.py) run the following steps:

### Native 
*Note: The plugin should be able to access the kubeconfig of your openshift cluster and the kube-burner binary must be downloaded locally. Install poetry(curl -sSL https://install.python-poetry.org | python3 - ). Poetry requires python version > 3.7, recommended to use >3.9*

1. Clone this repository
2. Create a `venv` in the current directory with `python3.9 -m venv $(pwd)/venv`
3. Activate the `venv` by running `source venv/bin/activate`
4. cd arcaflow-plugin-kube-burner
5. curl -L https://github.com/cloud-bulldozer/kube-burner/releases/download/v1.4.2/kube-burner-1.4.2-Linux-x86_64.tar.gz | tar xz -C . kube-burner
6. Run `poetry install`
7. Copy and Paste the openshift cluster's kubeconfig file content into the kubeburner_input.yaml file
8. To run a kube-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f configs/kubeburner_input.yaml -s kube-burner --debug`

### Containerized
1. Clone this repository
2. cd arcaflow-plugin-kube-burner
3. Copy and Paste the openshift cluster's kubeconfig file content into the kubeburner_input.yaml file
4. Create the container with `docker build -t arca-kube-burner -f Dockerfile`
5. Run `cat configs/kubeburner_input.yaml | docker run -i arca-kube-burner -s kube-burner --debug -f -`

In order to run the [web-burner plugin](arcaflow_plugin_kubeburner/kubeburner_plugin.py) run the following steps:

### Prerequisites
*Note: This is for ICNI2 worklaods*
1. Enable sr-iov on the baremetal nodes from the node management console or using badfish.
2. Install the openshift-sriov-network-operator on the openshift cluster using the cli or the operatorhub GUI.
3. Identify and label a specific number of nodes with the node-role.kubernetes.io/worker-spk="" label.
4. check if all labelled worker nodes have the same sr-iov PF(this is done by sshing into each node from the provisoner node to get the PF of a node, command: nic=$(ssh -i /home/kni/.ssh/id_rsa -o StrictHostKeyChecking=no core@{worker-node name} "sudo ovs-vsctl list-ports br-ex | head -1")  eg: $nic = ens7f0
5. Apply the sriov node policy using the $nic obtained from step 4.
6. wait for sriov nodes to be ready


### Native 
*Note: The plugin should be able to access the kubeconfig of your openshift cluster and the kube-burner binary must be downloaded locally. Rename the kube-burner binary as web-burner or follow step number 7&8 below. Install poetry(curl -sSL https://install.python-poetry.org | python3 - ). Poetry requires python version > 3.7, recommended to use >3.9*

1. Clone this repository
2. Create a `venv` in the current directory with `python3.9 -m venv $(pwd)/venv`
3. Activate the `venv` by running `source venv/bin/activate`
4. Run git clone https://github.com/redhat-performance/web-burner.git --branch v1.0
5. Run cp -r web-burner/workload web-burner/objectTemplates arcaflow-plugin-kube-burner/
6. cd arcaflow-plugin-kube-burner
7. curl -L https://github.com/cloud-bulldozer/kube-burner/releases/download/v0.14.2/kube-burner-0.14.2-Linux-x86_64.tar.gz | tar xz -C . kube-burner
8. mv kube-burner kube-burner-0.14.2
9. Run `poetry install`
10. Copy and Paste the openshift cluster's kubeconfig file content into the configs/webburner_input.yaml file
11. To run a web-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f configs/webburner_input.yaml -s run-web-burner --debug`
12. To delete a web-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f configs/webburner_input.yaml -s delete-web-burner --debug`

### Containerized
1. Clone this repository
2. cd arcaflow-plugin-kube-burner
3. Copy and Paste the openshift cluster's kubeconfig file content into the configs/webburner_input.yaml file
4. Create the container with `docker build -t arca-web-burner -f Dockerfile`
5. To run a web-burner workload `cat configs/webburner_input.yaml | docker run -i arca-web-burner -s run-web-burner--debug -f -`
6. To delete a web-burner workload `cat configs/webburner_input.yaml | docker run -i arca-kube-burner -s delete-web-burner --debug -f -`           


## Image Building

You can change this plugin's image version tag in
`.github/workflows/carpenter.yaml` by editing the
`IMAGE_TAG` variable, and pushing that change to the
branch designated in that workflow.

# Autogenerated Input/Output Documentation by Arcaflow-Docsgen Below

<!-- Autogenerated documentation by arcaflow-docsgen -->
## Web-Burner Workload (`delete-web-burner`)

Plugin to delete resources created by the web-burner workload

### Input

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>WebBurnerInputParams</td></tr>
<tr><th>Properties</th><td><details><summary>bfd_enabled (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Bidirectional Forwarding Detection</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>bridge (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>The network bridge to use. breth0 for kind.sh ovn-kubernetes clusters</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;br-ex&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>burst (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Maximum burst for throttle</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>es_index (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>The ElasticSearch index used to index the metrics</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>es_server (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>List of ES instances</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>indexing (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>To enable or disable indexing in elasticsearch(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>kubeconfig (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>kubeconfig</td></tr><tr><th>Description:</th><td>Openshift cluster kubeconfig file content as a string</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>number_of_nodes (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Number of nodes</td></tr><tr><th>Description:</th><td>Size of cluster/ number of nodes in the cluster</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>qps (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Max number of queries per second</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>scale_factor (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Scaling factor for the workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>1</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>sriov (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>To enable or disable sriov, disabling it will create macvlan network
            attachment definitions instead</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>uuid (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>uuid to be used for the job</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>workload_template (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Workload Template</td></tr><tr><th>Description:</th><td>Kube-burner Template to use</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>WebBurnerInputParams (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>bfd_enabled (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Bidirectional Forwarding Detection</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>bridge (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>The network bridge to use. breth0 for kind.sh ovn-kubernetes clusters</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;br-ex&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>burst (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Maximum burst for throttle</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>es_index (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>The ElasticSearch index used to index the metrics</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>es_server (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>List of ES instances</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>indexing (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>To enable or disable indexing in elasticsearch(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>kubeconfig (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>kubeconfig</td></tr><tr><th>Description:</th><td>Openshift cluster kubeconfig file content as a string</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>number_of_nodes (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Number of nodes</td></tr><tr><th>Description:</th><td>Size of cluster/ number of nodes in the cluster</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>qps (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Max number of queries per second</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>scale_factor (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Scaling factor for the workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>1</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>sriov (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>To enable or disable sriov, disabling it will create macvlan network
            attachment definitions instead</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>uuid (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>uuid to be used for the job</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>workload_template (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Workload Template</td></tr><tr><th>Description:</th><td>Kube-burner Template to use</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>

### Outputs


#### error

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>ErrorOutput</td></tr>
<tr><th>Properties</th><td><details><summary>error (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Failure Error</td></tr><tr><th>Description:</th><td>Reason for failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>exit_code (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Exit Code</td></tr><tr><th>Description:</th><td>Exit code returned by the program in case of a failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>ErrorOutput (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>error (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Failure Error</td></tr><tr><th>Description:</th><td>Reason for failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>exit_code (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Exit Code</td></tr><tr><th>Description:</th><td>Exit code returned by the program in case of a failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>

#### success

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>SuccessOutput</td></tr>
<tr><th>Properties</th><td><details><summary>output (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Kube burner workload output</td></tr><tr><th>Description:</th><td>Output generated by the kube burner workload</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>uuid (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>UUID</td></tr><tr><th>Description:</th><td>UUID used for this workload run</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>SuccessOutput (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>output (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Kube burner workload output</td></tr><tr><th>Description:</th><td>Output generated by the kube burner workload</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>uuid (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>UUID</td></tr><tr><th>Description:</th><td>UUID used for this workload run</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>



## Kube-Burner Workload (`kube-burner`)

Kube-burner Workloads: node-density, node-density-cni,
                node-density-heavy, cluster-density, cluster-density-v2,
                cluster-density-ms 

### Input

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>KubeBurnerInputParams</td></tr>
<tr><th>Properties</th><td><details><summary>alerting (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Enable alerting(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>burst (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Maximum burst for throttle</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>churn (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Enable churning(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>churn_delay (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Time to wait between each churn</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;2m0s&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>churn_duration (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Churn duration</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;1h0m0s&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>churn_percent (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Percentage of job iterations that kube-burner will churn each round</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>10</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>es_index (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>The ElasticSearch index used to index the metrics</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>es_server (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>List of ES instances</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>gc (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Garbage collect created namespaces(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>iterations (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Cluster-density iterations</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>500</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>kubeconfig (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>kubeconfig</td></tr><tr><th>Description:</th><td>Openshift cluster kubeconfig file content as a string</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>local_indexing (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Enable local indexing</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>log_level (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Allowed values: debug, info, warn, error, fatal</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;info&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>network_policies (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Enable network policies in the workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>pod_ready_threshold (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Pod ready timeout threshold for node-density workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;5s&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>pods_per_node (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Pods per node for node-density* workloads</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>245</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>probes_period (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Perf app readiness/livenes probes period in seconds</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>10</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>qps (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Max number of queries per second</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>timeout (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Benchmark timeout</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;2h&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>uuid (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>uuid to be used for the job</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>workload (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Name</td></tr><tr><th>Description:</th><td>workload name</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>KubeBurnerInputParams (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>alerting (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Enable alerting(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>burst (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Maximum burst for throttle</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>churn (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Enable churning(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>churn_delay (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Time to wait between each churn</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;2m0s&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>churn_duration (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Churn duration</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;1h0m0s&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>churn_percent (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Percentage of job iterations that kube-burner will churn each round</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>10</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>es_index (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>The ElasticSearch index used to index the metrics</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>es_server (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>List of ES instances</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>gc (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Garbage collect created namespaces(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>iterations (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Cluster-density iterations</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>500</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>kubeconfig (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>kubeconfig</td></tr><tr><th>Description:</th><td>Openshift cluster kubeconfig file content as a string</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>local_indexing (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Enable local indexing</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>log_level (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Allowed values: debug, info, warn, error, fatal</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;info&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>network_policies (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Enable network policies in the workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>pod_ready_threshold (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Pod ready timeout threshold for node-density workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;5s&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>pods_per_node (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Pods per node for node-density* workloads</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>245</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>probes_period (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Perf app readiness/livenes probes period in seconds</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>10</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>qps (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Max number of queries per second</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>timeout (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Benchmark timeout</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;2h&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>uuid (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>uuid to be used for the job</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>workload (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Name</td></tr><tr><th>Description:</th><td>workload name</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>

### Outputs


#### error

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>ErrorOutput</td></tr>
<tr><th>Properties</th><td><details><summary>error (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Failure Error</td></tr><tr><th>Description:</th><td>Reason for failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>exit_code (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Exit Code</td></tr><tr><th>Description:</th><td>Exit code returned by the program in case of a failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>ErrorOutput (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>error (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Failure Error</td></tr><tr><th>Description:</th><td>Reason for failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>exit_code (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Exit Code</td></tr><tr><th>Description:</th><td>Exit code returned by the program in case of a failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>

#### success

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>SuccessOutput</td></tr>
<tr><th>Properties</th><td><details><summary>output (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Kube burner workload output</td></tr><tr><th>Description:</th><td>Output generated by the kube burner workload</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>uuid (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>UUID</td></tr><tr><th>Description:</th><td>UUID used for this workload run</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>SuccessOutput (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>output (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Kube burner workload output</td></tr><tr><th>Description:</th><td>Output generated by the kube burner workload</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>uuid (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>UUID</td></tr><tr><th>Description:</th><td>UUID used for this workload run</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>



## Web-Burner Workload (`run-web-burner`)

Plugin to run the Web-burner workload

### Input

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>WebBurnerInputParams</td></tr>
<tr><th>Properties</th><td><details><summary>bfd_enabled (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Bidirectional Forwarding Detection</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>bridge (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>The network bridge to use. breth0 for kind.sh ovn-kubernetes clusters</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;br-ex&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>burst (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Maximum burst for throttle</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>es_index (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>The ElasticSearch index used to index the metrics</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>es_server (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>List of ES instances</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>indexing (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>To enable or disable indexing in elasticsearch(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>kubeconfig (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>kubeconfig</td></tr><tr><th>Description:</th><td>Openshift cluster kubeconfig file content as a string</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>number_of_nodes (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Number of nodes</td></tr><tr><th>Description:</th><td>Size of cluster/ number of nodes in the cluster</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>qps (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Max number of queries per second</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>scale_factor (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Scaling factor for the workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>1</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details><details><summary>sriov (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>To enable or disable sriov, disabling it will create macvlan network
            attachment definitions instead</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>uuid (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>uuid to be used for the job</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>workload_template (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Workload Template</td></tr><tr><th>Description:</th><td>Kube-burner Template to use</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>WebBurnerInputParams (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>bfd_enabled (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Bidirectional Forwarding Detection</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>bridge (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>The network bridge to use. breth0 for kind.sh ovn-kubernetes clusters</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;br-ex&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>burst (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Maximum burst for throttle</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>es_index (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>The ElasticSearch index used to index the metrics</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>es_server (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>List of ES instances</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>indexing (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>To enable or disable indexing in elasticsearch(true/false)</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;false&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>kubeconfig (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>kubeconfig</td></tr><tr><th>Description:</th><td>Openshift cluster kubeconfig file content as a string</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>number_of_nodes (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Number of nodes</td></tr><tr><th>Description:</th><td>Size of cluster/ number of nodes in the cluster</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>qps (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Max number of queries per second</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>20</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>scale_factor (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Scaling factor for the workload</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>1</code></pre></td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details><details><summary>sriov (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>To enable or disable sriov, disabling it will create macvlan network
            attachment definitions instead</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Default (JSON encoded):</th><td><pre><code>&#34;true&#34;</code></pre></td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>uuid (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>uuid to be used for the job</td></tr><tr><th>Required:</th><td>No</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>workload_template (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Workload Template</td></tr><tr><th>Description:</th><td>Kube-burner Template to use</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>

### Outputs


#### error

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>ErrorOutput</td></tr>
<tr><th>Properties</th><td><details><summary>error (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Failure Error</td></tr><tr><th>Description:</th><td>Reason for failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>exit_code (<code>int</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Exit Code</td></tr><tr><th>Description:</th><td>Exit code returned by the program in case of a failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>ErrorOutput (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>error (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Failure Error</td></tr><tr><th>Description:</th><td>Reason for failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>exit_code (<code>int</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Exit Code</td></tr><tr><th>Description:</th><td>Exit code returned by the program in case of a failure</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>int</code></td>
</tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>

#### success

<table><tbody>
<tr><th>Type:</th><td><code>scope</code></td><tr><th>Root object:</th><td>SuccessOutput</td></tr>
<tr><th>Properties</th><td><details><summary>output (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>Kube burner workload output</td></tr><tr><th>Description:</th><td>Output generated by the kube burner workload</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details><details><summary>uuid (<code>string</code>)</summary>
                <table><tbody><tr><th>Name:</th><td>UUID</td></tr><tr><th>Description:</th><td>UUID used for this workload run</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
            </details></td></tr>
<tr><td colspan="2"><details><summary><strong>Objects</strong></summary><details><summary>SuccessOutput (<code>object</code>)</summary>
            <table><tbody><tr><th>Type:</th><td><code>object</code></td><tr><th>Properties</th><td><details><summary>output (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>Kube burner workload output</td></tr><tr><th>Description:</th><td>Output generated by the kube burner workload</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details><details><summary>uuid (<code>string</code>)</summary>
        <table><tbody><tr><th>Name:</th><td>UUID</td></tr><tr><th>Description:</th><td>UUID used for this workload run</td></tr><tr><th>Required:</th><td>Yes</td></tr><tr><th>Type:</th><td><code>string</code></td></tbody></table>
        </details></td></tr>
</tbody></table>
        </details></details></td></tr>
</tbody></table>
<!-- End of autogenerated documentation -->