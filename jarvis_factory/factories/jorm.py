from enum import Enum
from functools import lru_cache

from jarvis_calc.database_interactors.db_controller import DBController
from jorm.market.infrastructure import Warehouse, HandlerType, Address
from jorm.market.person import Client, Account, User
from jorm.market.service import Request

from jarvis_factory.factories.jcalc import JCalcClassesFactory


class FactoryKeywords(Enum):
    DEFAULT_WAREHOUSE = "DEFAULT_WAREHOUSE"


class JORMClassesFactory:
    def __init__(self):
        self.__db_controller: DBController = JCalcClassesFactory.create_db_controller()

    @staticmethod
    def create_new_client() -> Client:
        return Client()

    @staticmethod
    def create_account(email: str, hashed_password: str, phone_number: str = "") -> Account:
        return Account(email, hashed_password, phone_number)

    @staticmethod
    def create_user(user_id=-1, name="UNNAMED") -> User:
        return User(user_id, name)

    @lru_cache(maxsize=5)
    def warehouse(self, warehouse_name: str) -> Warehouse:
        if warehouse_name == FactoryKeywords.DEFAULT_WAREHOUSE.value:
            return self.create_default_warehouse()
        return self.__db_controller.get_warehouse(warehouse_name)

    def create_default_warehouse(self) -> Warehouse:
        warehouses: list[Warehouse] = self.__db_controller.get_all_warehouses()
        if warehouses is None or len(warehouses) == 0:
            return self.__create_default_warehouse()
        mean_basic_logistic_to_customer_commission: int = 0
        mean_additional_logistic_to_customer_commission: float = 0
        mean_logistic_from_customer_commission: int = 0
        mean_basic_storage_commission: int = 0
        mean_additional_storage_commission: float = 0
        mean_mono_palette_storage_commission: int = 0
        for warehouse in warehouses:
            mean_basic_logistic_to_customer_commission += warehouse.basic_logistic_to_customer_commission
            mean_additional_logistic_to_customer_commission += warehouse.additional_logistic_to_customer_commission
            mean_logistic_from_customer_commission += warehouse.logistic_from_customer_commission
            mean_basic_storage_commission += warehouse.basic_storage_commission
            mean_additional_storage_commission += warehouse.additional_storage_commission
            mean_mono_palette_storage_commission += warehouse.mono_palette_storage_commission
        mean_basic_logistic_to_customer_commission //= len(warehouses)
        mean_additional_logistic_to_customer_commission /= len(warehouses)
        mean_logistic_from_customer_commission //= len(warehouses)
        mean_basic_storage_commission //= len(warehouses)
        mean_additional_storage_commission /= len(warehouses)
        mean_mono_palette_storage_commission //= len(warehouses)
        result_warehouse: Warehouse = \
            Warehouse(str(FactoryKeywords.DEFAULT_WAREHOUSE), 0, HandlerType.MARKETPLACE, Address(), products=[],
                      basic_logistic_to_customer_commission=mean_basic_logistic_to_customer_commission,
                      additional_logistic_to_customer_commission=mean_additional_logistic_to_customer_commission,
                      logistic_from_customer_commission=mean_logistic_from_customer_commission,
                      basic_storage_commission=mean_basic_storage_commission,
                      additional_storage_commission=mean_additional_storage_commission,
                      mono_palette_storage_commission=mean_mono_palette_storage_commission)
        return result_warehouse

    @staticmethod
    def __create_default_warehouse() -> Warehouse:
        return Warehouse(str(FactoryKeywords.DEFAULT_WAREHOUSE), 0, HandlerType.MARKETPLACE, Address(), products=[],
                         basic_logistic_to_customer_commission=0,
                         additional_logistic_to_customer_commission=0,
                         logistic_from_customer_commission=0,
                         basic_storage_commission=0,
                         additional_storage_commission=0,
                         mono_palette_storage_commission=0)

    def request(self, json_request) -> Request:
        pass
