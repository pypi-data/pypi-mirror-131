from thegraph_handlers._protocols import AClosableHTTPClient
from thegraph_handlers.shared.base_swap import BaseSwap
from thegraph_handlers.shared.dispatch import ParserDispatch
from thegraph_handlers.sushiswap.parsers import (
    parse_burn,
    parse_liquidity_position,
    parse_mint,
    parse_swap,
)


class Sushiswap(BaseSwap):
    def __init__(
        self,
        client: AClosableHTTPClient,
        url: str = "http://api.thegraph.com/subgraphs/name/sushiswap/exchange",
    ) -> None:
        parser_dispatch = ParserDispatch(
            burn=parse_burn,
            liquidity_position=parse_liquidity_position,
            mint=parse_mint,
            swap=parse_swap,
        )
        BaseSwap.__init__(self, client, url, parser_dispatch)
