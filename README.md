# Kube-burner workload plugin for Arcaflow

arca-kube-burner is a workload plugin which can run [kube-burner](https://github.com/cloud-bulldozer/kube-burner) benchmarks or the web-burner workloads [web-burner](https://github.com/redhat-performance/web-burner)
using the [Arcaflow python SDK](https://github.com/arcalot/arcaflow-plugin-sdk-python).

Documentation for Kube-burner workloads can be found here: [Workloads Documentation](https://github.com/cloud-bulldozer/e2e-benchmarking/blob/master/workloads/kube-burner/README.md)

Documentation for web-burner workloads can be found here: [Workloads Documentation](https://github.com/redhat-performance/web-burner)

## To test:

In order to run the [kube-burner plugin](arcaflow_plugin_kubeburner/kubeburner_plugin.py) run the following steps:

### Native 
*Note: The plugin should be able to access the kubeconfig of your openshift cluster and the kube-burner binary must be downloaded locally. Install poetry(curl -sSL https://install.python-poetry.org | python3 - )*
1. Clone this repository
2. Create a `venv` in the current directory with `python3.9 -m venv $(pwd)/venv`
3. Activate the `venv` by running `source venv/bin/activate`
4. cd arcaflow-plugin-kube-burner
5. curl -L https://github.com/cloud-bulldozer/kube-burner/releases/download/v1.3/kube-burner-1.3-Linux-x86_64.tar.gz | tar xz -C . kube-burner
6. Run `poetry install`
7. Copy and Paste the openshift cluster's kubeconfig file content into the kubeburner_input.yaml file
8. To run a kube-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f configs/kubeburner_input.yaml -s kube-burner`

### Containerized
1. Clone this repository
2. cd arcaflow-plugin-kube-burner
3. Copy and Paste the openshift cluster's kubeconfig file content into the kubeburner_input.yaml file
4. Create the container with `docker build -t arca-kube-burner -f Dockerfile`
5. Run `cat configs/kubeburner_input.yaml | docker run -i arca-kube-burner -s kube-burner --debug -f -`

In order to run the [web-burner plugin](arcaflow_plugin_kubeburner/kubeburner_plugin.py) run the following steps:

### Native 
*Note: The plugin should be able to access the kubeconfig of your openshift cluster and the kube-burner binary must be downloaded locally. Install poetry(curl -sSL https://install.python-poetry.org | python3 - ). Poetry requires python version > 3.7, recommended to use >3.9*
1. Clone this repository
2. Create a `venv` in the current directory with `python3.9 -m venv $(pwd)/venv`
3. Activate the `venv` by running `source venv/bin/activate`
4. Run git clone https://github.com/redhat-performance/web-burner.git
5. Run cp -r web-burner/workload web-burner/objectTemplates arcaflow-plugin-kube-burner/
6. cd arcaflow-plugin-kube-burner
7. curl -L https://github.com/cloud-bulldozer/kube-burner/releases/download/v1.3/kube-burner-1.3-Linux-x86_64.tar.gz | tar xz -C . kube-burner
8. Run `poetry install`
9. Copy and Paste the openshift cluster's kubeconfig file content into the configs/webburner_input.yaml file
10. To run a web-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f configs/webburner_input.yaml -s run-web-burner`
11. To delete a web-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f configs/webburner_input.yaml -s delete-web-burner`

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