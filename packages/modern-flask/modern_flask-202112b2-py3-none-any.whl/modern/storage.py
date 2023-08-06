from flask import Flask, g
from qcloud_cos import CosConfig, CosS3Client

COS_PARAMS_MAPPING = {
    "appid": "Appid",
    "region": "Region",
    "secret_id": "SecretId",
    "secret_key": "SecretKey",
    "token": "Token",
    "scheme": "Scheme",
    "timeout": "Timeout",
    "access_id": "SecretId",
    "access_key": "SecretKey",
    "endpoint": "Endpoint",
    "ip": "IP",
    "port": "Port",
    "anonymous": "Anonymous",
    "ua": "UA",
    "domain": "Domain",
    "service_domain": "ServiceDomain",
    "pool_connections": "PoolConnections",
    "pool_max_size": "PoolMaxSize",
    "allow_redirects": "AllowRedirects",
    "sign_host": "SignHost",
    "endpoint_ci": "EndpointCi",
}


def storage_cos_client() -> CosS3Client:
    return g.cos_client


def setup_storage(app: Flask):
    args = app.config.get_namespace("STORAGE_")
    if args.pop("vendor") == "cos":
        new_args = {}
        for key, val in args.items():
            new_args[COS_PARAMS_MAPPING[key]] = val
        cos_config = CosConfig(**new_args)
        cos_client = CosS3Client(cos_config)

        @app.before_request
        def do_before_request():
            g.cos_client = cos_client
    else:
        raise Exception('only cos is supported')
