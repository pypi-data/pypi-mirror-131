from collections import AsyncGenerator
from types import TracebackType
from typing import Any, Dict, Optional, Type

from thegraph_handlers import SubgraphError
from thegraph_handlers._protocols import AClosableHTTPClient
from thegraph_handlers._subgraph_client import SubgraphClient
from thegraph_handlers._utils import safe_decimal
from thegraph_handlers.mirror._types import RewardInfosRaw
from thegraph_handlers.mirror.data import MAIN_CONTRACTS
from thegraph_handlers.mirror.mirror_helper import (
    build_query,
    format_multi,
    format_single,
    wrap_query,
)
from thegraph_handlers.mirror.model import Reward
from thegraph_handlers.mirror.parsers import (
    parse_liquidity_position,
    parse_lp_token,
    parse_pool,
    parse_reward,
    parse_tx,
)
from thegraph_handlers.mirror.queries import txs_query
from thegraph_handlers.models import LiquidityPoolShare, LiquidityPoolToken
from thegraph_handlers.shared.base_swap import logger
from thegraph_handlers.shared.dispatch import ParserDispatch


class Mirror:
    def __init__(self, client: AClosableHTTPClient) -> None:
        self.parser_dispatch = ParserDispatch(
            liquidity_position=parse_liquidity_position,
            burn=None,
            mint=None,
            swap=None,
            lp_token=parse_lp_token,
        )

        mantle_url = "https://mantle.terra.dev/graphql"
        mirror_url = "https://graph.mirror.finance/graphql"

        self.mantle_subgraph_client = SubgraphClient(mantle_url, client=client)
        self.mirror_subgraph_client = SubgraphClient(mirror_url, client=client)

    async def __aenter__(self) -> "Mirror":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.mantle_subgraph_client.aclose()

    async def yield_rewards(
        self,
        address: str,
    ) -> AsyncGenerator[Reward, None]:
        """
        Fetch pool rewards for staked assets
        """
        reward_infos = await self._get_reward_infos(address)
        for token in reward_infos["reward_infos"]:
            yield parse_reward(token)

    async def yield_liquidity_pool_shares(
        self,
        address: str,
    ) -> AsyncGenerator[LiquidityPoolShare, None]:
        """Gets a all pools staked balances denominated in LPs and returns it in a list of
        LiquidityPoolShare and its underlying balances

        :returns: list of LP positions
        :rtype: AsyncGenerator[LiquidityPoolShare, None]
        """

        pools = await self._get_pools(address)
        reward_infos = await self._get_reward_infos(address)

        staked_amount_dict = {
            token["asset_token"]: safe_decimal(token["bond_amount"])
            for token in reward_infos["reward_infos"]
        }

        for token_address, masset in MAIN_CONTRACTS["whitelist"].items():
            if token_address not in staked_amount_dict:
                continue
            lp_balance = staked_amount_dict[token_address]
            lp_info = parse_pool(pools[token_address])

            yield self.parser_dispatch["liquidity_position"](
                masset,
                lp_info,
                lp_balance,
                address,
            )

    async def _get_pools(self, address: Optional[str]) -> Dict[str, Any]:
        query_parts = (
            build_query(
                query="get_pool",
                address=address,
                pair_contract=masset["pair"],
                masset_contract=masset["token"],
            )
            for masset in MAIN_CONTRACTS["whitelist"].values()
        )
        query = "".join(query_parts)
        return await self._query_multi(
            query,
        )

    async def _get_reward_infos(self, address: str) -> RewardInfosRaw:
        query = build_query(
            query="get_reward_infos",
            address=address,
            masset_contract=MAIN_CONTRACTS["contracts"]["staking"],
        )

        return await self._query_single(
            query,
        )

    async def _query_single(
        self,
        query: str,
    ) -> dict:
        wrapped_query = wrap_query(query)

        response = await self._execute(
            wrapped_query,
            self.mantle_subgraph_client,
        )

        return format_single(response)

    async def _query_multi(self, query: str) -> dict:
        wrapped_query = wrap_query(query)

        response = await self._execute(
            wrapped_query,
            self.mantle_subgraph_client,
        )

        return format_multi(response)

    async def yield_tokens(
        self,
    ) -> AsyncGenerator[LiquidityPoolToken, None]:

        pools = await self._get_pools(None)

        for token_address, masset in MAIN_CONTRACTS["whitelist"].items():
            lp_info = parse_pool(pools[token_address])
            yield self.parser_dispatch["lp_token"](
                masset,
                lp_info,
            )

    async def yield_txs(
        self,
        address: str,
    ) -> AsyncGenerator[dict, None]:

        variables = {
            "address": address.lower(),
            # "since": since,
            # "until": until,
        }

        response = await self._execute(
            txs_query,
            self.mirror_subgraph_client,
            variables,
        )

        for tx in response["txs"]:
            yield parse_tx(tx)

    async def _execute(
        self,
        query: str,
        client: SubgraphClient,
        variables: Dict[str, Any] = None,
    ) -> dict:
        try:
            return await client.execute(query, variables)
        except SubgraphError as exc:
            logger.error("Internal exception for %s fetching - %s", self.name, exc)
            raise exc from None
        except Exception as exc:
            logger.error("HTTP exception for %s fetching - %s", self.name, exc)
            raise exc from None

    @property
    def name(self) -> str:
        return self.__class__.__name__
