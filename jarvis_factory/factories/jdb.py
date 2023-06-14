from jarvis_db.repositores.mappers.market.infrastructure import NicheTableToJormMapper, WarehouseTableToJormMapper, \
    CategoryTableToJormMapper
from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.mappers.market.person.token_mappers import TokenTableMapper
from jarvis_db.repositores.mappers.market.service import EconomyRequestTableToJormMapper, \
    EconomyResultTableToJormMapper, FrequencyResultTableToJormMapper
from jarvis_db.repositores.market.infrastructure import NicheRepository, WarehouseRepository, CategoryRepository
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.repositores.market.person.token_repository import TokenRepository
from jarvis_db.repositores.market.service import EconomyRequestRepository, EconomyResultRepository, \
    FrequencyRequestRepository, FrequencyResultRepository
from jarvis_db.services.market.infrastructure.category_service import CategoryService
from jarvis_db.services.market.infrastructure.niche_service import NicheService
from jarvis_db.services.market.infrastructure.warehouse_service import WarehouseService
from jarvis_db.services.market.person import TokenService
from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService
from jarvis_db.services.market.service.economy_service import EconomyService
from jarvis_db.services.market.service.frequency_service import FrequencyService

from jorm.jarvis.db_access import JORMCollector, UserInfoCollector
from jarvis_db.access.user_info_collector_impl import UserInfoCollectorImpl
from jarvis_db.access.jorm_collector_impl import JormCollectorImpl


class JDBClassesFactory:
    @staticmethod
    def create_user_info_collector(session) -> UserInfoCollector:
        account_service = AccountService(AccountRepository(session), AccountTableToJormMapper())
        user_service = UserService(UserRepository(session), UserTableToJormMapper())
        token_service = TokenService(TokenRepository(session), TokenTableMapper())
        return UserInfoCollectorImpl(account_service, user_service, token_service)

    @staticmethod
    def create_jorm_collector(session) -> JORMCollector:
        niche_service = NicheService(NicheRepository(session), NicheTableToJormMapper())
        category_service = CategoryService(CategoryRepository(session),
                                           CategoryTableToJormMapper(NicheTableToJormMapper()))
        warehouse_service = WarehouseService(WarehouseRepository(session), WarehouseTableToJormMapper())
        unit_economy_service = EconomyService(EconomyRequestRepository(session),
                                              EconomyResultRepository(session),
                                              EconomyResultTableToJormMapper(EconomyRequestTableToJormMapper()),
                                              category_service, niche_service, warehouse_service)
        frequency_service = FrequencyService(FrequencyRequestRepository(session),
                                             FrequencyResultRepository(session),
                                             FrequencyResultTableToJormMapper())
        return JormCollectorImpl(niche_service, category_service,
                                 warehouse_service, unit_economy_service, frequency_service)
