from jdu.db_tools.fill.db_fillers import StandardDBFiller
from jdu.db_tools.fill.wildberries_fillers import WildberriesDBFillerImpl
from jdu.db_tools.update.jorm_changer_impl import JormChangerImpl
from jdu.db_tools.update.user_info_changer import UserInfoChangerImpl
from jdu.providers.wildberries_providers import WildberriesDataProviderWithoutKeyImpl
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger

from sqlalchemy.orm import Session

from jarvis_factory.support.jdb.services import JDBServiceFactory
from jarvis_factory.support.jdu.initializers import WildberriesDBFillerInitializer, WildberriesDataProviderInitializer


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer(session) -> UserInfoChanger:
        account_service = JDBServiceFactory.create_account_service(session)
        user_service = JDBServiceFactory.create_user_service(session)
        token_service = JDBServiceFactory.create_token_service(session)
        return UserInfoChangerImpl(user_service, account_service, token_service)

    @staticmethod
    def create_jorm_changer(session, db_filler: StandardDBFiller) -> JORMChanger:
        unit_economy_service = JDBServiceFactory.create_economy_service(session)
        frequency_service = JDBServiceFactory.create_frequency_service(session)
        return JormChangerImpl(unit_economy_service, frequency_service, db_filler)

    @staticmethod
    def create_wb_db_filler(session: Session) -> WildberriesDBFillerImpl:
        return WildberriesDBFillerImpl(session,
                                       WildberriesDataProviderWithoutKeyImpl(WildberriesDataProviderInitializer),
                                       WildberriesDBFillerInitializer
                                       )
