from jdu.db_tools.fill.base import DBFiller
from jdu.db_tools.fill.initializers import DBFillerInitializer
from sqlalchemy.orm import Session

from jarvis_factory.support.jdb.services import JDBServiceFactory


class WildberriesDBFillerInitializer(DBFillerInitializer):
    WILDBERRIES_NAME = 'wildberries'

    def get_marketplace_name(self) -> str:
        return self.WILDBERRIES_NAME

    def additional_init_db_filler(self, session: Session, db_filler: DBFiller):
        db_filler.marketplace_service = JDBServiceFactory.create_marketplace_service(session)
        db_filler.category_service = JDBServiceFactory.create_category_service(session)
        db_filler.niche_service = JDBServiceFactory.create_niche_service(session)

        db_filler.product_service = JDBServiceFactory.create_product_card_service(session)
        db_filler.history_unit_service = JDBServiceFactory.create_product_history_unit_service(session)
        db_filler.warehouse_service = JDBServiceFactory.create_warehouse_service(session)
        db_filler.product_history_service = JDBServiceFactory.create_product_history_service(session)
