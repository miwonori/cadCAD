from typing import Dict, List
from collections import defaultdict
from itertools import product
import warnings
from collections import namedtuple


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

    def __str__(self):
        filtered_members = {k: v for k, v in self.__dict__.items() if k != 'obj'}
        return f"{filtered_members}"


class UDC(object):
    def __init__(self, obj):
        d = vars(obj) # somehow is enough
        d['obj'] = obj

        self.members_dict = d

    def get_members(self):
        return self.members_dict

    def get_object(self):
        return objectview(self.members_dict)

    def get_namedtuple(self):
        return namedtuple("Hydra", self.members_dict.keys())(*self.members_dict.values())


# class UDC_Wrapper2(object):
#     def __init__(self, obj, functions):
#
#         self.obj = obj
#
#     def get_object(self):
#         return objectview(self.obj.__dict__)


def pipe(x):
    return x


def print_pipe(x):
    print(x)
    return x


def flattenDict(l):
    def tupalize(k, vs):
        l = []
        if isinstance(vs, list):
            for v in vs:
                l.append((k, v))
        else:
            l.append((k, vs))
        return l

    flat_list = [tupalize(k, vs) for k, vs in l.items()]
    flat_dict = [dict(items) for items in product(*flat_list)]
    return flat_dict


def flatten(l):
    if isinstance(l, list):
        return [item for sublist in l for item in sublist]
    elif isinstance(l, dict):
        return flattenDict(l)


def flatMap(f, collection):
    return flatten(list(map(f, collection)))


def dict_filter(dictionary, condition):
    return dict([(k, v) for k, v in dictionary.items() if condition(v)])


def get_max_dict_val_len(g: Dict[str, List[int]]) -> int:
    return len(max(g.values(), key=len))


def tabulate_dict(d: Dict[str, List[int]]) -> Dict[str, List[int]]:
    max_len = get_max_dict_val_len(d)
    _d = {}
    for k, vl in d.items():
        if len(vl) != max_len:
            _d[k] = vl + list([vl[-1]] * (max_len-1))
        else:
            _d[k] = vl

    return _d


def flatten_tabulated_dict(d: Dict[str, List[int]]) -> List[Dict[str, int]]:
    max_len = get_max_dict_val_len(d)
    dl = [{} for i in range(max_len)]

    for k, vl in d.items():
        for v, i in zip(vl, list(range(len(vl)))):
            dl[i][k] = v

    return dl


def contains_type(_collection, type):
    return any(isinstance(x, type) for x in _collection)


def drop_right(l, n):
    return l[:len(l) - n]

# backwards compatibility
# ToDo: Encapsulate in function
def key_filter(l, keyname):
    if (type(l) == list):
        return [v[keyname] for v in l]
        # Keeping support to dictionaries for backwards compatibility
        # Should be removed in the future
    warnings.warn(
        "The use of a dictionary to describe Partial State Update Blocks will be deprecated. Use a list instead.",
        FutureWarning)
    return [v[keyname] for k, v in l.items()]


def groupByKey(l):
    d = defaultdict(list)
    for key, value in l:
        d[key].append(value)
    return list(dict(d).items()).pop()


# @curried
def rename(new_name, f):
    f.__name__ = new_name
    return f


def curry_pot(f, *argv):
    sweep_ind = f.__name__[0:5] == 'sweep'
    arg_len = len(argv)
    if sweep_ind is True and arg_len == 4:
        return f(argv[0])(argv[1])(argv[2])(argv[3])
    elif sweep_ind is False and arg_len == 4:
        return f(argv[0], argv[1], argv[2], argv[3])
    elif sweep_ind is True and arg_len == 3:
        return f(argv[0])(argv[1])(argv[2])
    elif sweep_ind is False and arg_len == 3:
        return f(argv[0], argv[1], argv[2])
    else:
        raise TypeError('curry_pot() needs 3 or 4 positional arguments')

# def curry_pot(f, *argv):
#     sweep_ind = f.__name__[0:5] == 'sweep'
#     arg_len = len(argv)
#     if sweep_ind is True and arg_len == 4:
#         return f(argv[0])(argv[1])(argv[2])(argv[3])
#     elif sweep_ind is False and arg_len == 4:
#         return f(argv[0])(argv[1])(argv[2])(argv[3])
#     elif sweep_ind is True and arg_len == 3:
#         return f(argv[0])(argv[1])(argv[2])
#     elif sweep_ind is False and arg_len == 3:
#         return f(argv[0])(argv[1])(argv[2])
#     else:
#         raise TypeError('curry_pot() needs 3 or 4 positional arguments')

# def rename(newname):
#     def decorator(f):
#         f.__name__ = newname
#         return f
#     return decorator
