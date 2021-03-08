from planner.api.workers import WorkerResource, WorkerListResource
from planner.api.shifts import ShiftResource, ShiftListResource
from planner.api.worker_shifts import WorkerShiftResource, WorkerShiftListResource, WorkerShiftRelationshipsResource


def register_routes(api):
    # register workers/
    api.route(WorkerListResource, 'workers_list', 'v1/workers/')
    api.route(WorkerResource, 'workers_detail', 'v1/workers/<int:id>')

    # register shifts/
    api.route(ShiftListResource, 'shifts_list', 'v1/shifts/')
    api.route(ShiftResource, 'shifts_detail', 'v1/shifts/<int:id>')

    # register workers-shifts/
    api.route(WorkerShiftListResource, 'workers_shifts_list', 'v1/workers-shifts/')
    api.route(WorkerShiftResource, 'workers_shifts_detail', 'v1/workers-shifts/<int:id>')
    api.route(
        WorkerShiftRelationshipsResource, 'workers_shifts_worker', 'v1/workers-shifts/<int:id>/relationships/worker'
    )
    api.route(
        WorkerShiftRelationshipsResource, 'workers_shifts_shift', 'v1/workers-shifts/<int:id>/relationships/shift'
    )
