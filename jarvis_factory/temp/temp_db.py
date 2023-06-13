from jarvis_db.services.market.person.account_service import AccountService
import datetime

from jorm.jarvis.db_access import JORMCollector
from jorm.jarvis.db_update import JORMChanger
from jorm.market.infrastructure import Warehouse, Niche, HandlerType
from jorm.market.items import Product
from jorm.market.person import Account
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


class TempJORMCollector(JORMCollector):
    def get_products_by_user(self, user_id: int) -> list[Product]:
        return []

    def get_niche(self, niche_name: str, marketplace_id: int) -> Niche:
        return Niche("empty niche", {HandlerType.MARKETPLACE: 0.17}, 0)

    def get_warehouse(self, warehouse_name: str) -> Warehouse:
        pass

    def get_all_warehouses(self) -> list[Warehouse]:
        pass

    def get_all_unit_economy_results(self, user_id: int) \
            -> list[tuple[UnitEconomyRequest, UnitEconomyResult, RequestInfo]]:
        if user_id not in unit_economy_requests:
            return []
        return [
            unit_economy_requests[user_id][request_id]
            for request_id in unit_economy_requests[user_id]
        ]

    def get_all_frequency_results(self, user_id: int) -> list[tuple[FrequencyRequest, FrequencyResult, RequestInfo]]:
        return [
            (FrequencyRequest("nicheA"),
             FrequencyResult({123: 123}),
             RequestInfo(1, datetime.datetime.utcnow(), "first")),

            (FrequencyRequest("nicheB"),
             FrequencyResult({321: 321}),
             RequestInfo(2, datetime.datetime.utcnow(), "second"))
        ]


class TempJORMChanger(JORMChanger):
    last_request_id = 0

    def save_unit_economy_request(self, request: UnitEconomyRequest, result: UnitEconomyResult,
                                  request_info: RequestInfo, user_id: int) -> int:
        if user_id not in unit_economy_requests:
            unit_economy_requests[user_id] = {}
        if request_info.id is None:
            request_info.id = self.last_request_id
            self.last_request_id += 1
        unit_economy_requests[user_id][request_info.id] = (request, result, request_info)
        return request_info.id

    def save_frequency_request(self, request: FrequencyRequest, result: FrequencyResult,
                               request_info: RequestInfo, user_id: int) -> int:
        return 0

    def load_new_niche(self, niche_name: str) -> Niche:
        pass

    def delete_unit_economy_request(self, request_id: int, user_id: int) -> None:
        if user_id in unit_economy_requests:
            if request_id in unit_economy_requests[user_id]:
                unit_economy_requests[user_id].pop(request_id)

    def delete_frequency_request(self, request_id: int, user_id: int) -> None:
        pass
