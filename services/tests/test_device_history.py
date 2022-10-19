# type: ignore
from datetime import datetime
from tests.mock_data.device_history import device_history
from models.history import History


class TestDeviceHistory:
    def test_create_device_history(self):
        data_points = History.create_device_history(device_history)
        assert len(data_points) == 83

    def test_get_history(self):
        History.create_device_history(device_history)

        point_id = "123"
        from_time = datetime(2020, 2, 24, 0, 0, 0)
        to_time = datetime(2020, 2, 24, 18, 30, 0)

        res = History.get_history(point_id, from_time, to_time)
        assert len(res) == 74
