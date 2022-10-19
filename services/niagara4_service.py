from typing import Any, Dict, List
from app import config
from pyhaystack.client.niagara import Niagara4HaystackSession

session = Niagara4HaystackSession(
    uri=config.NIAGARA4_SERVER,
    username=config.NIAGARA4_USERNAME,
    password=config.NIAGARA4_PASSWORD,
    http_args=dict(tls_verify=False, debug=True),
    pint=False,
)


def get_site(site_name: str) -> Any:
    """
    return a site by name
    site_name example: S.~31430Broadway.elecMeter
    """
    op = session.get_entity(site_name)
    op.wait()
    site = op.result
    return site


def get_all_sites() -> Any:
    """
    returns all the sites we have
    """
    return session.sites


def get_history_for_device(
    device_name: str, rng: str = "today"
) -> List[Dict[Any, Any]]:
    """
    example device: 'S.~3575Madison.elecMeter.currentBuilding_Demand'
    """
    op = session.his_read(device_name, rng=rng)
    op.wait()
    site = op.result
    formatted_data = _format_data(site)
    return formatted_data


def _format_data(site: Any) -> List[Dict[Any, Any]]:
    formatted_data = []
    point_id = site.metadata["id"].name
    for row in site._row:
        formatted_data.append(
            dict(
                point_id=point_id,
                ts=row["ts"],
                quantity=row["val"].value,
                unit=row["val"].unit,
            )
        )
    return formatted_data
