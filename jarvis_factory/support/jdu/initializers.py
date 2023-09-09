import requests
from jdu.support.commission.wildberries_commission_resolver import WildberriesCommissionResolver
from jdu.support.constant import WILDBERRIES_NAME
from jorm.server.providers.initializers import DataProviderInitializer
from requests.adapters import HTTPAdapter


class WildberriesDataProviderInitializer(DataProviderInitializer):
    def additional_init_data_provider(self, data_provider):
        data_provider.commission_resolver = WildberriesCommissionResolver()
        data_provider.session = requests.Session()
        __adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
        data_provider.session.mount('https://', __adapter)

    def get_marketplace_name(self) -> str:
        return WILDBERRIES_NAME

