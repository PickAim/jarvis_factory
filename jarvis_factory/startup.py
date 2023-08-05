from jorm.market.infrastructure import Marketplace
from sqlalchemy.orm import Session

from jarvis_factory.support.constants import SUPPORTED_MARKETPLACES
from jarvis_factory.support.jdb.services import JDBServiceFactory


def init_supported_marketplaces(session: Session):
    marketplace_service = JDBServiceFactory.create_marketplace_service(session)
    for marketplace_name in SUPPORTED_MARKETPLACES:
        if marketplace_service.find_by_name(marketplace_name) is None:
            marketplace = Marketplace(marketplace_name)
            marketplace_service.create(marketplace)
