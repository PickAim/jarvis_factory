from jdu.support.constant import WILDBERRIES_NAME
from jorm.support.types import EconomyConstants

SUPPORTED_MARKETPLACES: list[str] = [
    WILDBERRIES_NAME
]

ECONOMY_CONSTANTS = {
    WILDBERRIES_NAME: EconomyConstants(
        max_mass=25,
        max_side_sum=200,
        max_side_length=120,
        max_standard_volume_in_liters=5,
        return_price=50_00,
        oversize_logistic_price=1000_00,
        oversize_storage_price=2_157,
        standard_warehouse_logistic_price=45_00,
        standard_warehouse_storage_price=30,
        nds_tax=0.20,
        commercial_tax=0.15,
        self_employed_tax=0.06,
    )
}
