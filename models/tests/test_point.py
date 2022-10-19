from models.point import Point
from tests.factories import PointFactory, DeviceFactory


class TestPoint:
    def test_get_point(self) -> None:
        point = PointFactory.create()
        res = Point.get_point(point.id)
        assert point == res

    def test_create_point(self) -> None:
        name = "point"
        unit = "kW"
        device = DeviceFactory.create()
        args = dict(name=name, unit=unit, device_id=device.id)
        point = Point.create_point(**args)
        assert point.name == name
        assert point.unit == unit

    def test_get_points(self) -> None:
        PointFactory.create()
        PointFactory.create()
        PointFactory.create()
        res = Point.get_points()
        assert res
        assert len(res) == 3

    def test_get_get_point_by_id(self) -> None:
        point = PointFactory.create()
        res = Point.get_point_by_id(point.id)
        assert res == point
