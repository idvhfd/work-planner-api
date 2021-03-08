from planner.app import db
from planner.models import Base


class Shift(Base):
    __tablename__ = 'shifts'

    id = db.Column(db.BigInteger, primary_key=True)
    start_time = db.Column(db.Text, nullable=False)
    end_time = db.Column(db.Text, nullable=False)
