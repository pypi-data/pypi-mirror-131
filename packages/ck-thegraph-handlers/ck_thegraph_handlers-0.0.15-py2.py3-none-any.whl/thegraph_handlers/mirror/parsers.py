from decimal import Decimal

from thegraph_handlers._exceptions import ContractMissing, NotExpected
from thegraph_handlers._utils import div_safe, safe_decimal
from thegraph_handlers.mirror._types import LpInfoRaw, MirrorAssetRaw, TxRaw
from thegraph_handlers.mirror.data import MAIN_CONTRACTS
from thegraph_handlers.mirror.model import Reward
from thegraph_handlers.models import (
    LiquidityPoolShare,
    LiquidityPoolToken,
    LiquidityPoolUnderlyingToken,
    TerraLiquidityPoolShare,
    TerraToken,
)

TERRA_DECIMALS = "6"
TERRA_COEF = Decimal("1e-6")

STABLECOIN_SYMBOL = "UST"
STABLECOIN_NAME = "TerraUSD"
STABLECOIN_ADDRESS = "uusd"


def create_lp_token_name(masset: MirrorAssetRaw, lp_info: LpInfoRaw) -> str:
    return f"Mirror {masset['symbol']}/{lp_info['stablecoin_symbol']}"


def _get_token_symbol(contract_addr: str) -> str:
    """Gets and returns a token symbol form the specified token contract address

    :param contract_addr: Contract of the token from whitelist on the running network
    (ex. terra10llyp6v3j3her8u3ce66ragytu45kcmd9asj3u)
    :type contract_addr: str
    :returns: A string with the symbol (ex. UUSD)
    :rtype: str
    """
    if contract_addr in MAIN_CONTRACTS["whitelist"]:
        return MAIN_CONTRACTS["whitelist"][contract_addr]["symbol"]
    else:
        raise ContractMissing("Contact address missing. Update list")


def parse_pool(pool: dict) -> LpInfoRaw:
    """Takes pool api response finds stablecoin and mirror asset balance and returns in better format"""

    if "assets" not in pool:
        raise NotExpected("Asset list not found in API response")

    assets = pool["assets"]

    if "native_token" in assets[0]["info"] and "token" in assets[1]["info"]:
        stablecoin = 0
        token = 1
    elif "native_token" in assets[1]["info"] and "token" in assets[0]["info"]:
        stablecoin = 1
        token = 0
    else:
        raise NotExpected("Pool asset list unexpected format.")

    stablecoin_amount = assets[stablecoin]["amount"]

    token_amount = assets[token]["amount"]
    token_contract = assets[token]["info"]["token"]["contract_addr"]
    token_symbol = _get_token_symbol(token_contract)
    total_share = pool["total_share"]

    return {
        "stablecoin_amount": stablecoin_amount,
        "stablecoin_symbol": STABLECOIN_SYMBOL,
        "token_amount": token_amount,
        "token_symbol": token_symbol,
        "total_share": total_share,
    }


def parse_liquidity_position(
    masset: MirrorAssetRaw,
    lp_info: LpInfoRaw,
    user_lp_balance: str,
    user_address: str,
) -> LiquidityPoolShare:

    lp_symbol = create_lp_token_name(masset, lp_info)
    lp_name = f"{lp_symbol} token"

    token_amount = (
        div_safe(lp_info["token_amount"], lp_info["total_share"]) * user_lp_balance
    ) * Decimal(f"1e-{TERRA_DECIMALS}")

    stablecoin_amount = (
        div_safe(lp_info["stablecoin_amount"], lp_info["total_share"]) * user_lp_balance
    ) * Decimal(f"1e-{TERRA_DECIMALS}")

    return TerraLiquidityPoolShare(
        user_address=user_address,
        share=safe_decimal(lp_info["total_share"]),  # verify if this is correct
        lp_token=LiquidityPoolToken(
            token=TerraToken(
                symbol=lp_symbol,
                name=lp_name,
                contract_address=masset["pair"],
                decimals=TERRA_DECIMALS,
            ),
            amount=safe_decimal(user_lp_balance),
            underlying_tokens=(
                LiquidityPoolUnderlyingToken(
                    token=TerraToken(
                        symbol=lp_info["token_symbol"],
                        name=masset["name"],
                        contract_address=masset["token"],
                        decimals=TERRA_DECIMALS,
                    ),
                    weight=Decimal("0.5"),
                    amount=safe_decimal(token_amount),
                ),
                LiquidityPoolUnderlyingToken(
                    token=TerraToken(
                        symbol=lp_info["stablecoin_symbol"],
                        name=STABLECOIN_NAME,
                        contract_address=STABLECOIN_ADDRESS,
                        decimals=TERRA_DECIMALS,
                    ),
                    weight=Decimal("0.5"),
                    amount=safe_decimal(stablecoin_amount),
                ),
            ),
        ),
    )


def parse_reward(token: dict) -> Reward:
    symbol = _get_token_symbol(contract_addr=token["asset_token"])
    reward_amount = Decimal(token["pending_reward"]) * TERRA_COEF
    return Reward(
        reward_amount=reward_amount,
        asset_symbol=symbol,
        asset_address=token["asset_token"],
        decimals=TERRA_DECIMALS,
    )


def parse_tx(tx: TxRaw) -> dict:
    # todo redesign data model
    return tx


def parse_lp_token(
    masset: MirrorAssetRaw,
    lp_info: LpInfoRaw,
) -> LiquidityPoolToken:

    lp_symbol = create_lp_token_name(masset, lp_info)
    lp_name = f"{lp_symbol} token"

    return LiquidityPoolToken(
        token=TerraToken(
            symbol=lp_symbol,
            name=lp_name,
            contract_address=masset["pair"],
            decimals=TERRA_DECIMALS,
        ),
        amount=safe_decimal(lp_info["total_share"]) * Decimal(f"1e-{TERRA_DECIMALS}"),
        underlying_tokens=(
            LiquidityPoolUnderlyingToken(
                token=TerraToken(
                    symbol=lp_info["token_symbol"],
                    name=masset["name"],
                    contract_address=masset["token"],
                    decimals=TERRA_DECIMALS,
                ),
                weight=Decimal("0.5"),
                amount=safe_decimal(lp_info["token_amount"])
                * Decimal(f"1e-{TERRA_DECIMALS}"),
            ),
            LiquidityPoolUnderlyingToken(
                token=TerraToken(
                    symbol=lp_info["stablecoin_symbol"],
                    name=STABLECOIN_NAME,
                    contract_address=STABLECOIN_ADDRESS,
                    decimals=TERRA_DECIMALS,
                ),
                weight=Decimal("0.5"),
                amount=safe_decimal(lp_info["stablecoin_amount"])
                * Decimal(f"1e-{TERRA_DECIMALS}"),
            ),
        ),
    )
