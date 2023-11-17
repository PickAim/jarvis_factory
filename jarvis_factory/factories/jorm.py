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
        products = []
        niche_name = DEFAULT_NICHE_NAME
        for i, cost in enumerate(cost_data):
            spec_leftovers: list[SpecifiedLeftover] = [SpecifiedLeftover("second", leftover_func(cost))]
            before_trade_storage_dict = StorageDict()
            before_trade_storage_dict[1] = spec_leftovers

            spec_leftovers: list[SpecifiedLeftover] = [SpecifiedLeftover("second", max(0, leftover_func(cost) - 5))]
            after_trade_storage_dict = StorageDict()
            after_trade_storage_dict[1] = spec_leftovers
            products.append(Product(f'prod{i}', cost, i, 4.0, "brand", "seller", niche_name, DEFAULT_CATEGORY_NAME,
                                    history=ProductHistory([
                                        ProductHistoryUnit(1, datetime.utcnow(), before_trade_storage_dict),
                                        ProductHistoryUnit(3, datetime.utcnow(), after_trade_storage_dict)]),
                                    width=0.15, height=0.3, depth=0.1,
                                    top_places=SpecifiedTopPlaceDict({'Test niche': i})))
        return Niche(niche_name, niche_commissions_dict, 0.1, products)

    @staticmethod
    def create_default_warehouse() -> Warehouse:
        return Warehouse(DEFAULT_WAREHOUSE_NAME, 1, HandlerType.MARKETPLACE, Address("", ""))
