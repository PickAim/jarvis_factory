from typing import Type

from jdu.providers.wildberries_providers import WildberriesDataProviderWithoutKeyImpl, \
    WildberriesUserMarketDataProviderImpl
from jdu.support.constant import WILDBERRIES_NAME
from jorm.server.providers.initializers import DataProviderInitializer
from jorm.server.providers.providers import DataProviderWithoutKey, UserMarketDataProvider
from sqlalchemy.orm import Session

from jarvis_factory.support.jdb.services import JDBServiceFactory
from jarvis_factory.support.jdu.initializers import WildberriesDataProviderInitializer

_DATA_PROVIDERS_WITHOUT_KEY_INIT_INFO: dict[str, tuple[Type[DataProviderWithoutKey], Type[DataProviderInitializer]]] = {
    WILDBERRIES_NAME: (WildberriesDataProviderWithoutKeyImpl, WildberriesDataProviderInitializer)
}

_USER_DATA_PROVIDER_INIT_INFO: dict[str, tuple[Type[UserMarketDataProvider], Type[DataProviderInitializer]]] = {
    WILDBERRIES_NAME: (WildberriesUserMarketDataProviderImpl, WildberriesDataProviderInitializer)
}


class JDUClassesFactory:

    @staticmethod
    def create_data_provider_without_key(session: Session, marketplace_id: int) -> DataProviderWithoutKey | None:
        marketplace_service = JDBServiceFactory.create_marketplace_service(session)
        marketplace = marketplace_service.find_by_id(marketplace_id)
        if marketplace is None or marketplace.name not in _DATA_PROVIDERS_WITHOUT_KEY_INIT_INFO:
            return None
        data_provider_class, initializer_class = _DATA_PROVIDERS_WITHOUT_KEY_INIT_INFO[marketplace.name]
        return data_provider_class(initializer_class)

    @staticmethod
    def create_user_market_data_provider(session: Session,
                                         marketplace_id: int, user_id: int) -> UserMarketDataProvider | None:
        marketplace_service = JDBServiceFactory.create_marketplace_service(session)
        user_service = JDBServiceFactory.create_user_service(session)
        marketplace = marketplace_service.find_by_id(marketplace_id)
        user = user_service.find_by_id(user_id)
        if (user is None
                or marketplace is None
                or marketplace.name not in _DATA_PROVIDERS_WITHOUT_KEY_INIT_INFO
                or marketplace_id not in user.marketplace_keys):
            return None
        api_key = user.marketplace_keys[marketplace_id]
        user_data_provider_class, initializer_class = _USER_DATA_PROVIDER_INIT_INFO[marketplace.name]
        return user_data_provider_class(api_key=api_key, data_provider_initializer_class=initializer_class)
