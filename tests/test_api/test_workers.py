from planner.app import db
from tests import response_util


def test_get_workers(app, test_client, worker_factory):
    worker = worker_factory()

    with app.app_context():
        worker = db.session.merge(worker)

    url = '/api/v1/workers/'

    response = test_client.get(url, follow_redirects=True)
    assert response_util.parse_data(response) == [
        {
            'type': 'workers',
            'id': str(worker.id),
            'attributes': {
                'first_name': worker.first_name,
                'last_name': worker.last_name,
            },
            'links': {
                'self': f'/api/v1/workers/{worker.id}'
            }
        }
    ]


def test_get_one_worker(app, test_client, worker_factory):
    worker = worker_factory()

    with app.app_context():
        worker = db.session.merge(worker)

    url = f"/api/v1/workers/{worker.id}"

    response = test_client.get(url, follow_redirects=True)
    assert response_util.parse_data(response) == {
        'type': 'workers',
        'id': str(worker.id),
        'attributes': {
            'first_name': worker.first_name,
            'last_name': worker.last_name,
        },
        'links': {
            'self': f'/api/v1/workers/{worker.id}'
        }
    }
