from fastapi import Depends
from jarvis_calc.database_interactors.db_controller import DBController
from jarvis_factory.db_context import DbContext

from jarvis_factory.factories.jdb import JDBClassesFactory
from jarvis_factory.factories.jdu import JDUClassesFactory

db_context = DbContext(connection_sting='sqlite:///test.db', echo=True)


def session_depend():
    with db_context.session() as session, session.begin():
        yield session


class JCalcClassesFactory:
    @staticmethod
    def create_db_controller(session=Depends(session_depend)) -> DBController:
        user_info_collector = JDBClassesFactory.create_user_info_collector(session)
        jorm_collector = JDBClassesFactory.create_jorm_collector()

        user_info_changer = JDUClassesFactory.create_user_info_changer(session)
        jorm_changer = JDUClassesFactory.create_jorm_changer()

        return DBController(user_info_collector, jorm_collector, user_info_changer, jorm_changer)
