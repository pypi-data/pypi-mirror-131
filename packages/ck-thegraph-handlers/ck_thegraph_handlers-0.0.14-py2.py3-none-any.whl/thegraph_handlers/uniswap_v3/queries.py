
positions = """
    query ($address: String) {
        positions(where: { owner: $address}) {
            id
            owner
            liquidity
            pool {
                id
                tick
                token0Price
                token1Price
                totalValueLockedETH
            }
            tickLower {
              tickIdx
            }
            tickUpper {
              tickIdx
            }
            depositedToken0
            depositedToken1
            withdrawnToken0
            withdrawnToken1
            collectedFeesToken0
            collectedFeesToken1
            token0 {
                id
                symbol
                name
                feesUSD
                decimals
                derivedETH
            }
            token1 {
                id
                symbol
                name
                feesUSD
                decimals
                derivedETH
            }
        }
    }
    """


position_and_snaps = """
    query ($address: String, $orderDirection: String) {
        positions(where: {owner: $address}) {
            liquidity
            pool {
                id
                tick
            }
            tickLower {
                tickIdx
            }
            tickUpper {
                tickIdx
            }
            transaction {
                timestamp
                mints {
                    amountUSD
                }
            }
            token0 {
                decimals
            }
            token1 {
                decimals
            }
        }
        positionSnapshots(where: {owner: $address}, orderBy: timestamp, orderDirection: $orderDirection) {
            blockNumber
            timestamp
            liquidity
            depositedToken0
            depositedToken1
            withdrawnToken0
            withdrawnToken1
            collectedFeesToken0
            collectedFeesToken1
            transaction {
                id
                gasUsed
                gasPrice
                mints {
                    amountUSD
                    amount0
                    amount1
                }
                burns {
                    amountUSD
                    amount0
                    amount1
                }
            }
            pool {
                token0 {
                    id
                }
                token1 {
                    id
                }
            }
        }
    }
    """
