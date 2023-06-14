from jarvis_db.repositores.mappers.market.infrastructure import NicheTableToJormMapper, CategoryTableToJormMapper, \
    WarehouseTableToJormMapper
from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.mappers.market.person.token_mappers import TokenTableMapper
from jarvis_db.repositores.mappers.market.service import FrequencyResultTableToJormMapper, \
    EconomyResultTableToJormMapper, EconomyRequestTableToJormMapper
from jarvis_db.repositores.market.infrastructure import NicheRepository, CategoryRepository, WarehouseRepository
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.repositores.market.person.token_repository import TokenRepository
from jarvis_db.repositores.market.service import FrequencyRequestRepository, FrequencyResultRepository, \
    EconomyResultRepository, EconomyRequestRepository
from jarvis_db.services.market.infrastructure.category_service import CategoryService
from jarvis_db.services.market.infrastructure.niche_service import NicheService
from jarvis_db.services.market.infrastructure.warehouse_service import WarehouseService
from jarvis_db.services.market.person import TokenService
from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService
from jarvis_db.services.market.service.economy_service import EconomyService
from jarvis_db.services.market.service.frequency_service import FrequencyService
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger

from jdu.db_tools.update.user_info_changer import UserInfoChangerImpl
from jdu.db_tools.update.jorm_changer_impl import JormChangerImpl


class JDUClassesFactory:
    @staticmethod
    def create_user_info_changer(session) -> UserInfoChanger:
        account_service = AccountService(AccountRepository(session), AccountTableToJormMapper())
        user_service = UserService(UserRepository(session), UserTableToJormMapper())
        token_service = TokenService(TokenRepository(session), TokenTableMapper())
        return UserInfoChangerImpl(user_service, account_service, token_service)

    @staticmethod
    def create_jorm_changer(session) -> JORMChanger:
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
        return JormChangerImpl(unit_economy_service, frequency_service)
