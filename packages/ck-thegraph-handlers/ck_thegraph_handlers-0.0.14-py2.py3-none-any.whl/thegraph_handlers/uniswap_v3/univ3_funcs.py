# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 18:53:09 2021

https://github.com/Ranges-fi/Uni_v3_utils

@author: JNP
"""
from decimal import Decimal

'''liquitidymath'''
'''Python library to emulate the calculations done in liquiditymath.sol of UNI_V3 peryphery contract'''

'''get_amounts function'''


# Use 'get_amounts' function to calculate amounts as a function of liquidity and price range

def get_amount0(sqrt_a, sqrt_b, liquidity, decimals):
    if sqrt_a > sqrt_b:
        (sqrt_a, sqrt_b) = (sqrt_b, sqrt_a)

    amount0 = ((liquidity * 2 ** 96 * (sqrt_b - sqrt_a) / sqrt_b / sqrt_a) / 10 ** decimals)

    return amount0


def get_amount1(sqrt_a, sqrt_b, liquidity, decimals):
    if sqrt_a > sqrt_b:
        (sqrt_a, sqrt_b) = (sqrt_b, sqrt_a)

    amount1 = liquidity * (sqrt_b - sqrt_a) / 2 ** 96 / 10 ** decimals

    return amount1


def get_amounts(tick, tick_a, tick_b, liquidity, decimal0, decimal1):
    sqrt = (Decimal(1.0001) ** (tick / 2) * (2 ** 96))
    sqrt_a = (Decimal(1.0001) ** (tick_a / 2) * (2 ** 96))
    sqrt_b = (Decimal(1.0001) ** (tick_b / 2) * (2 ** 96))

    if sqrt_a > sqrt_b:
        (sqrt_a, sqrt_b) = (sqrt_b, sqrt_a)

    if sqrt <= sqrt_a:

        amount0 = get_amount0(sqrt_a, sqrt_b, liquidity, decimal0)
        return amount0, 0

    elif sqrt_b > sqrt > sqrt_a:
        amount0 = get_amount0(sqrt, sqrt_b, liquidity, decimal0)

        amount1 = get_amount1(sqrt_a, sqrt, liquidity, decimal1)

        return amount0, amount1

    else:
        amount1 = get_amount1(sqrt_a, sqrt_b, liquidity, decimal1)
        return 0, amount1


'''get token amounts relation'''


# Use this formula to calculate amount of t0 based on amount of t1 (required before calculate liquidity)
# relation = t1/t0
def amounts_relation(tick, tick_a, tick_b, decimals0, decimals1):
    sqrt = (1.0001 ** tick / 10 ** (decimals1 - decimals0)) ** (1 / 2)
    sqrt_a = (1.0001 ** tick_a / 10 ** (decimals1 - decimals0)) ** (1 / 2)
    sqrt_b = (1.0001 ** tick_b / 10 ** (decimals1 - decimals0)) ** (1 / 2)

    if sqrt == sqrt_a or sqrt == sqrt_b:
        relation = 0

    relation = (sqrt - sqrt_a) / ((1 / sqrt) - (1 / sqrt_b))
    return relation


'''get_liquidity function'''


# Use 'get_liquidity' function to calculate liquidity as a function of amounts and price range
def get_liquidity0(sqrt_a, sqrt_b, amount0, decimals):
    if sqrt_a > sqrt_b:
        (sqrt_a, sqrt_b) = (sqrt_b, sqrt_a)

    liquidity = amount0 / ((2 ** 96 * (sqrt_b - sqrt_a) / sqrt_b / sqrt_a) / 10 ** decimals)
    return liquidity


def get_liquidity1(sqrt_a, sqrt_b, amount1, decimals):
    if sqrt_a > sqrt_b:
        (sqrt_a, sqrt_b) = (sqrt_b, sqrt_a)

    liquidity = amount1 / ((sqrt_b - sqrt_a) / 2 ** 96 / 10 ** decimals)
    return liquidity


def get_liquidity(tick, tick_a, tick_b, amount0, amount1, decimal0, decimal1):
    sqrt = (1.0001 ** (tick / 2) * (2 ** 96))
    sqrt_a = (1.0001 ** (tick_a / 2) * (2 ** 96))
    sqrt_b = (1.0001 ** (tick_b / 2) * (2 ** 96))
    if sqrt_a > sqrt_b:
        (sqrt_a, sqrt_b) = (sqrt_b, sqrt_a)

    if sqrt <= sqrt_a:

        liquidity0 = get_liquidity0(sqrt_a, sqrt_b, amount0, decimal0)
        return liquidity0
    elif sqrt_b > sqrt > sqrt_a:

        liquidity0 = get_liquidity0(sqrt, sqrt_b, amount0, decimal0)
        liquidity1 = get_liquidity1(sqrt_a, sqrt, amount1, decimal1)

        liquidity = liquidity0 if liquidity0 < liquidity1 else liquidity1
        return liquidity

    else:
        liquidity1 = get_liquidity1(sqrt_a, sqrt_b, amount1, decimal1)
        return liquidity1
