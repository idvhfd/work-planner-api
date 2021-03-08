from planner.app import db
from planner.models import Base


class Worker(Base):
    __tablename__ = 'workers'

    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
