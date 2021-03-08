from planner.app import db
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
