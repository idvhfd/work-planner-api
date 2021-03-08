from datetime import datetime

from planner.app import db
from tests import response_util


def test_get_workers_shifts(app, test_client, regular_worker_shift):
    worker_shift = regular_worker_shift

    with app.app_context():
        worker_shift = db.session.merge(worker_shift)
        worker = worker_shift.worker
        shift = worker_shift.shift

    url = '/api/v1/workers-shifts'

    response = test_client.get(url, follow_redirects=True)
    timestamp_string = datetime.strftime(worker_shift.day, '%Y-%m-%dT%H:%M:%S%z')
    assert response_util.parse_data(response) == [
        {
            'type': 'workers_shifts',
            'id': str(worker_shift.id),
            'attributes': {
                'day': f"{timestamp_string[:-2]}:{timestamp_string[-2:]}",
            },
            'links': {
                'self': f'/api/v1/workers-shifts/{str(worker_shift.id)}'
            },
            'relationships': {
                'shift': {
                    'data': {
                        'id': str(shift.id),
                        'type': 'shifts'
                    },
                    'links': {
                        'related': f'/api/v1/shifts/{str(shift.id)}',
                        'self': f'/api/v1/workers-shifts/{str(worker_shift.id)}/relationships/shift'
                    }
                },
                'worker': {
                    'data': {
                        'id': str(worker.id),
                        'type': 'workers'
                    },
                    'links': {
                        'related': f'/api/v1/workers/{str(worker.id)}',
                        'self': f'/api/v1/workers-shifts/{str(worker_shift.id)}/relationships/worker'}
                }
            }
        }
    ]


def test_get_one_workers_shifts(app, test_client, regular_worker_shift):
    worker_shift = regular_worker_shift

    with app.app_context():
        worker_shift = db.session.merge(worker_shift)
        worker = worker_shift.worker
        shift = worker_shift.shift

    url = f"/api/v1/workers-shifts/{worker_shift.id}"

    response = test_client.get(url, follow_redirects=True)
    timestamp_string = datetime.strftime(worker_shift.day, '%Y-%m-%dT%H:%M:%S%z')
    assert response_util.parse_data(response) == {
        'type': 'workers_shifts',
        'id': str(worker_shift.id),
        'attributes': {
            'day': f"{timestamp_string[:-2]}:{timestamp_string[-2:]}",
        },
        'links': {
            'self': f'/api/v1/workers-shifts/{str(worker_shift.id)}'
        },
        'relationships': {
            'shift': {
                'data': {
                    'id': str(shift.id),
                    'type': 'shifts'
                },
                'links': {
                    'related': f'/api/v1/shifts/{str(shift.id)}',
                    'self': f'/api/v1/workers-shifts/{str(worker_shift.id)}/relationships/shift'
                }
            },
            'worker': {
                'data': {
                    'id': str(worker.id),
                    'type': 'workers'
                },
                'links': {
                    'related': f'/api/v1/workers/{str(worker.id)}',
                    'self': f'/api/v1/workers-shifts/{str(worker_shift.id)}/relationships/worker'}
            }
        }
    }
