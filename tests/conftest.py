import pytest
from flask import Flask

from planner.app import create_app, db
from planner.models import Worker, Shift, WorkerShift


def delete_from_all_tables(app: Flask) -> None:
    with app.app_context():
        with db.session.connection() as conn:
            for table in reversed(db.Model.metadata.sorted_tables):
                conn.execute(table.delete())
            db.session.commit()


@pytest.fixture(scope='session')
def app_global(request):
    app = create_app(env='testing')

    with app.app_context():
        db.create_all()

    delete_from_all_tables(app)

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def app(app_global):
    yield app_global


@pytest.fixture()
def cleanup_db(app):
    yield
    delete_from_all_tables(app)


@pytest.fixture()
def test_client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def worker_factory(app):
    worker_ids = []

    def factory(
            first_name='Test',
            last_name='McTest',
    ):
        with app.app_context():
            worker = Worker()

            worker.first_name = first_name
            worker.last_name = last_name

            db.session.add(worker)
            db.session.commit()
            worker_ids.append(worker.id)

        return worker

    yield factory

    with app.app_context():
        db.session.query(Worker).filter(Worker.id.in_(worker_ids)).delete(synchronize_session='fetch')
        db.session.commit()


@pytest.fixture()
def regular_worker(app, worker_factory):
    worker = worker_factory()
    yield worker


@pytest.fixture()
def shift_factory(app):
    shift_ids = []

    def factory(
            start_time='0:00',
            end_time='8:00',
    ):
        with app.app_context():
            shift = Shift()

            shift.start_time = start_time
            shift.end_time = end_time

            db.session.add(shift)
            db.session.commit()
            shift_ids.append(shift.id)

        return shift

    yield factory

    with app.app_context():
        db.session.query(Shift).filter(Shift.id.in_(shift_ids)).delete(synchronize_session='fetch')
        db.session.commit()


@pytest.fixture()
def regular_shift(app, shift_factory):
    shift = shift_factory()
    yield shift


@pytest.fixture()
def worker_shift_factory(app, regular_worker, regular_shift):
    workers_shifts_ids = []

    def factory(
            worker=regular_worker,
            shift=regular_shift,
            day='2021-01-01',
    ):
        with app.app_context():
            worker_shift = WorkerShift()

            worker_shift.worker = worker
            worker_shift.shift = shift
            worker_shift.day = day

            db.session.add(worker_shift)
            db.session.commit()
            workers_shifts_ids.append(worker_shift.id)

        return worker_shift

    yield factory

    with app.app_context():
        db.session.query(WorkerShift).filter(WorkerShift.id.in_(workers_shifts_ids)).delete(synchronize_session='fetch')
        db.session.commit()


@pytest.fixture()
def regular_worker_shift(app, worker_shift_factory):
    worker_shift = worker_shift_factory()
    yield worker_shift
