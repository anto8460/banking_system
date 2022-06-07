from enum import Enum


class AccountRanks(str, Enum):
    BASIC = 'basic'
    SILVER = 'silver'
    GOLD = 'gold'
    LOAN = 'loan'
