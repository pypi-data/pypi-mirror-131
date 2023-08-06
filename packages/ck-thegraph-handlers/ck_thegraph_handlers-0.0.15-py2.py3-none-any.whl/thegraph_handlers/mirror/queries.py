txs_query = """
{
    txs(account: $address) {
        id
        height
        txHash
        type
        data
        token
        datetime
        fee
        memo
    }
}
"""

pool_balance_query = """
    {masset_contract}: WasmContractsContractAddressStore( 
        ContractAddress: "{lp_token_contract}", 
        QueryMsg: "{{ \\"balance\\" : {{  \\"address\\" : \\"{address}\\" }} }}"
    ){{
        Result
    }}"""

pool_query = """
    {masset_contract}: WasmContractsContractAddressStore( 
        ContractAddress: "{pair_contract}", 
        QueryMsg: "{{ \\"pool\\" : {{}} }}"
    ){{
        Result
    }}"""

pool_info_query = """
    {masset_contract}: WasmContractsContractAddressStore( 
        ContractAddress: "{staking_contract}", 
        QueryMsg: "{{ \\"pool_info\\": {{ \\"asset_token\\" : \\"{masset_contract}\\" }} }}"
    ){{
        Result
    }}"""

locked_balance_query = """
    {masset_contract}: WasmContractsContractAddressStore( 
        ContractAddress: "{masset_contract}", 
        QueryMsg: "{{ \\"balance\\" : {{  \\"address\\" : \\"{address}\\" }} }}"
    ){{
        Result
    }}"""

reward_infos_query = """
    {masset_contract}: WasmContractsContractAddressStore( 
        ContractAddress: "{masset_contract}", 
        QueryMsg: "{{ \\"reward_info\\" : {{ \\"staker_addr\\" : \\"{address}\\" }} }}"
    ){{
        Result
    }}"""
