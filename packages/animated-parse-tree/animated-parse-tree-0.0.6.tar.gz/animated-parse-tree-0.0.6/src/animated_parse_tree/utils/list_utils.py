from typing import Any, Callable, List


def find_element(ls: List, find: Any, default_value: Any, *args):
    try:
        return ls.index(find)
    except ValueError:
        return default_value


def find_element_where(ls: List, condition: Callable[[Any], bool]):
    for el in ls:
        if condition(el):
            return el
    return None


def index_first_element(ls: List, *args):
    return min([find_element(ls=ls, find=el, default_value=len(ls)) for el in args])
