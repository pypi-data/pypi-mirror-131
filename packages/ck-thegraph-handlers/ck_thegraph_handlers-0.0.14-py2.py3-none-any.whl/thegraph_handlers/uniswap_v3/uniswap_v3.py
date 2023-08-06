import logging
from types import TracebackType
from typing import Type, Any, TypeVar, AsyncGenerator, Tuple, Optional

from thegraph_handlers import SubgraphError
from thegraph_handlers._protocols import AClosableHTTPClient
from thegraph_handlers._subgraph_client import SubgraphClient
from thegraph_handlers.abstract_handler import AbstractHandler
from thegraph_handlers.models import LiquidityPoolShare
from thegraph_handlers.shared.dispatch import ParserDispatch
from thegraph_handlers.uniswap_v3.parsers import parse_liquidity_position
from thegraph_handlers.uniswap_v3.queries import position_and_snaps, positions

A = TypeVar("A")

logger = logging.getLogger(__name__)


class UniswapV3(AbstractHandler):
    def __init__(
        self,
        client: AClosableHTTPClient,
    ) -> None:
        self.parser_dispatch = ParserDispatch(
            liquidity_position=parse_liquidity_position,
        )
        url: str = "http://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        self.subgraph_client = SubgraphClient(url, client=client)

    async def __aenter__(self) -> "UniswapV3":
        return self

    @property
    def name(self) -> str:
        return self.__class__.__name__

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.subgraph_client.aclose()

    async def yield_liquidity_pool_shares(
        self, address: str, include_withdrawn: bool = False
    ) -> AsyncGenerator[LiquidityPoolShare, None]:
        """
        If `include_withdrawn=True`, list shares of liquidity pools the `address`
        somewhen in the past provided liquidity to.
        """
        variables = {
            "address": address.lower(),
            "min": "-1" if include_withdrawn else "0",
        }
        try:
            response = await self.subgraph_client.execute(
                positions, variables
            )
        except SubgraphError as exc:
            logger.error("Internal exception for %s fetching - %s", self.name, exc)
            raise exc from None
        except Exception as exc:
            logger.error("HTTP exception for %s fetching - %s", self.name, exc)
            raise exc from None

        for position in response["positions"]:
            yield self.parser_dispatch["liquidity_position"](position)

    async def yield_positions_and_snaps(
        self,
        address: str,
        skip: int = 0,
        from_start: bool = True,
    ) -> Optional[Tuple[Any, Any]]:
        variables = {
            "address": address.lower(),
            "skip": skip,
            "orderDirection": 'desc' if from_start else 'asc',
        }

        try:
            response = await self.subgraph_client.execute(
                position_and_snaps, variables
            )

            # todo add parser
            yield response['positions'], response['positionSnapshots']

        except SubgraphError as exc:
            logger.error("Internal exception for %s fetching - %s", self.name, exc)
            raise exc from None
        except Exception as exc:
            logger.error("HTTP exception for %s fetching - %s", self.name, exc)
            raise exc from None
