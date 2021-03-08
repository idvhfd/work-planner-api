import datetime
import logging

from flask import request, jsonify
from flask.blueprints import Blueprint
from flask_rest_jsonapi.api import jsonapi_exception_formatter
from sqlalchemy import func

from planner.app import db
from planner.models import WorkerShift


workers_shifts_stats = Blueprint('workers_shifts_stats', __name__)
logger = logging.getLogger(__name__)


def format_date(d: datetime.datetime) -> str:
    return datetime.datetime.strftime(d, '%Y-%m-%d')


@workers_shifts_stats.route('/api/v1/workers-shifts-aggregate', methods=['GET'])
@jsonapi_exception_formatter
def get_shifts_by_day():
    """
    Helper controller that allows a prospective user to retrieve the number of worker shifts scheduled in a given timeframe.
    If no timeframe is given, it defaults to the past 30 days.

    data = {
        "01/12": {"count": 2},
        "01/13": {"count": 3},
    }
    """
    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
    end_date = datetime.datetime.now(datetime.timezone.utc)

    start_date_param = request.args.get('start_date')
    end_date_param = request.args.get('end_date')

    if start_date_param:
        try:
            start_date = datetime.datetime.strptime(start_date_param, '%Y-%m-%d')
            start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        except (TypeError, ValueError):
            pass

    if end_date_param:
        try:
            end_date = datetime.datetime.strptime(end_date_param, '%Y-%m-%d')
            end_date = end_date.replace(tzinfo=datetime.timezone.utc)
        except (TypeError, ValueError):
            pass

    worker_shifts_in_period = (
        db.session.query(
            func.date_trunc('day', WorkerShift.day).label('day'),
            func.count(WorkerShift.id),
        )
        .filter(WorkerShift.day >= start_date)
        .filter(WorkerShift.day <= end_date)
        .group_by('day')
        .order_by('day')
        .all()
    )

    return jsonify({
        'data': {
            format_date(ws[0]): {
                'shift_count': ws[1],
            }
            for ws in worker_shifts_in_period
        }
    })
