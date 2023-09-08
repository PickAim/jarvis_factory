from jarvis_calc.database_interactors.db_controller import DBController

from jarvis_factory.factories.jdb import JDBClassesFactory


class JCalcClassesFactory:
    @staticmethod
    def create_db_controller(session, marketplace_id: int = 0, user_id: int = 0) -> DBController:
        user_info_collector = JDBClassesFactory.create_user_info_collector(session)
        jorm_collector = JDBClassesFactory.create_jorm_collector(session)

        user_info_changer = JDBClassesFactory.create_user_info_changer(session)
        jorm_changer = JDBClassesFactory.create_jorm_changer(session, marketplace_id, user_id)
        return DBController(user_info_collector, jorm_collector, user_info_changer, jorm_changer)
