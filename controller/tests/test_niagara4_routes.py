# type: ignore
from datetime import datetime
import pytest
from tests.factories import HistoryFactory, UserFactory
from conftest import logged_in_client
from tests.mock_data.device_history import device_history
from models.history import History


class TestNiagara4:
    @pytest.fixture()
    def niagara4_mock_sites(self, mocker):
        return mocker.patch(
            "controller.niagara4_routes.get_all_sites",
            return_value=dict(building1="somthing", building2="something"),
        )

    @pytest.fixture()
    def niagara4_mock_create_history(self, mocker):
        return mocker.patch(
            "controller.niagara4_routes.create_history_for_device", return_value=None
        )

    def test_get_sites(self, niagara4_mock_sites) -> None:
        user = UserFactory.create()
        with logged_in_client(user) as client:
            resp = client.get("/sites")
            assert resp.status_code == 200
            assert resp.json == {"names": ["building1", "building2"]}

    def test_create_history(self, niagara4_mock_create_history) -> None:
        user = UserFactory.create()
        history = [
            HistoryFactory.create(point_id="a123"),
            HistoryFactory.create(point_id="a123"),
            HistoryFactory.create(point_id="a123"),
        ]

        with logged_in_client(user) as client:
            resp = client.post("/history/a123", json={})
            assert resp.status_code == 200
            assert len(resp.json) == len(history)
            niagara4_mock_create_history.assert_called_once()

    def test_history_route(self):
        user = UserFactory.create()
        History.create_device_history(device_history)

        point_id = "123"
        from_time = str(datetime(2020, 2, 24).date())
        to_time = str(datetime(2020, 2, 25).date())

        with logged_in_client(user) as client:
            resp = client.get(
                f"/history?point_id={point_id}&from_time={from_time}&to_time={to_time}"
            )

        assert len(resp.json) == 83

    def test_create_history_for_device(self) -> None:
        user = UserFactory.create()
        history = device_history[0:10]
        for h in history:
            h["ts"] = str(h["ts"])

        with logged_in_client(user) as client:
            resp = client.post("/history", json=history)
            assert resp.status_code == 204
