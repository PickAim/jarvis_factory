from jdu.db_tools.update.jorm.jorm_changer_impl import JORMChangerImpl
from jdu.db_tools.update.user.user_info_changer import UserInfoChangerImpl
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger
from sqlalchemy.orm import Session

from jarvis_factory.support.jdu.initializers import JORMChangerInitializerImpl, UserInfoChangerInitializerImpl


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer(session) -> UserInfoChanger:
        return UserInfoChangerImpl(session, UserInfoChangerInitializerImpl)

    @staticmethod
    def create_jorm_changer(session: Session) -> JORMChanger:
        return JORMChangerImpl(session, JORMChangerInitializerImpl)
