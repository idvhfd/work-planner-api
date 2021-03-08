from typing import Any  # noqa: F401

from planner.app import db

Base = db.Model  # type: Any


def get_model(name):
    return db.Model._decl_class_registry.get(name, None)
