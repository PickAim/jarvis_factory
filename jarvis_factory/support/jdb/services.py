from jarvis_db.factories.services import create_category_service, create_marketplace_service, create_niche_service, \
    create_warehouse_service, create_economy_service, create_product_card_service, \
    create_product_history_service, create_token_service, create_user_service, create_account_service, \
    create_user_items_service, create_transit_economy_service
from jarvis_db.services.market.infrastructure.category_service import CategoryService
from jarvis_db.services.market.infrastructure.marketplace_service import MarketplaceService
from jarvis_db.services.market.infrastructure.niche_service import NicheService
from jarvis_db.services.market.infrastructure.warehouse_service import WarehouseService
from jarvis_db.services.market.items.product_card_service import ProductCardService
from jarvis_db.services.market.items.product_history_service import ProductHistoryService
from jarvis_db.services.market.person import UserService, AccountService, TokenService
from jarvis_db.services.market.person.user_items_service import UserItemsService
from jarvis_db.services.market.service.economy_service import EconomyService
from jarvis_db.services.market.service.transit_economy_service import TransitEconomyService
from sqlalchemy.orm import Session


class JDBServiceFactory:
    @staticmethod
    def create_marketplace_service(session: Session) -> MarketplaceService:
        return create_marketplace_service(session)

    @staticmethod
    def create_category_service(session: Session) -> CategoryService:
        return create_category_service(session)

    @staticmethod
    def create_niche_service(session: Session) -> NicheService:
        return create_niche_service(session)

    @staticmethod
    def create_warehouse_service(session: Session) -> WarehouseService:
        return create_warehouse_service(session)

    @staticmethod
    def create_economy_service(session: Session) -> EconomyService:
        return create_economy_service(session)

    @staticmethod
    def create_transit_service(session: Session) -> TransitEconomyService:
        return create_transit_economy_service(session)

    @staticmethod
    def create_product_card_service(session: Session) -> ProductCardService:
        return create_product_card_service(session)

    @staticmethod
    def create_product_history_service(session: Session) -> ProductHistoryService:
        return create_product_history_service(session)

    @staticmethod
    def create_token_service(session: Session) -> TokenService:
        return create_token_service(session)

    @staticmethod
    def create_user_service(session: Session) -> UserService:
        return create_user_service(session)

    @staticmethod
    def create_user_items_service(session: Session) -> UserItemsService:
        return create_user_items_service(session)

    @staticmethod
    def create_account_service(session: Session) -> AccountService:
        return create_account_service(session)
