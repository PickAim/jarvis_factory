from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.mappers.market.person.token_mappers import TokenTableMapper
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.repositores.market.person.token_repository import TokenRepository
from jarvis_db.services.market.person import TokenService
from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger

from jdu.db_tools.update.user_info_changer import UserInfoChangerImpl
from jarvis_factory.temp.temp_db import TempJORMChanger


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer(session) -> UserInfoChanger:
        account_service = AccountService(AccountRepository(session), AccountTableToJormMapper())
        user_service = UserService(UserRepository(session), UserTableToJormMapper())
        token_service = TokenService(TokenRepository(session), TokenTableMapper())
        return UserInfoChangerImpl(user_service, account_service, token_service)

    @staticmethod
    def create_jorm_changer() -> JORMChanger:
        return TempJORMChanger()
