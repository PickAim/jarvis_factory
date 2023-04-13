import datetime

from jorm.jarvis.db_access import JORMCollector, UserInfoCollector
from jorm.jarvis.db_update import UserInfoChanger, JORMChanger
from jorm.market.infrastructure import Warehouse, Niche, HandlerType
from jorm.market.person import Account, User
from jorm.market.service import FrequencyRequest, FrequencyResult, UnitEconomyRequest, UnitEconomyResult, RequestInfo
from jorm.server.token.types import TokenType

users: dict[int, User] = {}
users_by_email: dict[str, User] = {}
users_by_phone: dict[str, User] = {}
accounts_by_email: dict[str, Account] = {}
accounts_by_phone: dict[str, Account] = {}
user_tokens: dict[int, dict[str, dict[TokenType, str]]] = {}


class TempUserInfoCollector(UserInfoCollector):
    def get_user_by_account(self, account: Account) -> User | None:
        if account.email in users_by_email:
            return users_by_email[account.email]
        if account.phone_number in users_by_phone:
            return users_by_phone[account.phone_number]
        return None

    def get_user_by_id(self, user_id: int) -> User | None:
        if user_id in users:
            return users[user_id]
        return None

    def get_account_by_email(self, email: str) -> Account | None:
        if email in accounts_by_email:
            return accounts_by_email[email]
        return None

    def get_account_by_phone(self, phone: str) -> Account | None:
        if phone in accounts_by_phone:
            return accounts_by_phone[phone]
        return None

    def get_token_rnd_part(self, user_id: int, imprint: str, token_type: TokenType) -> str:
        return user_tokens[user_id][imprint][token_type]


class TempJORMCollector(JORMCollector):
    def get_niche(self, niche_name: str) -> Niche:
        return Niche("empty niche", {HandlerType.MARKETPLACE: 0.17}, 0)

    def get_warehouse(self, warehouse_name: str) -> Warehouse:
        pass

    def get_all_warehouses(self) -> list[Warehouse]:
        pass

    def get_all_unit_economy_results(self, user: User) \
            -> list[tuple[UnitEconomyRequest, UnitEconomyResult, RequestInfo]]:
        return [
            (UnitEconomyRequest(50, 10, "nicheA"),
             UnitEconomyResult(50, 10, 2, 12, 1, 5, 100, 0, 0, 0),
             RequestInfo(1, datetime.datetime.utcnow(), "first")),

            (UnitEconomyRequest(500, 100, "nicheB"),
             UnitEconomyResult(500, 100, 20, 120, 10, 50, 1000, 0, 0, 0),
             RequestInfo(2, datetime.datetime.utcnow(), "second"))
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
    def update_session_tokens(self, old_update_token: str, new_access_token: str, new_update_token: str) -> None:
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
        users[user.user_id] = user
        if account.email is not None and account.email != "":
            users_by_email[account.email] = user
            accounts_by_email[account.email] = account
        if account.phone_number is not None and account.phone_number != "":
            users_by_phone[account.phone_number] = user
            accounts_by_phone[account.phone_number] = account

    def delete_tokens_for_user(self, user: User, imprint_token: str):
        user_tokens[user.user_id].pop(imprint_token, None)


class TempJORMChanger(JORMChanger):

    def save_unit_economy_request(self, request: UnitEconomyRequest, result: UnitEconomyResult,
                                  request_info: RequestInfo, user: User) -> int:
        return 0

    def save_frequency_request(self, request: FrequencyRequest, result: FrequencyResult,
                               request_info: RequestInfo, user: User) -> int:
        return 0

    def load_new_niche(self, niche_name: str) -> Niche:
        pass

    def delete_frequency_request(self, request_id: int, user: User) -> None:
        pass

    def delete_unit_economy_request(self, request_id: int, user: User) -> None:
        pass
