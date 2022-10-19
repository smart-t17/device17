from typing import List, Any
from models.device import Device
from models.history import History
from services.niagara4_service import get_history_for_device
from datetime import datetime

"""
example: This is how you would get the data for devices from date to date:
from_date = datetime(2020,3,1)
to_date = datetime.now()
update_devices_from_to(from_date=from_date,to_date=to_date)
"""


def get_all_devices() -> List[Device]:
    return Device.get_devices()


def create_history_for_device(device: Device, rng: Any = "today") -> List[History]:
    data = get_history_for_device(device_name=device.name, rng=rng)
    device_history = History.create_device_history(data)
    return device_history


def update_devices(rng: Any = "today") -> None:
    devices = get_all_devices()
    for device in devices:
        create_history_for_device(device, rng)


def update_devices_from_to(from_date: datetime, to_date: datetime) -> None:
    rng = _range_variable(from_date=from_date, to_date=to_date)
    update_devices(rng)


def _range_variable(from_date: datetime, to_date: datetime) -> str:
    from_date_str = str(from_date.date())
    to_date_str = str(to_date.date())
    return f"{from_date_str},{to_date_str}"
