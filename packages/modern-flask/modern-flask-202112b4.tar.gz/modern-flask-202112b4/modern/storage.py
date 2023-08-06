import oss2
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


def storage_oss_service() -> oss2.Service:
    return g.oss_service


def storage_oss_bucket() -> oss2.Bucket:
    return g.oss_bucket


def setup_storage(app: Flask):
    args = app.config.get_namespace("STORAGE_")
    vendor = args.pop("vendor")
    if vendor == "cos":
        new_args = {}
        for key, val in args.items():
            new_args[COS_PARAMS_MAPPING[key]] = val
        cos_config = CosConfig(**new_args)
        cos_client = CosS3Client(cos_config)

        @app.before_request
        def do_before_request():
            g.cos_client = cos_client
    elif vendor == "oss":
        auth = oss2.Auth(args.pop("access_key_id"), args.pop("access_key_secret"))
        service = oss2.Service(auth, endpoint=args.get("endpoint"))
        bucket = None
        if "bucket" in args:
            bucket = oss2.Bucket(auth, args.get("endpoint"), args.get("bucket"))

        @app.before_request
        def do_before_request():
            g.oss_service = service
            g.oss_bucket = bucket

    else:
        raise Exception('only cos, oss is supported')
