from jarvis_db.repositores.mappers.market.person import AccountTableToJormMapper, UserTableToJormMapper
from jarvis_db.repositores.mappers.market.person.token_mappers import TokenTableMapper
from jarvis_db.repositores.mappers.market.service import FrequencyRequestTableToJormMapper
from jarvis_db.repositores.market.infrastructure import NicheRepository
from jarvis_db.repositores.market.person import AccountRepository, UserRepository
from jarvis_db.repositores.market.person.token_repository import TokenRepository
from jarvis_db.repositores.market.service import FrequencyRequestRepository, FrequencyResultRepository
from jarvis_db.services.market.person import UserService, AccountService, TokenService
from jarvis_db.services.market.service.frequency_service import FrequencyService
from sqlalchemy.orm import Session


class JDBServiceFactory:
    @staticmethod
    def create_frequency_service(session: Session) -> FrequencyService:
        return FrequencyService(
            FrequencyRequestRepository(session),
            NicheRepository(session),
            FrequencyResultRepository(session),
            FrequencyRequestTableToJormMapper(),
        )

    @staticmethod
    def create_token_service(session: Session) -> TokenService:
        return TokenService(TokenRepository(session), TokenTableMapper())

    @staticmethod
    def create_user_service(session: Session) -> UserService:
        return UserService(UserRepository(session), UserTableToJormMapper())

    @staticmethod
    def create_account_service(session: Session) -> AccountService:
        return AccountService(AccountRepository(session), AccountTableToJormMapper())
