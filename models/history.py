from typing import Any, Dict, List
from datetime import datetime
from app import db, logger
from common.database import db_session
from sqlalchemy import Index
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


class History(db.Model):  # type: ignore
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    point_id = db.Column(db.String(255), index=True)

    ts = db.Column(db.DateTime(), nullable=False, index=True)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(255), nullable=False)

    __table_args__ = (db.UniqueConstraint("point_id", "ts"),)
    Index("idx_history_point", point_id, ts)

    @classmethod
    def get_device_history(cls, point_id: int) -> List["History"]:
        with db_session() as session:
            history = (
                session.query(cls).filter(cls.point_id == point_id).all()
            )  # type: List["History"]
            return history

    @classmethod
    def create_device_history(cls, points: List[Dict[Any, Any]]) -> List["History"]:
        """
        creating device history
        TODO: going one over one here to create the data points. 
        Might be too much and it's better to use add_all instead add
        The reason to use is that it's easier to catch unique rows here and skip them
        """
        with db_session() as session:
            data_points = []
            for data_point in points:
                try:
                    data_point = cls(**data_point)
                    session.add(data_point)
                    session.commit()
                    data_points.append(data_point)
                except IntegrityError:
                    logger.info("Already inserted this data point. Skipping")
                    session.rollback()
                    continue
                except Exception as error:
                    logger.error(error)
                    raise error

            return data_points

    @classmethod
    def get_history(
        cls, point_id: str, from_time: datetime, to_time: datetime
    ) -> List["History"]:
        with db_session() as session:
            history = (
                session.query(cls.ts, cls.quantity)
                .filter(
                    cls.point_id == point_id,
                    and_(cls.ts > from_time, cls.ts < to_time,),
                )
                .all()
            )  # type: List["History"]
            return history

    @classmethod
    def get_history_count(cls, point_id: str) -> int:
        with db_session() as session:
            count = (
                session.query(cls).filter(cls.point_id == point_id).count()
            )  # type: int
            return count
