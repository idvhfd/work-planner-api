import datetime
import logging

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import BadRequest
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from planner.app import db
from planner.models import Shift

logger = logging.getLogger(__name__)


class ShiftSchema(Schema):
    class Meta:
        type_ = 'shifts'
        self_view = 'api_app.shifts_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_app.shifts_list'
        strict = True

    id = fields.String(dump_only=True)
    start_time = fields.String()
    end_time = fields.String()


class ShiftListResource(ResourceList):
    """ GET api/v1/shifts/ """
    schema = ShiftSchema
    methods = ['GET', 'POST']
    data_layer = {
        'session': db.session,
        'model': Shift
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_collection(self, qs, kwargs, filters=None):
        shifts = Shift.query

        if qs.querystring.get('filter[start_time]'):
            start_time = qs.querystring.get('filter[start_time]')
            shifts = shifts.filter(Shift.start_time == start_time)

        if qs.querystring.get('filter[end_time]'):
            end_time = qs.querystring.get('filter[end_time]')
            shifts = shifts.filter(Shift.end_time == end_time)

        if qs.sorting:
            shifts = self._data_layer.sort_query(shifts, qs.sorting)

        count = shifts.count()
        shifts = self._data_layer.paginate_query(shifts, qs.pagination)

        return count, shifts

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def before_post(self, args, kwargs, data=None):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        try:
            start_time_dt = datetime.datetime.strptime(start_time, '%H:%M')
            end_time_dt = datetime.datetime.strptime(end_time, '%H:%M')
        except ValueError as e:
            raise BadRequest(
                detail='Start time or end time value is invalid. Accepted values are 24-hour clock time strings.'
                       'Example: "23:00", "14:00".'
                       f'Exception: {str(e)}.'
            )

        # Add 8 hour constraint per shift
        if end_time_dt < start_time_dt:
            end_time_dt += datetime.timedelta(days=1)

        if (end_time_dt - start_time_dt).total_seconds()/3600 != 8:
            raise BadRequest(detail='Shifts must be exactly 8 hours long')


class ShiftResource(ResourceDetail):
    """ GET api/v1/shifts/<id> """
    schema = ShiftSchema
    methods = ['GET', 'PATCH', 'DELETE']
    data_layer = {
        'session': db.session,
        'model': Shift,
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs)

    def before_patch(self, args, kwargs, data=None):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        try:
            datetime.datetime.strptime(start_time, '%H:%M')
            datetime.datetime.strptime(end_time, '%H:%M')
        except ValueError as e:
            raise BadRequest(
                detail='Start time or end time value is invalid. Accepted values are 24-hour clock time strings.'
                       'Example: "23:00", "14:00".'
                       f'Exception: {str(e)}.'
            )

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
