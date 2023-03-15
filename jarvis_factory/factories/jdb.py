from jorm.jarvis.db_access import JORMCollector, UserInfoCollector

from jarvis_factory.temp.temp_db import TempUserInfoCollector, TempJORMCollector


class JDBClassesFactory:
    @staticmethod
    def create_user_info_collector() -> UserInfoCollector:
        return TempUserInfoCollector()

    @staticmethod
    def create_jorm_collector() -> JORMCollector:
        return TempJORMCollector()
