import requests
from jdu.db_tools.fill.base import DBFiller
from jdu.db_tools.fill.initializers import DBFillerInitializer
from jdu.providers.initializers import DataProviderInitializer
from jdu.support.commission.wildberries_commission_resolver import WildberriesCommissionResolver
from requests.adapters import HTTPAdapter
from sqlalchemy.orm import Session

from jarvis_factory.support.jdb.services import JDBServiceFactory


class WildberriesDataProviderInitializer(DataProviderInitializer):
    WILDBERRIES_NAME = 'wildberries'

    def additional_init_data_provider(self, data_provider):
        data_provider.commission_resolver = WildberriesCommissionResolver()
        data_provider.session = requests.Session()
        __adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
        data_provider.session.mount('https://', __adapter)

    def get_marketplace_name(self) -> str:
        return self.WILDBERRIES_NAME


class WildberriesDBFillerInitializer(DBFillerInitializer):
    WILDBERRIES_NAME = 'wildberries'

    def get_marketplace_name(self) -> str:
        return self.WILDBERRIES_NAME

    def additional_init_db_filler(self, session: Session, db_filler: DBFiller):
        db_filler.marketplace_service = JDBServiceFactory.create_marketplace_service(session)
        db_filler.category_service = JDBServiceFactory.create_category_service(session)
        db_filler.niche_service = JDBServiceFactory.create_niche_service(session)

        db_filler.product_service = JDBServiceFactory.create_product_card_service(session)
        db_filler.warehouse_service = JDBServiceFactory.create_warehouse_service(session)
        db_filler.product_history_service = JDBServiceFactory.create_product_history_service(session)
