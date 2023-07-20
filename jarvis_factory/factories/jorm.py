from datetime import datetime

from jarvis_calc.database_interactors.db_controller import DBController
from jorm.market.infrastructure import Warehouse, HandlerType, Address, Niche, Category, Marketplace
from jorm.market.items import ProductHistory, ProductHistoryUnit, Product
from jorm.market.person import Account, User
from jorm.support.constants import DEFAULT_CATEGORY_NAME, DEFAULT_MARKETPLACE_NAME, DEFAULT_NICHE_NAME, \
    DEFAULT_WAREHOUSE_NAME
from jorm.support.types import StorageDict, SpecifiedLeftover, SpecifiedTopPlaceDict

from jarvis_factory.support.const_data import cost_data
from jarvis_factory.support.functions import leftover_func


class JORMClassesFactory:
    def __init__(self, db_controller: DBController):
        self.__db_controller: DBController = db_controller

    @staticmethod
    def create_account(email: str, hashed_password: str, phone_number: str = "") -> Account:
        return Account(email, hashed_password, phone_number)

    @staticmethod
    def create_user(user_id=-1, name="UNNAMED") -> User:
        return User(user_id, name)

    @staticmethod
    def create_default_category() -> Category:
        return Category(DEFAULT_CATEGORY_NAME)

    @staticmethod
    def create_default_marketplace() -> Marketplace:
        return Marketplace(DEFAULT_MARKETPLACE_NAME)

    @staticmethod
    def create_default_niche() -> Niche:
        niche_commissions_dict: dict[HandlerType, float] = {
            HandlerType.MARKETPLACE: 0.17,
            HandlerType.PARTIAL_CLIENT: 0.15,
            HandlerType.CLIENT: 0.10
        }
        niche_cost_data = cost_data.copy()
        niche_cost_data.sort()
        products = []
        niche_name = DEFAULT_NICHE_NAME
        for i, cost in enumerate(cost_data):
            spec_leftovers: list[SpecifiedLeftover] = [SpecifiedLeftover("second", leftover_func(cost))]
            before_trade_storage_dict = StorageDict()
            before_trade_storage_dict[1] = spec_leftovers
            after_trade_storage_dict = StorageDict()
            after_trade_storage_dict[1] = [SpecifiedLeftover("second", max(leftover_func(cost) - 2, 0))]
            products.append(Product(f'prod{i}', cost, i, 4.0, "brand", "seller", niche_name, DEFAULT_CATEGORY_NAME,
                                    history=ProductHistory([
                                        ProductHistoryUnit(1, datetime.utcnow(), before_trade_storage_dict),
                                        ProductHistoryUnit(3, datetime.utcnow(), after_trade_storage_dict)]),
                                    width=0.15, height=0.3, depth=0.1,
                                    top_places=SpecifiedTopPlaceDict({'Test niche': i})))
        return Niche(niche_name, niche_commissions_dict, 0.1, products)

    def create_default_warehouse(self, reference_warehouses: list[Warehouse]) -> Warehouse:
        if reference_warehouses is None or len(reference_warehouses) == 0:
            return self.create_simple_default_warehouse()
        mean_basic_logistic_to_customer_commission: int = 0
        mean_additional_logistic_to_customer_commission: float = 0
        mean_logistic_from_customer_commission: int = 0
        mean_basic_storage_commission: int = 0
        mean_additional_storage_commission: float = 0
        mean_mono_palette_storage_commission: int = 0
        for warehouse in reference_warehouses:
            mean_basic_logistic_to_customer_commission += warehouse.basic_logistic_to_customer_commission
            mean_additional_logistic_to_customer_commission += warehouse.additional_logistic_to_customer_commission
            mean_logistic_from_customer_commission += warehouse.logistic_from_customer_commission
            mean_basic_storage_commission += warehouse.basic_storage_commission
            mean_additional_storage_commission += warehouse.additional_storage_commission
            mean_mono_palette_storage_commission += warehouse.mono_palette_storage_commission
        mean_basic_logistic_to_customer_commission //= len(reference_warehouses)
        mean_additional_logistic_to_customer_commission /= len(reference_warehouses)
        mean_logistic_from_customer_commission //= len(reference_warehouses)
        mean_basic_storage_commission //= len(reference_warehouses)
        mean_additional_storage_commission /= len(reference_warehouses)
        mean_mono_palette_storage_commission //= len(reference_warehouses)
        result_warehouse: Warehouse = \
            Warehouse(DEFAULT_WAREHOUSE_NAME, 0, HandlerType.MARKETPLACE, Address(), products=[],
                      basic_logistic_to_customer_commission=mean_basic_logistic_to_customer_commission,
                      additional_logistic_to_customer_commission=mean_additional_logistic_to_customer_commission,
                      logistic_from_customer_commission=mean_logistic_from_customer_commission,
                      basic_storage_commission=mean_basic_storage_commission,
                      additional_storage_commission=mean_additional_storage_commission,
                      mono_palette_storage_commission=mean_mono_palette_storage_commission)
        return result_warehouse

    @staticmethod
    def create_simple_default_warehouse() -> Warehouse:
        return Warehouse(DEFAULT_WAREHOUSE_NAME, 0, HandlerType.MARKETPLACE, Address(), products=[],
                         basic_logistic_to_customer_commission=0,
                         additional_logistic_to_customer_commission=0,
                         logistic_from_customer_commission=0,
                         basic_storage_commission=0,
                         additional_storage_commission=0,
                         mono_palette_storage_commission=0)
