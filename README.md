# Kube-burner workload plugin for Arcaflow

arca-kube-burner is a workload plugin of the [kube-burner](https://github.com/cloud-bulldozer/kube-burner) benchmark tool
using the [Arcaflow python SDK](https://github.com/arcalot/arcaflow-plugin-sdk-python).

Documentation for Kube-burner wokrloads can be found here: [Workloads Documentation](https://github.com/cloud-bulldozer/e2e-benchmarking/blob/master/workloads/kube-burner/README.md)

### Note: The plugin should be able to access the kubeconfig of your kubernetes/openshift cluster and kube-burner binary must be downloaded locally. Install poetry(curl -sSL https://install.python-poetry.org | python3 - )

## To test:

In order to run the [kube-burner plugin](kube-burner-plugin.py) run the following steps:

1. Clone this repository
2. Create a `venv` in the current directory with `python3 -m venv $(pwd)/venv`
3. Activate the `venv` by running `source venv/bin/activate`
4. cd arcaflow-plugin-kube-burner
5. curl -L https://github.com/cloud-bulldozer/kube-burner/releases/download/v1.1/kube-burner-1.1-Linux-x86_64.tar.gz | tar xz -C . kube-burner
6. Run `poetry install`
7. To run a kube-burner workload `python3.9 ./arcaflow_plugin_kubeburner/kubeburner_plugin.py -f kubeburner_input.yaml`

## Image Building

You can change this plugin's image version tag in
`.github/workflows/carpenter.yaml` by editing the
`IMAGE_TAG` variable, and pushing that change to the
branch designated in that workflow.