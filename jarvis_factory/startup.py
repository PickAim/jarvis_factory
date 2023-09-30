from jorm.market.infrastructure import Marketplace
from sqlalchemy.orm import Session

from jarvis_factory.support.constants import SUPPORTED_MARKETPLACES, ECONOMY_CONSTANTS
from jarvis_factory.support.jdb.services import JDBServiceFactory


def init_supported_marketplaces(session: Session) -> list[int]:
    marketplace_service = JDBServiceFactory.create_marketplace_service(session)
    economy_constants_service = JDBServiceFactory.create_economy_constants_service(session)
    marketplace_ids: list[int] = []
    for marketplace_name in SUPPORTED_MARKETPLACES:
        if marketplace_service.find_by_name(marketplace_name) is None:
            marketplace = Marketplace(marketplace_name)
            marketplace_service.create(marketplace)
        found_info: tuple[Marketplace, int] = marketplace_service.find_by_name(marketplace_name)
        economy_constants_service.upsert_constants(found_info[1], ECONOMY_CONSTANTS[marketplace_name])
        marketplace_ids.append(found_info[1])
    return marketplace_ids
