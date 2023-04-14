from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService

from jorm.jarvis.db_access import JORMCollector, UserInfoCollector

from jarvis_factory.temp.temp_db import TempUserInfoCollector, TempJORMCollector


class JDBClassesFactory:
    @staticmethod
    def create_user_info_collector(session) -> UserInfoCollector:
        account_service = AccountService(AccountRepository(session), AccountTableToJormMapper())
        user_service = UserService(UserRepository(session), UserTableToJormMapper())
        return TempUserInfoCollector(user_service, account_service)

    @staticmethod
    def create_jorm_collector() -> JORMCollector:
        return TempJORMCollector()
