import json

from thegraph_handlers._exceptions import InvalidMethod
from thegraph_handlers.mirror.queries import (
    locked_balance_query,
    pool_balance_query,
    pool_info_query,
    pool_query,
    reward_infos_query,
)

SUPPORTED_QUERIES = {
    "get_pool_balance": pool_balance_query,
    "get_pool": pool_query,
    "get_pool_info": pool_info_query,
    "get_locked_balance": locked_balance_query,
    "get_reward_infos": reward_infos_query,
}


def build_query(query: str, **params) -> str:
    """Builds query from supplied params values"""
    if query not in SUPPORTED_QUERIES:
        raise InvalidMethod("Query not in supported requests.")
    return SUPPORTED_QUERIES[query].format(**params)


def format_multi(response: dict) -> dict:
    """
    Takes the 'Response' string: {Response: <json_string> } converts to json and returns
    """
    formatted = {}
    for query_name, result in response.items():
        if not result:
            raise Exception("No result in response")
        formatted[query_name] = json.loads(result["Result"])

    return formatted


def format_single(response: dict) -> dict:
    res = json.loads(list(response.values())[0]["Result"])
    return res


def wrap_query(query: str) -> str:
    return f"{{ {query} }}"
