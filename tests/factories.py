import factory
from faker import Faker

from app import db
from models.user import User
from models.history import History
from models.device import Device
from models.building import Building
from models.point import Point

faker = Faker()
faker.seed_instance(4321)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    password = factory.Faker("password")
    is_active = True
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    user_role = 0


class BuildingFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore
    class Meta:
        model = Building
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    address = factory.Faker("address")
    client = factory.Faker("word")
    utility = factory.Faker("word")
    market = factory.Faker("word")
    sq_footage = factory.Faker("random_number")


class DeviceFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore
    class Meta:
        model = Device
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    unit = "kW"

    building = factory.SubFactory(BuildingFactory)


class PointFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore
    class Meta:
        model = Point
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    unit = "kW"

    device = factory.SubFactory(DeviceFactory)


class HistoryFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore
    class Meta:
        model = History
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    point_id = factory.Faker("word")
    ts = factory.Faker("date_time_between", start_date="-1d", end_date="now")
    quantity = factory.Faker("random_number")
    unit = "kW"
