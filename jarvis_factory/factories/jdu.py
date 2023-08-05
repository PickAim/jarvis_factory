from jdu.db_tools.update.jorm.jorm_changer_impl import JORMChangerImpl
from jdu.db_tools.update.user_info_changer import UserInfoChangerImpl
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger
from sqlalchemy.orm import Session

from jarvis_factory.support.jdb.services import JDBServiceFactory
from jarvis_factory.support.jdu.initializers import JORMChangerInitializerImpl


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer(session) -> UserInfoChanger:
        account_service = JDBServiceFactory.create_account_service(session)
        user_service = JDBServiceFactory.create_user_service(session)
        token_service = JDBServiceFactory.create_token_service(session)
        return UserInfoChangerImpl(user_service, account_service, token_service)

    @staticmethod
    def create_jorm_changer(session: Session) -> JORMChanger:
        return JORMChangerImpl(session, JORMChangerInitializerImpl)
