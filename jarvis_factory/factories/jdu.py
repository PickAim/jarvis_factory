from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.mappers.market.person.token_mappers import TokenTableMapper
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.repositores.market.person.token_repository import TokenRepository
from jarvis_db.services.market.person import TokenService
from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService
from jarvis_factory.factories.jdb import JDBClassesFactory
from jdu.db_tools.fill.db_fillers import StandardDBFiller
from jdu.db_tools.fill.wildberries_fillers import WildberriesDBFillerImpl
from jdu.db_tools.update.jorm_changer_impl import JormChangerImpl
from jdu.db_tools.update.user_info_changer import UserInfoChangerImpl
from jdu.providers.wildberries_providers import WildberriesDataProviderWithoutKeyImpl
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger

from sqlalchemy.orm import Session


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer(session) -> UserInfoChanger:
        account_service = AccountService(AccountRepository(session), AccountTableToJormMapper())
        user_service = UserService(UserRepository(session), UserTableToJormMapper())
        token_service = TokenService(TokenRepository(session), TokenTableMapper())
        return UserInfoChangerImpl(user_service, account_service, token_service)

    @staticmethod
    def create_jorm_changer(session, db_filler: StandardDBFiller) -> JORMChanger:
        unit_economy_service = JDBClassesFactory.create_economy_service(session)
        frequency_service = JDBClassesFactory.create_frequency_service(session)
        return JormChangerImpl(unit_economy_service, frequency_service, db_filler)

    @staticmethod
    def create_wb_db_filler(session: Session) -> WildberriesDBFillerImpl:
        return WildberriesDBFillerImpl(WildberriesDataProviderWithoutKeyImpl(), session)
