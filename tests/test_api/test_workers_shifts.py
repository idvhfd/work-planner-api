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

    assert response_util.parse_data(response) == [
        {
            'type': 'workers_shifts',
            'id': str(worker_shift.id),
            'attributes': {
                'day': datetime.strftime(worker_shift.day, '%Y-%m-%d'),
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

    assert response_util.parse_data(response) == {
        'type': 'workers_shifts',
        'id': str(worker_shift.id),
        'attributes': {
            'day': datetime.strftime(worker_shift.day, '%Y-%m-%d'),
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


def test_post_workers_shifts(app, test_client, regular_worker_shift, regular_worker, regular_shift):
    url = '/api/v1/workers-shifts/'

    with app.app_context():
        regular_worker = db.session.merge(regular_worker)
        regular_shift = db.session.merge(regular_shift)

    payload = {
        'data': {
            'type': 'workers_shifts',
            'attributes': {
                'day': '2021-01-01',
            },
            'relationships': {
                'worker': {
                    'data': {
                        'type': 'workers',
                        'id': f'{regular_worker.id}'
                    }
                },
                'shift': {
                    'data': {
                        'type': 'shifts',
                        'id': f'{regular_shift.id}'
                    }
                }
            }
        }
    }

    response = test_client.post(
        url,
        json=payload,
        follow_redirects=True,
        headers={'Content-Type': 'application/vnd.api+json'}
    )

    assert response.status_code == 400
    assert response_util.parse_errors(response) == [
        {
            'detail': 'A worker may not have more than one shift per day',
            'status': '400',
            'title': 'Bad request'
        },
    ]
