import os

import spell.cli.utils  # for __file__ introspection
from spell.cli.utils.cluster_utils import kubectl

runs_manifests_dir = os.path.join(os.path.dirname(spell.cli.utils.__file__), "kube_manifests", "spell-run")

#########################
# Runs
#########################


# must be executed with elevated permissions (crd)
def add_argo():
    kubectl(
        "apply",
        "-f",
        os.path.join(runs_manifests_dir, "argo"),
        "-n",
        "spell-run",
    )


def create_build_run_configmap(namespace):
    # Delete if it exists
    kubectl(
        "delete",
        "configmap",
        "k8s-build",
        "-n",
        namespace,
        "--ignore-not-found",
    )
    path = os.path.join(runs_manifests_dir, "build.sh")
    kubectl(
        "create",
        "configmap",
        "k8s-build",
        "-n",
        namespace,
        f"--from-file={path}",
    )


def create_build_artifacts_pvc(namespace):
    kubectl("apply", "-n", namespace, "-f", os.path.join(runs_manifests_dir, "build_artifacts_pvc.yaml"))
