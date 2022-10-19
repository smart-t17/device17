from typing import Optional, List
from datetime import datetime
from app import db
from common.database import db_session


class Device(db.Model):  # type: ignore
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(255))

    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    building = db.relationship("Building", backref="buildings")

    @classmethod
    def get_device(cls, device_id: int) -> Optional["Device"]:
        with db_session() as session:
            device = (
                session.query(cls).filter(cls.device_id == device_id).one_or_none()
            )  # type: Optional[Device]
            return device

    @classmethod
    def create_device(cls, **args: str) -> "Device":
        with db_session() as session:
            device = cls(**args)
            session.add(device)
            session.commit()
            return device

    @classmethod
    def get_devices(cls) -> List["Device"]:
        with db_session() as session:
            devices = session.query(cls).all()  # type: List[Device]
            return devices

    @classmethod
    def get_device_by_id(cls, device_id: int) -> "Device":
        with db_session() as session:
            device = (
                session.query(cls).filter(cls.id == device_id).one_or_none()
            )  # type: Device
            return device
