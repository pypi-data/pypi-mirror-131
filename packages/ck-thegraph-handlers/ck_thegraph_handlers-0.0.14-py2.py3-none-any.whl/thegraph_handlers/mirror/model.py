from decimal import Decimal

import attr


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Reward:
    reward_amount: Decimal
    decimals: str
    asset_symbol: str
    asset_address: str
