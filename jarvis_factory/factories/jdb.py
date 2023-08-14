from jarvis_db.access.jorm_collector_impl import JormCollectorImpl
from jarvis_db.access.user_info_collector_impl import UserInfoCollectorImpl
from jorm.jarvis.db_access import JORMCollector, UserInfoCollector

from jarvis_factory.support.jdb.services import JDBServiceFactory


class JDBClassesFactory:
    @staticmethod
    def create_user_info_collector(session) -> UserInfoCollector:
        account_service = JDBServiceFactory.create_account_service(session)
        user_service = JDBServiceFactory.create_user_service(session)
        token_service = JDBServiceFactory.create_token_service(session)
        return UserInfoCollectorImpl(account_service, user_service, token_service)

    @staticmethod
    def create_jorm_collector(session) -> JORMCollector:
        marketplace_service = JDBServiceFactory.create_marketplace_service(session)
        niche_service = JDBServiceFactory.create_niche_service(session)
        category_service = JDBServiceFactory.create_category_service(session)
        warehouse_service = JDBServiceFactory.create_warehouse_service(session)
        unit_economy_service = JDBServiceFactory.create_economy_service(session)
        frequency_service = JDBServiceFactory.create_frequency_service(session)
        user_items_service = JDBServiceFactory.create_user_items_service(session)
        return JormCollectorImpl(marketplace_service, niche_service, category_service,
                                 warehouse_service, unit_economy_service, frequency_service, user_items_service)
