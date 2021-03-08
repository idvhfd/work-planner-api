import logging

from flask_rest_jsonapi import ResourceDetail, ResourceList
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from planner.app import db
from planner.models import Worker

logger = logging.getLogger(__name__)


class WorkerSchema(Schema):
    class Meta:
        type_ = 'workers'
        self_view = 'api_app.workers_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_app.workers_list'
        strict = True

    id = fields.String(dump_only=True)
    first_name = fields.String()
    last_name = fields.String()


class WorkerListResource(ResourceList):
    """ GET api/v1/workers/ """
    schema = WorkerSchema
    methods = ['GET', 'POST']
    data_layer = {
        'session': db.session,
        'model': Worker
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_collection(self, qs, kwargs, filters=None):
        workers = Worker.query

        if qs.querystring.get('filter[first_name]'):
            first_name = qs.querystring.get('filter[first_name]')
            workers = workers.filter(Worker.first_name == first_name)

        if qs.querystring.get('filter[last_name]'):
            last_name = qs.querystring.get('filter[last_name]')
            workers = workers.filter(Worker.last_name == last_name)

        if qs.sorting:
            workers = self._data_layer.sort_query(workers, qs.sorting)

        count = workers.count()
        workers = self._data_layer.paginate_query(workers, qs.pagination)

        return count, workers

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class WorkerResource(ResourceDetail):
    """ GET api/v1/workers/<id> """
    schema = WorkerSchema
    methods = ['GET', 'PATCH', 'DELETE']
    data_layer = {
        'session': db.session,
        'model': Worker,
    }

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
