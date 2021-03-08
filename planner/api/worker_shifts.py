from datetime import datetime
import logging

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound, BadRequest
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

from planner.app import db
from planner.models import WorkerShift, Worker, Shift

logger = logging.getLogger(__name__)


class WorkerShiftSchema(Schema):
    class Meta:
        type_ = 'workers_shifts'
        self_view = 'api_app.workers_shifts_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_app.workers_shifts_list'
        strict = True

    id = fields.String(dump_only=True)
    day = fields.DateTime()

    worker = Relationship(
        self_view='api_app.workers_shifts_worker',
        self_view_kwargs={'id': '<id>'},
        related_view='api_app.workers_detail',
        related_view_kwargs={'id': '<worker_id>'},
        include_resource_linkage=True,
        schema='WorkerSchema',
        type_='workers',
    )
    shift = Relationship(
        self_view='api_app.workers_shifts_shift',
        self_view_kwargs={'id': '<id>'},
        related_view='api_app.shifts_detail',
        related_view_kwargs={'id': '<shift_id>'},
        include_resource_linkage=True,
        schema='ShiftSchema',
        type_='shifts'
    )


class WorkerShiftListResource(ResourceList):
    """ GET, POST api/v1/workers-shifts/ """
    schema = WorkerShiftSchema
    methods = ['GET', 'POST']
    data_layer = {
        'session': db.session,
        'model': WorkerShift
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_collection(self, qs, kwargs, filters=None):
        workers_shifts = WorkerShift.query

        if qs.querystring.get('filter[worker_ids]'):
            worker_ids = qs.querystring.get('filter[worker_ids]')

            ids = [_id for _id in worker_ids.split(',')]
            workers_shifts = WorkerShift.query.filter(WorkerShift.worker_id.in_(ids))

        if qs.querystring.get('filter[shift_ids]'):
            shift_ids = qs.querystring.get('filter[shift_ids]')

            ids = [_id for _id in shift_ids.split(',')]
            workers_shifts = WorkerShift.query.filter(WorkerShift.shift_id.in_(ids))

        count = workers_shifts.count()
        workers_shifts = self._data_layer.paginate_query(workers_shifts, qs.pagination)

        return count, workers_shifts

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def before_post(self, args, kwargs, data=None):
        # Make sure both the worker and shift are provided in the post data
        try:
            worker_id = int(data.get('worker'))
            shift_id = int(data.get('shift'))
        except TypeError:
            raise BadRequest(detail='Could not read relationships')

        # Find the relationship objects in the database
        worker = Worker.query.filter(Worker.id == worker_id).one_or_none()
        if not worker:
            raise ObjectNotFound(detail='Worker not found')

        shift = Shift.query.get(shift_id)
        if not shift:
            raise ObjectNotFound(detail='Shift not found')

        day = data.get('day')
        try:
            datetime.strptime(day, '%Y-%m-%d')
        except ValueError as e:
            raise BadRequest(
                detail='"day" parameter needs to be a valid date string. Accepted format: "Y-%m-%d".'
                       'Example: "2021-01-01", "2021-12-05".'
                       f'Exception: {str(e)}.'
            )

        return super().before_post(args, kwargs, data)


class WorkerShiftResource(ResourceDetail):
    """ GET, DELETE api/v1/workers-shifts/<id> """
    schema = WorkerShiftSchema
    methods = ['GET', 'DELETE']
    data_layer = {
        'session': db.session,
        'model': WorkerShift,
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_object(self, kwargs, qs):
        worker_shift = WorkerShift.query.get(kwargs.get('id'))
        if not worker_shift:
            raise ObjectNotFound(detail='WorkerShift not found')

        return worker_shift

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def delete_object(self, kwargs):
        worker_shift = self.get_object(kwargs, None)
        self._data_layer.delete_object(worker_shift, kwargs)


class WorkerShiftRelationshipsResource(ResourceRelationship):
    """ GET api/v1/workers-shifts/<id>/relationships/<RELATIONSHIP_ITEM>/ """
    methods = ['GET']
    schema = WorkerShiftSchema
    data_layer = {
        'session': db.session,
        'model': WorkerShift
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
