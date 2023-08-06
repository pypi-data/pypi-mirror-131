import ast
from typing import Optional, List
import pymich.exceptions as E


class Type:
    def __init__(self, annotation: Optional[str] = None):
        self.annotation = annotation
        pass

    def __eq__(self, o):
        return type(self) == type(o)

    def python_name(self):
        return self.__str__()

class Unknown(Type):
    def __str__(self):
        return "unknown"

class Unit(Type):
    def __str__(self):
        return "unit"


class Bytes(Type):
    def __str__(self):
        return "bytes"

class PythonInt(Type):
    def __str__(self):
        return "python_int"

class Int(Type):
    def __str__(self):
        return "int"

class Datetime(Type):
    def __str__(self):
        return "int"


class Nat(Type):
    def __str__(self):
        return "int"


class Mutez(Type):
    def __str__(self):
        return "mutez"

class PythonString(Type):
    def __str__(self):
        return "python_string"

class String(Type):
    def __str__(self):
        return "string"


class Bool(Type):
    def __str__(self):
        return "bool"


class Address(Type):
    def __str__(self):
        return "address"

    def python_name(self):
        return "Address"


class Operation(Type):
    def __str__(self):
        return "operation"


class Pair(Type):
    """
    car: first element
    cdr: second element
    """
    def __init__(self, car: Type, cdr: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.car = car
        self.cdr = cdr

    def __eq__(self, o):
        return type(self) == type(o) and self.car == o.car and self.cdr == o.cdr


class Record(Type):
    def __init__(self, name: str, attribute_names: List[str], attribute_types: List[Type], annotation: Optional[str] = None):
        super().__init__(annotation)
        self.name = name
        self.attribute_names = attribute_names
        self.attribute_types = attribute_types

    def __eq__(self, o):
        return type(self) == type(o) and self.attribute_names == o.attribute_names and self.attribute_types == o.attribute_types

    def make_node(self, left, right):
        return Pair(car=left, cdr=right)

    def get_type(self, i=0, acc=None):
        attribute_type = self.attribute_types[i]
        if acc == None:
            acc = self.make_node(None, None)

        if i == 0:
            return self.make_node(attribute_type, self.get_type(i+1))

        elif i == len(self.attribute_types) - 1:
            return attribute_type

        else:
            return self.make_node(attribute_type, self.get_type(i+1))

    def get_attribute_type(self, attribute_name: str):
        attribute_index = self.attribute_names.index(attribute_name)
        return self.attribute_types[attribute_index]


class List(Type):
    def __init__(self, element_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.element_type = element_type

    def __eq__(self, o):
        return type(self) == type(o) and self.element_type == o.element_type

class Spread(Type):
    def __init__(self, element_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.element_type = element_type

    def __eq__(self, o):
        return type(self) == type(o) and self.element_type == o.element_type


class Dict(Type):
    def __init__(self, key_type: Type, value_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.key_type = key_type
        self.value_type = value_type

    def __eq__(self, o):
        return type(self) == type(o) and self.key_type == o.key_type and self.value_type == o.value_type


class BigMap(Type):
    def __init__(self, key_type: Type, value_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.key_type = key_type
        self.value_type = value_type

    def __eq__(self, o):
        return type(self) == type(o) and self.key_type == o.key_type and self.value_type == o.value_type


class Callable(Type):
    def __init__(self, param_type: Type, return_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.param_type = param_type
        self.return_type = return_type

    def __eq__(self, o):
        return type(self) == type(o) and self.param_type == o.param_type and self.return_type == o.return_type


class Contract(Type):
    def __init__(self, param_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.param_type = param_type

    def __eq__(self, o):
        return type(self) == type(o) and self.param_type == o.param_type


base_types = [
    "Nat",
    "Int",
    "str",
    "Address",
    "bool",
    "unit",
    "Mutez",
    "bytes",
    "datetime",
]

polymorphic_types = [
    "Dict",
    "List",
    "Callable",
    "Contract",
]

record_types = [
    "Records"
]

class TypeParser:
    def __init__(self):
        pass

    def parse_name(self, name: ast.Name, e, annotation: Optional[str] = None, lineno = 0) -> Type:
        if name.id == 'Int':
            return Int(annotation)
        if name.id == 'Nat':
            return Nat(annotation)
        if name.id == 'String':
            return String(annotation)
        if name.id == 'Address':
            return Address(annotation)
        if name.id == 'bool':
            return Bool(annotation)
        if name.id == 'unit':
            return Unit(annotation)
        if name.id == 'Mutez':
            return Mutez(annotation)
        if name.id == 'Bytes':
            return Bytes(annotation)
        if name.id == 'datetime':
            return Datetime(annotation)
        if name.id == 'Timestamp':
            return Datetime(annotation)
        if name.id in e.types.keys():
            return e.types[name.id]

        allowed_annotations = base_types + record_types
        raise E.TypeAnnotationDoesNotExistException(name.id, allowed_annotations, lineno)

    def parse_dict(self, dictionary: ast.Subscript, e, annotation: Optional[str] = None):
        key_type = self.parse(dictionary.slice.elts[0], e)
        value_type = self.parse(dictionary.slice.elts[1], e)
        return Dict(key_type, value_type, annotation)

    def parse_callable(self, dictionary: ast.Subscript, e, annotation: Optional[str] = None):
        key_type = self.parse(dictionary.slice.elts[0], e)
        value_type = self.parse(dictionary.slice.elts[1], e)
        return Callable(key_type, value_type, annotation)

    def parse_contract(self, contract: ast.Subscript, e, annotation):
        param_type = self.parse(contract.slice, e)
        return Contract(param_type)

    def parse_list(self, list_: ast.Subscript, e, annotation):
        param_type = self.parse(list_.slice, e)
        return List(param_type)

    def parse_subscript(self, subscript: ast.Subscript, e, annotation: Optional[str] = None, lineno = 0):
        if subscript.value.id == "Dict":
            return self.parse_dict(subscript, e, annotation)
        if subscript.value.id == "BigMap":
            return self.parse_dict(subscript, e, annotation)
        if subscript.value.id == "Map":
            return self.parse_dict(subscript, e, annotation)
        if subscript.value.id == "Callable":
            return self.parse_callable(subscript, e, annotation)
        if subscript.value.id == "Contract":
            return self.parse_contract(subscript, e, annotation)
        if subscript.value.id == "List":
            return self.parse_list(subscript, e, annotation)
        else:
            allowed_annotations = f"only polymorphic types ({polymorphic_types}) are subscriptable"
            raise E.TypeAnnotationDoesNotExistException(subscript.value.id, allowed_annotations, lineno)

    def parse(self, type_ast, e, annotation: Optional[str] = None, lineno = 0) -> Type:
        if type(type_ast) == ast.Name:
            return self.parse_name(type_ast, e, annotation, lineno)
        if type(type_ast) == ast.Subscript:
           return self.parse_subscript(type_ast, e, annotation, lineno)
        if type(type_ast) == ast.Tuple:
            attribute_names = []
            attribute_types = []
            for i, elt in enumerate(type_ast.elts):
                attribute_names.append(str(i))
                attribute_types.append(self.parse(elt, e, annotation, lineno))
            return Record("_", attribute_names, attribute_types)
        if type_ast == None:
            return Unit()
        raise E.TypeAnnotationDoesNotExistException(
            ast.dump(type_ast),
            f"expected a base type ({base_types}) or an polymorphic type ({polymorphic_types})",
            type_ast.lineno
            )
        raise NotImplementedError

