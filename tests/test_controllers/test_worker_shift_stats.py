import datetime

from planner.app import db
from tests import response_util


def test_get_ad_entry_counts_by_day(app, test_client, worker_factory, shift_factory, worker_shift_factory):
    workers_shifts = []
    workers = []
    shifts = []

    entry_count = 15
    start_date = '2020-12-31'
    end_date = '2021-01-31'

    for i in range(1, entry_count):
        workers.append(worker_factory(first_name=f'Test#{i}', last_name=f'McTest#{i}'))
        shifts.append(shift_factory(start_time=str(i) + ":00", end_time=str(i + 1) + ":00"))

    with app.app_context():
        workers = [db.session.merge(worker) for worker in workers]
        shifts = [db.session.merge(shift) for shift in shifts]

    for i in range(1, entry_count):
        workers_shifts.append(worker_shift_factory(worker=workers[i-1], shift=shifts[i-1], day=f'2021-01-{i}'))

    with app.app_context():
        workers_shifts = [db.session.merge(worker_shift) for worker_shift in workers_shifts]

    url = (
        f"/api/v1/workers-shifts-aggregate?"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
    )

    response = test_client.get(url, follow_redirects=True)

    assert response_util.parse_data(response) == {
        datetime.datetime.strftime(ws.day, '%Y-%m-%d'): {
            'shift_count': 1,
        }
        for ws in workers_shifts
    }
