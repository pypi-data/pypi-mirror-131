from functools import wraps
from timeit import default_timer
from typing import Optional, List, Tuple

from flask import Flask, Response, g, request
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_ZIPKIN_ENDPOINT
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Histogram
from prometheus_client.exposition import make_wsgi_app


def ignore_metrics(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        g.metrics_ignore = True
        return f(*args, **kwargs)

    return wrapper


class Metrics:

    def __init__(self, app: Flask, metrics_path="/metrics", ignored_paths: Optional[List[str]] = None):
        self.metrics_path = metrics_path
        self.metrics_app = make_wsgi_app()
        self.ignored_paths = ignored_paths if ignored_paths is not None else []

        self.duration_histogram = Histogram(
            name="http_request_duration_seconds",
            documentation="duration of HTTP requests in seconds",
            labelnames=("method", "handler", "status"),
            buckets=Histogram.DEFAULT_BUCKETS,
        )

        @app.before_request
        def do_before_request():
            if self.should_ignore():
                return
            g.metrics_start_time = default_timer()

        @app.after_request
        def do_after_request(response: Response):
            if self.should_ignore():
                return response
            self.duration_histogram.labels(*self.calculate_request_labels(response)).observe(
                self.calculate_request_duration())
            return response

        @app.teardown_request
        def do_teardown_request(exception=None):
            if exception is None or self.should_ignore():
                return
            self.duration_histogram.labels(*self.calculate_request_labels(None)).observe(
                self.calculate_request_duration())

    def calculate_request_duration(self) -> float:
        _ = self
        return max(g.metrics_start_time - default_timer(), 0)

    def calculate_request_labels(self, response: Response = None) -> Tuple[str, str, str]:
        _ = self
        status = "500"
        if status is not None:
            status = str(response.status_code)
        rule = "/404"
        if request.url_rule is not None:
            rule = request.url_rule.rule
        return request.method, rule, status

    def should_ignore(self) -> bool:
        if hasattr(g, "metrics_ignore") and g.metrics_ignore:
            return True
        if any((request.url == p or (request.url_rule is not None and request.url_rule.rule == p)) for p in
               self.ignored_paths):
            g.metrics_ignore = True
            return True
        return False

    def expose(self, app: Flask):
        """
        exponse metrics to Flask application

        :param app: Flask application
        :return: None
        """

        @app.get(self.metrics_path)
        @ignore_metrics
        def route_metrics():
            return self.metrics_app


def setup_observability(app: Flask):
    # using B3 headers
    set_global_textmap(B3MultiFormat())

    # using zipkin exporter
    span_exporter = ZipkinExporter(endpoint=(
        app.config[OTEL_EXPORTER_ZIPKIN_ENDPOINT] if hasattr(app.config, OTEL_EXPORTER_ZIPKIN_ENDPOINT) else None))
    span_processor = BatchSpanProcessor(span_exporter)

    # setup global tracer provider
    tracer_provider = TracerProvider(resource=Resource(attributes={
        "service.name": app.config.get("SERVICE_NAME", "unknown-service")
    }))
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # initialize tracing components
    LoggingInstrumentor().instrument(set_logging_format=True)
    FlaskInstrumentor().instrument_app(
        app,
        excluded_urls="/metrics,/favicon.ico,/healthz",
    )
    RequestsInstrumentor().instrument()

    # setup metrics
    Metrics(
        app,
        ignored_paths=[
            "/favicon.ico",
            "/healthz",
        ],
    ).expose(app)
