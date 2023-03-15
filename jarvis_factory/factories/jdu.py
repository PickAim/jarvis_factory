from jorm.jarvis.db_update import UserInfoChanger, JORMChanger

from jarvis_factory.temp.temp_db import TempUserInfoChanger, TempJORMChanger


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer() -> UserInfoChanger:
        return TempUserInfoChanger()

    @staticmethod
    def create_jorm_changer() -> JORMChanger:
        return TempJORMChanger()
