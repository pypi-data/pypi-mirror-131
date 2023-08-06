from flask import Flask, g
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, registry, Session

model_registry = registry()

ModelBase = model_registry.generate_base(name="ModelBase")


def database_engine() -> Engine:
    return g.database_engine


def database_session_maker() -> sessionmaker:
    return g.database_session_maker


def database_session() -> Session:
    return database_session_maker()()


def database_transaction() -> Session:
    return database_session_maker().begin()


def setup_database(app: Flask, engine_args: dict = None, session_args: dict = None):
    if engine_args is None:
        engine_args = {}
    if session_args is None:
        session_args = {}

    engine_extras = app.config.get_namespace("DATABASE_ENGINE_")
    url = engine_extras.pop("url")
    engine_extras.update(**engine_args)

    engine = create_engine(url, **engine_extras)
    SQLAlchemyInstrumentor().instrument(engine=engine)

    session_extras = app.config.get_namespace("DATABASE_SESSION_")
    session_extras.update(**session_args)

    session_maker = sessionmaker(engine, **session_extras)

    @app.before_request
    def do_before_request():
        g.database_engine = engine
        g.database_session_maker = session_maker
