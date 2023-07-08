from jarvis_db.access.jorm_collector_impl import JormCollectorImpl
from jarvis_db.access.user_info_collector_impl import UserInfoCollectorImpl
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
from jarvis_db.services.market.person import TokenService
from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService
from jarvis_db.services.market.service.economy_service import EconomyService
from jarvis_db.services.market.service.frequency_service import FrequencyService
from jorm.jarvis.db_access import JORMCollector, UserInfoCollector
from sqlalchemy.orm import Session


class JDBClassesFactory:
    @staticmethod
    def create_user_info_collector(session) -> UserInfoCollector:
        account_service = AccountService(AccountRepository(session), AccountTableToJormMapper())
        user_service = UserService(UserRepository(session), UserTableToJormMapper())
        token_service = TokenService(TokenRepository(session), TokenTableMapper())
        return UserInfoCollectorImpl(account_service, user_service, token_service)

    @staticmethod
    def create_jorm_collector(session) -> JORMCollector:
        niche_service = JDBClassesFactory.create_niche_service(session)
        category_service = JDBClassesFactory.create_category_service(session)
        warehouse_service = JDBClassesFactory.create_warehouse_service(session)
        unit_economy_service = JDBClassesFactory.create_economy_service(session)
        frequency_service = JDBClassesFactory.create_frequency_service(session)
        return JormCollectorImpl(niche_service, category_service,
                                 warehouse_service, unit_economy_service, frequency_service)

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
            JDBClassesFactory.create_category_service(session),
            JDBClassesFactory.create_niche_service(session),
            JDBClassesFactory.create_warehouse_service(session),
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
        unit_service = ProductHistoryUnitService(ProductHistoryRepository(session))
        product_history_service = ProductHistoryService(
            unit_service,
            LeftoverService(
                LeftoverRepository(session), WarehouseRepository(session), unit_service
            ),
            ProductHistoryRepository(session),
            ProductHistoryTableToJormMapper(LeftoverTableToJormMapper()),
        )
        return ProductCardService(ProductCardRepository(session),
                                  product_history_service,
                                  ProductTableToJormMapper())
