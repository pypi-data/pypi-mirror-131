from typing import List, TypedDict

# class TxType(Enum):
#     BUY = "buy"
#     SELL = "sell"
#     SEND = "send"
#     RECEIVE = "receive"
#     OPEN_POSITION = "open_position"
#     DEPOSIT_COLLATERAL = "deposit_collateral"
#     WITHDRAW_COLLATERAL = "withdraw_collateral"
#     MINT = "mint"
#     BURN = "burn"
#     AUCTION = "auction"
#     PROVIDE_LIQUIDITY = "provide_liquidity"
#     WITHDRAW_LIQUIDITY = "withdraw_liquidity"
#     STAKE = "stake"
#     UNSTAKE = "unstake"
#     GOV_STAKE = "gov_stake"
#     GOV_UNSTAKE = "gov_unstake"
#     GOV_CREATE_POLL = "gov_create_poll"
#     GOV_END_POLL = "gov_end_poll"
#     GOV_CAST_POLL = "gov_cast_poll"
#     GOV_WITHDRAW_VOTING_REWARDS = "gov_withdraw_voting_rewards"
#     WITHDRAW_REWARDS = "withdraw_rewards"
#     CLAIM_AIRDROP = "claim_airdrops"
#     TERRA_SWAP = "terra_swap"
#     TERRA_SEND = "terra_send"
#     TERRA_SWAP_SEND = "terra_swap_send"
#     TERRA_RECEIVE = "terra_receive"
#     REGISTRATION = "registration"
#     BID_LIMIT_ORDER = "bid_limit_order"
#     ASK_LIMIT_ORDER = "ask_limit_order"
#     CANCEL_LIMIT_ORDER = "cancel_limit_order"
#     EXECUTE_LIMIT_ORDER = "execute_limit_order"
#     WITHDRAW_UNLOCKED_UST = "withdraw_unlocked_ust"
#     WITHDRAW_UNLOCKED_UST_ALL = "withdraw_unlocked_ust_all"


class TxRaw(TypedDict):
    id: str
    height: str
    txHash: str
    type: str
    data: str
    token: str
    datetime: str
    fee: str
    memo: str


class LpInfoRaw(TypedDict):
    stablecoin_symbol: str
    stablecoin_amount: str
    token_symbol: str
    token_amount: str
    total_share: str


class MirrorAssetRaw(TypedDict):
    symbol: str
    name: str
    token: str
    pair: str
    lpToken: str
    status: str


class RewardInfoRaw(TypedDict):
    asset_token: str
    bond_amount: str


class RewardInfosRaw(TypedDict):
    reward_infos: List[RewardInfoRaw]
