from typing import Optional
from datetime import datetime
from app import db
from common.database import db_session


class Building(db.Model):  # type: ignore
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    client = db.Column(db.String(255))
    utility = db.Column(db.String(255))
    market = db.Column(db.String(255))
    sq_footage = db.Column(db.Integer)

    @classmethod
    def get_building(cls, building_id: int) -> Optional["Building"]:
        with db_session() as session:
            building = (
                session.query(cls).filter(cls.building_id == building_id).one_or_none()
            )  # type: Optional["Building"]
            return building

    @classmethod
    def create_building(cls, **args: str) -> "Building":
        with db_session() as session:
            building = cls(**args)
            session.add(building)
            session.commit()
            return building
