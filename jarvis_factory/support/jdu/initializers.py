import requests
from jdu.db_tools.fill.db_fillers_impl import StandardDBFillerImpl
from jdu.db_tools.fill.initializers import DBFillerInitializer
from jdu.db_tools.update.jorm.base import InitInfo, JORMChangerBase
from jdu.db_tools.update.jorm.initializers import JORMChangerInitializer
from jdu.db_tools.update.user.base import UserInfoChangerBase
from jdu.db_tools.update.user.initializers import UserInfoChangerInitializer
from jdu.providers.initializers import DataProviderInitializer
from jdu.providers.wildberries_providers import WildberriesUserMarketDataProviderImpl, \
    WildberriesDataProviderWithoutKeyImpl
from jdu.support.commission.wildberries_commission_resolver import WildberriesCommissionResolver
from jdu.support.constant import WILDBERRIES_NAME
from requests.adapters import HTTPAdapter

from jarvis_factory.support.jdb.services import JDBServiceFactory


class WildberriesDataProviderInitializer(DataProviderInitializer):
    def additional_init_data_provider(self, data_provider):
        data_provider.commission_resolver = WildberriesCommissionResolver()
        data_provider.session = requests.Session()
        __adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
        data_provider.session.mount('https://', __adapter)

    def get_marketplace_name(self) -> str:
        return WILDBERRIES_NAME


class WildberriesDBFillerInitializer(DBFillerInitializer):

    def get_marketplace_name(self) -> str:
        return WILDBERRIES_NAME


INITIALIZER_MAP: dict[str, InitInfo] = {
    WILDBERRIES_NAME: InitInfo(WildberriesUserMarketDataProviderImpl,
                               WildberriesDataProviderWithoutKeyImpl,
                               StandardDBFillerImpl,
                               WildberriesDataProviderInitializer,
                               WildberriesDBFillerInitializer)
}


class JORMChangerInitializerImpl(JORMChangerInitializer):
    def _init_something(self, jorm_changer: JORMChangerBase):
        session = self.session
        jorm_changer.economy_service = JDBServiceFactory.create_economy_service(session)
        jorm_changer.frequency_service = JDBServiceFactory.create_frequency_service(session)
        jorm_changer.user_service = JDBServiceFactory.create_user_service(session)
        jorm_changer.user_item_service = JDBServiceFactory.create_user_items_service(session)
        jorm_changer.marketplace_service = JDBServiceFactory.create_marketplace_service(session)
        jorm_changer.warehouse_service = JDBServiceFactory.create_warehouse_service(session)
        jorm_changer.category_service = JDBServiceFactory.create_category_service(session)
        jorm_changer.niche_service = JDBServiceFactory.create_niche_service(session)
        jorm_changer.product_card_service = JDBServiceFactory.create_product_card_service(session)
        jorm_changer.initializing_mapping = INITIALIZER_MAP


class UserInfoChangerInitializerImpl(UserInfoChangerInitializer):
    def _init_something(self, user_info_changer: UserInfoChangerBase):
        session = self.session
        user_info_changer.user_service = JDBServiceFactory.create_user_service(session)
        user_info_changer.token_service = JDBServiceFactory.create_token_service(session)
        user_info_changer.account_service = JDBServiceFactory.create_account_service(session)
