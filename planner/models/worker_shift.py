from sqlalchemy import ForeignKey

from planner.app import db
from planner.models import Base


class WorkerShift(Base):
    __tablename__ = 'workers_shifts'

    id = db.Column(db.BigInteger, primary_key=True)
    day = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

    worker_id = db.Column(db.BigInteger, ForeignKey('workers.id', ondelete='CASCADE'), nullable=False)
    shift_id = db.Column(db.BigInteger, ForeignKey('shifts.id', ondelete='CASCADE'), nullable=False)

    worker = db.relationship('Worker', foreign_keys=worker_id)
    shift = db.relationship('Shift', foreign_keys=shift_id)
