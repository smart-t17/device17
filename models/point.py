from typing import Optional, List
from datetime import datetime
from app import db
from common.database import db_session


class Point(db.Model):  # type: ignore
    __tablename__ = "points"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(255))

    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    device = db.relationship("Device", backref="devices")

    @classmethod
    def get_point(cls, point_id: int) -> Optional["Point"]:
        with db_session() as session:
            point = (
                session.query(cls).filter(cls.id == point_id).one_or_none()
            )  # type: Optional[Point]
            return point

    @classmethod
    def create_point(cls, **args: str) -> "Point":
        with db_session() as session:
            point = cls(**args)
            session.add(point)
            session.commit()
            return point

    @classmethod
    def get_points(cls) -> List["Point"]:
        with db_session() as session:
            points = session.query(cls).all()  # type: List[Point]
            return points

    @classmethod
    def get_point_by_id(cls, point_id: int) -> "Point":
        with db_session() as session:
            point = (
                session.query(cls).filter(cls.id == point_id).one_or_none()
            )  # type: Point
            return point
