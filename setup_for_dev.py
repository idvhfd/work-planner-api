from planner.app import create_app, db
from planner.models import Worker, Shift, WorkerShift


def main():
    worker = Worker()
    worker.first_name = 'Test'
    worker.last_name = 'McTest'

    db.session.add(worker)

    shift = Shift()
    shift.start_time = '0:00'
    shift.end_time = '8:00'

    db.session.add(shift)
    db.session.commit()

    worker_shift = WorkerShift()
    worker_shift.worker = worker
    worker_shift.shift = shift
    worker_shift.day = '2021-01-01'

    db.session.add(worker_shift)
    db.session.commit()


if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        main()
