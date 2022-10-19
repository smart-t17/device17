# type: ignore
import pytest
from services.niagara4_service import get_all_sites


class TestNiagara4:
    @pytest.fixture()
    def niagara4_mock_sites(self, mocker):
        return mocker.patch("services.niagara4_service.session")

    def test_get_sites(self, niagara4_mock_sites) -> None:
        assert get_all_sites() is not None
