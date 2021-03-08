#!/usr/bin/env python3

import click
from flask.cli import FlaskGroup
from planner.app import create_app


@click.group(cls=FlaskGroup, create_app=lambda info: create_app())
def cli():
    pass


if __name__ == "__main__":
    cli()
