import base64
import os
import tempfile
from typing import List

import kubernetes
import requests
from flask import Flask
from kubernetes.client import V1ConfigMap, V1Secret

KUBERNETES_NAMESPACE_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"


def config_read_namespace() -> str:
    with open(KUBERNETES_NAMESPACE_FILENAME) as f:
        return f.read().strip()


def config_from_pycode(app: Flask, content: str):
    with tempfile.NamedTemporaryFile(mode='w', suffix="config.py") as f:
        f.write(content)
        f.flush()
        app.config.from_pyfile(f.name)


def setup_config(app: Flask):
    src = os.getenv("CONFIG_SOURCE", "config.py")
    if src.startswith("kubernetes://"):
        items: List[str] = src.removeprefix("kubernetes://").split("/")
        if len(items) == 3:
            items.insert(0, config_read_namespace())
        if len(items) != 4:
            raise Exception("invalid CONFIG_SOURCE: " + src)
        kubernetes.config.load_config()

        namespace, kind, name, key = items
        if kind.startswith("configmap"):
            config: V1ConfigMap = kubernetes.client.CoreV1Api().read_namespaced_config_map(name=name,
                                                                                           namespace=namespace)
            config_from_pycode(app, config.data[key])
        elif kind.startswith("secret"):
            secret: V1Secret = kubernetes.client.CoreV1Api().read_namespaced_secret(name=name, namespace=namespace)
            config_from_pycode(app, base64.b64decode(secret.data[key]).decode("utf-8"))
        else:
            raise Exception("invalid CONFIG_SOURCE: " + src)
    elif src.startswith("http://") or src.startswith("https://"):
        config_from_pycode(app, requests.get(src).text)
    else:
        app.config.from_pyfile(src)
