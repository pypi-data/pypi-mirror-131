from typing import List, Union
from .operand_ import Operand
from .operator_ import Operator
from math import pi, e, tau
from math import factorial
from math import log10, log
from math import sin, cos, tan, sinh, cosh, tanh, asin, acos, atan, asinh, acosh, atanh

Bundle = List[Union[Operand, Operator]]


# Basics bundle
BASICS: Bundle = [
    Operator(symbol='+', func=lambda a, b: a + b, priority=1),
    Operator(symbol='-', func=lambda a, b: a - b, priority=1),
    Operator(symbol='*', func=lambda a, b: a * b, priority=3),
    Operator(symbol='/', func=lambda a, b: a / b, priority=3),
    Operator(symbol='-', func=lambda a: -a, priority=9, operands=1, kind='pre')
]


# Constants bundle
CONSTANTS: Bundle = [
    Operand(value=pi, symbol='pi'),
    Operand(value=e, symbol='e'),
    Operand(value=tau, symbol='tau')
]


# Exponentiation bundle
EXPONENTIATION: Bundle = [
    Operator(symbol='^', func=lambda a, b: a ** b, priority=5),
    Operator(symbol='**', func=lambda a, b: a ** b, priority=5),
    Operator(symbol='log', func=lambda a, b: log(b, a), priority=7, kind='post'),
    Operator(symbol='lg', func=lambda a: log10(a), priority=7, kind='pre', operands=1),
    Operator(symbol='ln', func=lambda a: log(a, e), priority=7, kind='pre', operands=1)
]


# Trigonometry bundle
TRIGONOMETRY: Bundle = [
    Operator(symbol='deg', func=lambda a: pi / 180 * a, priority=7, kind='post', operands=1),
    Operator(symbol='sin', func=lambda a: sin(a), priority=7, kind='pre'),
    Operator(symbol='sine', func=lambda a: sin(a), priority=7, kind='pre'),
    Operator(symbol='cos', func=lambda a: cos(a), priority=7, kind='pre'),
    Operator(symbol='cosine', func=lambda a: cos(a), priority=7, kind='pre'),
    Operator(symbol='tan', func=lambda a: tan(a), priority=7, kind='pre'),
    Operator(symbol='tangent', func=lambda a: tan(a), priority=7, kind='pre'),
]


# Series bundle
# SERIES: Bundle = [
#     Operator(symbol='sum', func=lambda a, b, c: a + b + c, priority=9)
# ]
