from enum import Enum


class Domain(str, Enum):
    CANARY = 'canary'
    REGULAR = 'regular'
