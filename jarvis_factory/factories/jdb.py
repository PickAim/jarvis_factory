from jarvis_db.access.fill.standard_filler_impl import StandardDbFillerImpl
from jarvis_db.access.jorm_changer import JormChangerImpl
from jarvis_db.access.jorm_collector_impl import JormCollectorImpl
from jarvis_db.access.user_info_changer import UserInfoChangerImpl
from jarvis_db.access.user_info_collector_impl import UserInfoCollectorImpl
from jorm.jarvis.db_access import JORMCollector, UserInfoCollector
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger
from sqlalchemy.orm import Session

from jarvis_factory.factories.jdu import JDUClassesFactory
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
        simple_economy_service = JDBServiceFactory.create_economy_service(session)
        transit_economy_service = JDBServiceFactory.create_transit_service(session)
        user_items_service = JDBServiceFactory.create_user_items_service(session)
        green_trade_zone_service = JDBServiceFactory.create_green_trade_zone_service(session)
        niche_characteristics_service = JDBServiceFactory.create_niche_characteristics_service(session)
        return JormCollectorImpl(
            economy_constants_service=JDBServiceFactory.create_economy_constants_service(session),
            marketplace_service=marketplace_service,
            niche_service=niche_service,
            category_service=category_service,
            warehouse_service=warehouse_service,
            economy_service=simple_economy_service,
            transit_service=transit_economy_service,
            user_items_service=user_items_service,
            green_trade_zone_service=green_trade_zone_service,
            niche_characteristics_service=niche_characteristics_service
        )

    @staticmethod
    def create_user_info_changer(session: Session) -> UserInfoChanger:
        return UserInfoChangerImpl(
            token_service=JDBServiceFactory.create_token_service(session),
            account_service=JDBServiceFactory.create_account_service(session),
            user_service=JDBServiceFactory.create_user_service(session)
        )

    @staticmethod
    def create_jorm_changer(session: Session, marketplace_id: int, user_id: int) -> JORMChanger:
        return JormChangerImpl(
            economy_constants_service=JDBServiceFactory.create_economy_constants_service(session),
            category_service=JDBServiceFactory.create_category_service(session),
            niche_characteristics_service=JDBServiceFactory.create_niche_characteristics_service(session),
            niche_service=JDBServiceFactory.create_niche_service(session),
            product_card_service=JDBServiceFactory.create_product_card_service(session),
            product_history_service=JDBServiceFactory.create_product_history_service(session),
            economy_service=JDBServiceFactory.create_economy_service(session),
            transit_service=JDBServiceFactory.create_transit_service(session),
            user_items_service=JDBServiceFactory.create_user_items_service(session),
            green_trade_zone_service=JDBServiceFactory.create_green_trade_zone_service(session),
            data_provider_without_key=JDUClassesFactory.create_data_provider_without_key(session, marketplace_id),
            user_market_data_provider=JDUClassesFactory.create_user_market_data_provider(session,
                                                                                         marketplace_id, user_id),
            standard_filler=StandardDbFillerImpl(marketplace_id, JDBServiceFactory.create_warehouse_service(session))
        )


