from jarvis_db.repositores.mappers.market.infrastructure import CategoryTableToJormMapper, NicheTableToJormMapper, \
    WarehouseTableToJormMapper, MarketplaceTableToJormMapper
from jarvis_db.repositores.mappers.market.items import ProductHistoryTableToJormMapper, ProductTableToJormMapper
from jarvis_db.repositores.mappers.market.items.leftover_mappers import LeftoverTableToJormMapper
from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.mappers.market.person.token_mappers import TokenTableMapper
from jarvis_db.repositores.mappers.market.service import EconomyResultTableToJormMapper, \
    EconomyRequestTableToJormMapper, FrequencyRequestTableToJormMapper
from jarvis_db.repositores.market.infrastructure import CategoryRepository, WarehouseRepository, NicheRepository, \
    MarketplaceRepository
from jarvis_db.repositores.market.items import ProductHistoryRepository, ProductCardRepository
from jarvis_db.repositores.market.items.leftover_repository import LeftoverRepository
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.repositores.market.person.token_repository import TokenRepository
from jarvis_db.repositores.market.service import EconomyRequestRepository, EconomyResultRepository, \
    FrequencyRequestRepository, FrequencyResultRepository
from jarvis_db.services.market.infrastructure.category_service import CategoryService
from jarvis_db.services.market.infrastructure.marketplace_service import MarketplaceService
from jarvis_db.services.market.infrastructure.niche_service import NicheService
from jarvis_db.services.market.infrastructure.warehouse_service import WarehouseService
from jarvis_db.services.market.items.leftover_service import LeftoverService
from jarvis_db.services.market.items.product_card_service import ProductCardService
from jarvis_db.services.market.items.product_history_service import ProductHistoryService
from jarvis_db.services.market.items.product_history_unit_service import ProductHistoryUnitService
from jarvis_db.services.market.person import UserService, AccountService, TokenService
from jarvis_db.services.market.service.economy_service import EconomyService
from jarvis_db.services.market.service.frequency_service import FrequencyService
from sqlalchemy.orm import Session


class JDBServiceFactory:
    @staticmethod
    def create_marketplace_service(session: Session) -> MarketplaceService:
        return MarketplaceService(MarketplaceRepository(session),
                                  MarketplaceTableToJormMapper(WarehouseTableToJormMapper()))

    @staticmethod
    def create_category_service(session: Session) -> CategoryService:
        niche_mapper = NicheTableToJormMapper()
        return CategoryService(
            CategoryRepository(session),
            CategoryTableToJormMapper(niche_mapper),
        )

    @staticmethod
    def create_niche_service(session: Session) -> NicheService:
        niche_mapper = NicheTableToJormMapper()
        return NicheService(NicheRepository(session), niche_mapper)

    @staticmethod
    def create_warehouse_service(session: Session) -> WarehouseService:
        return WarehouseService(WarehouseRepository(session), WarehouseTableToJormMapper())

    @staticmethod
    def create_economy_service(session: Session) -> EconomyService:
        return EconomyService(
            EconomyRequestRepository(session),
            EconomyResultRepository(session),
            EconomyResultTableToJormMapper(EconomyRequestTableToJormMapper()),
            JDBServiceFactory.create_category_service(session),
            JDBServiceFactory.create_niche_service(session),
            JDBServiceFactory.create_warehouse_service(session),
        )

    @staticmethod
    def create_frequency_service(session: Session) -> FrequencyService:
        return FrequencyService(
            FrequencyRequestRepository(session),
            NicheRepository(session),
            FrequencyResultRepository(session),
            FrequencyRequestTableToJormMapper(),
        )

    @staticmethod
    def create_product_card_service(session: Session) -> ProductCardService:
        product_history_service = JDBServiceFactory.create_product_history_service(session)
        return ProductCardService(ProductCardRepository(session),
                                  product_history_service,
                                  ProductTableToJormMapper())

    @staticmethod
    def create_product_history_service(session: Session) -> ProductHistoryService:
        unit_service = JDBServiceFactory.create_product_history_unit_service(session)
        return ProductHistoryService(
            unit_service,
            LeftoverService(
                LeftoverRepository(session), WarehouseRepository(session), unit_service
            ),
            ProductHistoryRepository(session),
            ProductHistoryTableToJormMapper(LeftoverTableToJormMapper()),
        )

    @staticmethod
    def create_product_history_unit_service(session: Session) -> ProductHistoryUnitService:
        return ProductHistoryUnitService(ProductHistoryRepository(session))

    @staticmethod
    def create_token_service(session: Session) -> TokenService:
        return TokenService(TokenRepository(session), TokenTableMapper())

    @staticmethod
    def create_user_service(session: Session) -> UserService:
        return UserService(UserRepository(session), UserTableToJormMapper())

    @staticmethod
    def create_account_service(session: Session) -> AccountService:
        return AccountService(AccountRepository(session), AccountTableToJormMapper())
