from typing import Type, Callable, Dict, List, Set, Any

from server.model import User
from server.request.request_user import RequestUserCreate


class TypeMapper:
    def __init__(self) -> None:
        self.converters: Dict[(str, str), Callable[[object], object]] = {}

    def add_conversion(self, from_type: Type, to_type: Type, conversion_func: Callable[[object], object]):
        self.converters[(f'{from_type}', f'{to_type}')] = conversion_func

    def convert(self, from_object, to_type: Type):
        from_type = type(from_object)
        converter_key = (f'{from_type}', f'{to_type}')
        if converter_key in self.converters:
            return self.converters[converter_key](from_object)
        raise ValueError(f'Could not find converter for [{from_type} -> {to_type}]')


converter = TypeMapper()

obj_attrs = set(dir(object))
attrs_cache: Dict[Type, Set[str]] = {}


def get_class_attributes(obj: Any) -> Set[str]:
    curr_type = type(obj)
    if curr_type in attrs_cache:
        return attrs_cache[curr_type]
    curr_attrs = set(dir(obj))
    diff_attrs = curr_attrs - obj_attrs
    attrs_cache[curr_type] = set([attrs for attrs in diff_attrs if not attrs.startswith('__')])
    return attrs_cache[curr_type]


def convert_dict_requestusercreate(request: dict) -> RequestUserCreate:
    dict_keys = set(request.keys())
    cls_attrs = get_class_attributes(RequestUserCreate())
    for cls_attr in cls_attrs:
        if cls_attr not in dict_keys:
            raise ValueError(f'Missing [{cls_attr}] in dict for conversion')
    result = RequestUserCreate()
    result.name = request['name']
    result.email = request['email']
    result.first_name = request['first_name']
    result.password = request['password']
    return result


def convert_requestusercreate_user(request: RequestUserCreate) -> User:
    user = User(request.email, request.password)
    user.first_name = request.first_name
    user.name = request.name
    return user


converter.add_conversion(RequestUserCreate, User, convert_requestusercreate_user)
converter.add_conversion(dict, RequestUserCreate, convert_dict_requestusercreate)
