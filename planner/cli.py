from datetime import datetime

import click
from flask.cli import with_appcontext

from planner.app import db
from planner.models import Worker, Shift, WorkerShift


# --- DEV CLI ---
@click.command()
@click.option('--first-name', prompt=True)
@click.option('--last-name', prompt=True)
@click.option('--count', prompt=True, type=click.INT)
@with_appcontext
def create_workers(first_name: str, last_name: str, count: int):
    for i in range(count):
        worker = Worker(
            first_name=first_name + f' #{i}',
            last_name=last_name
        )
        db.session.add(worker)

    db.session.commit()


@click.command()
@click.option('--start-time', prompt=True)
@click.option('--end-time', prompt=True)
@with_appcontext
def create_shifts(start_time: str, end_time: str):
    shift = Shift(
        start_time=start_time,
        end_time=end_time,
    )
    db.session.add(shift)
    db.session.commit()


@click.command()
@click.option('--worker-id', prompt=True, type=click.INT)
@click.option('--shift-id', prompt=True, type=click.INT)
@click.option('--day', prompt=True)
@with_appcontext
def create_workers_shifts(worker_id: int, shift_id: int, day: str):
    try:
        datetime.strptime(day, '%Y-%m-%d')
    except ValueError:
        click.echo('Invalid "day" value')

    workers_shifts = WorkerShift(
        worker_id=worker_id,
        shift_id=shift_id,
        day=day,
    )
    db.session.add(workers_shifts)
    db.session.commit()
