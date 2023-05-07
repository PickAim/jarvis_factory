from jarvis_db.services.market.person.account_service import AccountService
from jarvis_db.services.market.person.user_service import UserService
import datetime

from jorm.jarvis.db_access import JORMCollector, UserInfoCollector
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger
from jorm.market.infrastructure import Warehouse, Niche, HandlerType
from jorm.market.items import Product
from jorm.market.person import Account, User
from jorm.market.service import FrequencyRequest, FrequencyResult, UnitEconomyRequest, UnitEconomyResult, RequestInfo
from jorm.server.token.types import TokenType

user_tokens: dict[int, dict[str, dict[TokenType, str]]] = {}
unit_economy_requests: dict[int, dict[int, tuple[UnitEconomyRequest, UnitEconomyResult, RequestInfo]]] = {}


def temp_get_account_and_id(email: str, phone: str, account_service: AccountService) -> tuple[Account, int] | None:
    try:
        return account_service.find_by_email(email)
    except (Exception, Exception):
        try:
            return account_service.find_by_phone(phone)
        except (Exception, Exception):
            return None


class TempUserInfoCollector(UserInfoCollector):
    def __init__(self, user_service: UserService, account_service: AccountService):
        self.__user_service = user_service
        self.__account_service = account_service

    def get_account_and_id(self, email: str, phone: str) -> tuple[Account, int] | None:
        return temp_get_account_and_id(email, phone, self.__account_service)

    def get_user_by_account(self, account: Account) -> User | None:
        found_account, account_id = self.get_account_and_id(account.email, account.phone_number)
        if found_account is None:
            return None
        return self.__user_service.find_by_account_id(account_id)[0]

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.__user_service.find_by_id(user_id)

    def get_token_rnd_part(self, user_id: int, imprint: str, token_type: TokenType) -> str:
        return user_tokens[user_id][imprint][token_type]


class TempJORMCollector(JORMCollector):
    def get_products_by_user(self, user: User) -> list[Product]:
        return []

    def get_niche(self, niche_name: str, marketplace_id: int) -> Niche:
        return Niche("empty niche", {HandlerType.MARKETPLACE: 0.17}, 0)

    def get_warehouse(self, warehouse_name: str) -> Warehouse:
        pass

    def get_all_warehouses(self) -> list[Warehouse]:
        pass

    def get_all_unit_economy_results(self, user: User) \
            -> list[tuple[UnitEconomyRequest, UnitEconomyResult, RequestInfo]]:
        if user.user_id not in unit_economy_requests:
            return []
        return [
            unit_economy_requests[user.user_id][request_id]
            for request_id in unit_economy_requests[user.user_id]
        ]

    def get_all_frequency_results(self, user: User) -> list[tuple[FrequencyRequest, FrequencyResult, RequestInfo]]:
        return [
            (FrequencyRequest("nicheA"),
             FrequencyResult({123: 123}),
             RequestInfo(1, datetime.datetime.utcnow(), "first")),

            (FrequencyRequest("nicheB"),
             FrequencyResult({321: 321}),
             RequestInfo(2, datetime.datetime.utcnow(), "second"))
        ]


class TempUserInfoChanger(UserInfoChanger):
    def __init__(self, user_service: UserService, account_service: AccountService):
        self.__user_service = user_service
        self.__account_service = account_service

    def update_session_tokens(self, user_id: int, old_update_token: str,
                              new_access_token: str, new_update_token: str) -> None:
        for user_id in user_tokens:
            for imprint in user_tokens[user_id]:
                if user_tokens[user_id][imprint][TokenType.UPDATE] == old_update_token:
                    user_tokens[user_id][imprint][TokenType.UPDATE] = new_update_token
                    user_tokens[user_id][imprint][TokenType.ACCESS] = new_access_token
                    return
        raise Exception

    def update_session_tokens_by_imprint(self, access_token: str, update_token: str, imprint_token: str,
                                         user: User) -> None:
        if user.user_id not in user_tokens:
            user_tokens[user.user_id] = {}
        if imprint_token in user_tokens[user.user_id]:
            user_tokens[user.user_id][imprint_token][TokenType.ACCESS] = access_token
            user_tokens[user.user_id][imprint_token][TokenType.UPDATE] = update_token
        else:
            self.save_all_tokens(access_token, update_token, imprint_token, user)

    def save_all_tokens(self, access_token: str, update_token: str, imprint_token: str, user: User) -> None:
        if user.user_id not in user_tokens:
            user_tokens[user.user_id] = {}
        if imprint_token not in user_tokens[user.user_id]:
            user_tokens[user.user_id][imprint_token] = {}
        user_tokens[user.user_id][imprint_token][TokenType.ACCESS] = access_token
        user_tokens[user.user_id][imprint_token][TokenType.UPDATE] = update_token

    def save_user_and_account(self, user: User, account: Account) -> None:
        self.__account_service.create(account)
        _, account_id = temp_get_account_and_id(account.email, account.phone_number, self.__account_service)
        self.__user_service.create(user, account_id)

    def delete_tokens_for_user(self, user: User, imprint_token: str):
        user_tokens[user.user_id].pop(imprint_token, None)


class TempJORMChanger(JORMChanger):
    last_request_id = 0

    def save_unit_economy_request(self, request: UnitEconomyRequest, result: UnitEconomyResult,
                                  request_info: RequestInfo, user: User) -> int:
        if user.user_id not in unit_economy_requests:
            unit_economy_requests[user.user_id] = {}
        if request_info.id is None:
            request_info.id = self.last_request_id
            self.last_request_id += 1
        unit_economy_requests[user.user_id][request_info.id] = (request, result, request_info)
        return request_info.id

    def save_frequency_request(self, request: FrequencyRequest, result: FrequencyResult,
                               request_info: RequestInfo, user: User) -> int:
        return 0

    def load_new_niche(self, niche_name: str) -> Niche:
        pass

    def delete_unit_economy_request(self, request_id: int, user: User) -> None:
        if user.user_id in unit_economy_requests:
            if request_id in unit_economy_requests[user.user_id]:
                unit_economy_requests[user.user_id].pop(request_id)

    def delete_frequency_request(self, request_id: int, user: User) -> None:
        pass
