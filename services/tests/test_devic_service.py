# type: ignore
from services.device_service import (
    get_all_devices,
    update_devices,
    create_history_for_device,
)
from tests.factories import DeviceFactory
from tests.mock_data.device_history import device_history
from models.history import History


class TestDevice:
    def test_get_devices(self) -> None:
        DeviceFactory.create()
        DeviceFactory.create()
        DeviceFactory.create()
        devices = get_all_devices()
        assert devices
        assert len(devices) == 3

    def test_update(self, mocker) -> None:
        DeviceFactory.create()
        DeviceFactory.create()

        create_history_for_device_mock = mocker.patch(
            "services.device_service.create_history_for_device", return_value=None,
        )

        update_devices()
        assert create_history_for_device_mock.call_count == 2

    def test_create_history_for_device(self, mocker) -> None:
        device = DeviceFactory.create()
        get_history_for_device_mock = mocker.patch(
            "services.device_service.get_history_for_device",
            return_value=device_history,
        )

        history = create_history_for_device(device)
        assert history
        assert len(history) == 83

        get_history_for_device_mock.assert_called_once()

    def test_create_history_for_device_non_unique(self, mocker) -> None:
        device = DeviceFactory.create()
        get_history_for_device_mock = mocker.patch(
            "services.device_service.get_history_for_device",
            return_value=device_history,
        )

        history = create_history_for_device(device)

        assert len(history) == 83

        create_history_for_device(device)

        count = History.get_history_count(point_id="123")
        assert count == 83

        assert get_history_for_device_mock.call_count == 2
