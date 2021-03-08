from planner.app import db
from planner.models import Shift
from tests import response_util


def test_get_shifts(app, test_client, shift_factory):
    shift = shift_factory()

    with app.app_context():
        shift = db.session.merge(shift)

    url = '/api/v1/shifts/'

    response = test_client.get(url, follow_redirects=True)
    assert response_util.parse_data(response) == [
        {
            'type': 'shifts',
            'id': str(shift.id),
            'attributes': {
                'start_time': shift.start_time,
                'end_time': shift.end_time,
            },
            'links': {
                'self': f'/api/v1/shifts/{shift.id}'
            }
        }
    ]


def test_get_one_shift(app, test_client, shift_factory):
    shift = shift_factory()

    with app.app_context():
        shift = db.session.merge(shift)

    url = f"/api/v1/shifts/{shift.id}"

    response = test_client.get(url, follow_redirects=True)
    assert response_util.parse_data(response) == {
        'type': 'shifts',
        'id': str(shift.id),
        'attributes': {
            'start_time': shift.start_time,
            'end_time': shift.end_time,
        },
        'links': {
            'self': f'/api/v1/shifts/{shift.id}'
        }
    }


def test_post_shifts_hour_limit(app, test_client):
    url = '/api/v1/shifts/'

    payload = {
        'data': {
            'type': 'shifts',
            'attributes': {
                'start_time': '0:00',
                'end_time': '10:00'
            },
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
            'detail': 'Shifts must be exactly 8 hours long',
            'status': '400',
            'title': 'Bad request'
        },
    ]


def test_post_shifts(app, test_client):
    url = '/api/v1/shifts/'

    payload = {
        'data': {
            'type': 'shifts',
            'attributes': {
                'start_time': '0:00',
                'end_time': '8:00'
            },
        }
    }

    response = test_client.post(
        url,
        json=payload,
        follow_redirects=True,
        headers={'Content-Type': 'application/vnd.api+json'}
    )

    assert response.status_code == 201
    shift = Shift.query.one()
    assert response_util.parse_data(response) == {
        'id': str(shift.id),
        'type': 'shifts',
        'attributes': {
            'start_time': shift.start_time,
            'end_time': shift.end_time,
        },
        'links': {'self': f'/api/v1/shifts/{str(shift.id)}'},
    }
