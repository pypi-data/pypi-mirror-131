import ast
import time
import pprint
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

from pytezos.context.impl import ExecutionContext
from pytezos.michelson.instructions.adt import *
from pytezos.michelson.instructions.arithmetic import *
from pytezos.michelson.instructions.control import *
from pytezos.michelson.instructions.stack import *
from pytezos.michelson.instructions.struct import *
from pytezos.michelson.program import *
from pytezos.michelson.repl import InterpreterResult
from pytezos.michelson.sections import CodeSection
from pytezos.michelson.sections.parameter import ParameterSection
from pytezos.michelson.sections.storage import StorageSection
from pytezos.michelson.stack import MichelsonStack
from pytezos.michelson.types import core
from pytezos.michelson.types.core import *
from pytezos.michelson.types.domain import AddressType
from pytezos.michelson.types.map import MapType
from pytezos.michelson.types.operation import *
from pytezos.michelson.types.pair import PairType
from pytezos import ContractInterface

import pymich.instr_types as t
from pymich.instr_types import Datetime, base_types, polymorphic_types, record_types
from pymich.compiler_backend import CompilerBackend
from pymich.macro_expander import macro_expander
from pymich.helpers import Tree, ast_to_tree
from pymich.vm_types import (Array, Contract, Entrypoint, FunctionPrototype, Instr,
                             Pair, Some, MultiArgFunctionPrototype)
import pymich.exceptions as E


def debug(cb):
    def f(*args, **kwargs):
        self = args[0]
        if self.isDebug:
            print(cb.__name__)

        return cb(*args, **kwargs)

    return f


def Comment(msg: str):
    return Instr("COMMENT", [msg], {})


class RecordUtils:
    @staticmethod
    def compile_record(record: t.Record, attribute_values, compile_function, env):
        instructions = []
        for attribute_value, attribute_type in zip(reversed(attribute_values), reversed(record.attribute_types)):
            instructions += compile_function(attribute_value, env, current_type=attribute_type)
        env.sp -= len(attribute_values) - 1
        return instructions + [Instr("PAIR", [len(attribute_values)], {})]

    @staticmethod
    def navigate_to_tree_leaf(record: t.Record, attribute_name, lineno=0):
        if type(record) != t.Record:
            raise E.TypeException(t.Record, type(record), lineno)

        if attribute_name not in record.attribute_names:
            raise E.AttributeException(record, attribute_name, lineno)

        el_number = 1
        for i, candidate in enumerate(record.attribute_names):
            if i == len(record.attribute_names) - 1:
                el_number = 2 * i
            elif attribute_name == candidate:
                el_number = 2 * i + 1
                break

        return [Instr("GET", [t.Int(), el_number], {})]

    @staticmethod
    def update_tree_leaf(record: t.Record, attribute_name, e):
        el_number = 1
        for i, candidate in enumerate(record.attribute_names):
            if i == len(record.attribute_names) - 1:
                el_number = 2 * i
            elif attribute_name == candidate:
                el_number = 2 * i + 1
                break

        e.sp -= 1  # account for update
        return [Instr("UPDATE", [t.Int(), el_number], {})]

@dataclass
class Env:
    vars: Dict[str, int]
    sp: int
    args: Dict[str, List[str]]
    types: Dict[str, t.Type]

    def copy(self):
        return Env(
            self.vars.copy(),
            self.sp,
            self.args.copy(),
            self.types.copy(),
        )


class StdlibVariable:
    def __init__(self, type_: t.Type, compile_callback):
        self.type = type_
        self.compile_callback = compile_callback

class StdlibFunctionSpec:
    def __init__(self, compile_callback, get_prototype: FunctionPrototype):
        self.compile_callback = compile_callback
        self.get_prototype = get_prototype

class StdLibClassSpec:
    def __init__(self):
        self.methods = {}
        self.static_methods = []
        self.constructor = None

    def create_constructor(self, constructor_spec: StdlibFunctionSpec):
        self.constructor = constructor_spec
        return self

    def create_method(self, name: str, method_spec: StdlibFunctionSpec, is_static=False):
        self.methods[name] = method_spec
        if is_static:
            self.static_methods.append(name)
        return self

@dataclass
class StdLibCompileCallbacks:
    sender: Callable
    source: Callable
    amount: Callable
    balance: Callable
    unit: Callable
    datetime: Callable
    dict_safe: Callable
    abs: Callable
    blake2b: Callable
    pack: Callable
    unpack: Callable
    datetime_now: Callable
    datetime_from_timestamp: Callable
    timedelta: Callable
    transaction: Callable
    contract: Callable
    mutez: Callable
    nat: Callable
    int: Callable
    string: Callable
    address: Callable
    list: Callable
    list_prepend: Callable
    map: Callable
    map_set: Callable
    big_map: Callable


class StdLib:
    def __init__(self, compile_callbacks: StdLibCompileCallbacks):
        self.compile_callbacks = compile_callbacks
        dict_object = self.dict_get()
        datetime_object = self.datetime()
        timestamp_object = self.timestamp()
        bytes_object = self.bytes()
        list_object = self.list()
        map_object = self.map()
        big_map_object = self.big_map()
        self.constants_mapping = {
            "SENDER": self.sender(),
            "SOURCE": self.source(),
            "AMOUNT": self.amount(),
            "BALANCE": self.balance(),
            "Unit": self.unit(),
            "dic_get": dict_object,
            "abs": self.abs(),
            "datetime": datetime_object,
            "timedelta": self.timedelta(),
            "transaction": self.transaction(),
            "Contract": self.contract(),
            "Bytes": bytes_object,
            "String": self.string(),
            "Mutez": self.mutez(),
            "Nat": self.nat(),
            "Int": self.int(),
            "Address": self.address(),
            "Timestamp": timestamp_object,
            "List": list_object,
            "Map": map_object,
            "BigMap": big_map_object,
        }
        self.types_mapping = {
            t.Dict: map_object,
            t.BigMap: map_object,
            t.Datetime: timestamp_object,
            t.Bytes: bytes_object,
            t.List: list_object,
        }

    def list(self):
        list_constructor = StdlibFunctionSpec(
            self.compile_callbacks.list,
            lambda element_types: FunctionPrototype(
                t.Spread(element_types[0]),
                t.List(element_types[0]),
            )
        )
        list_prepend = StdlibFunctionSpec(
            self.compile_callbacks.list_prepend,
            lambda el_type: FunctionPrototype(
                el_type,
                t.List(el_type),
            )
        )
        list_object = StdLibClassSpec()
        list_object.create_constructor(list_constructor)
        list_object.create_method("prepend", list_prepend, False)

        return list_object

    def big_map(self):
        big_map_constructor = StdlibFunctionSpec(
            self.compile_callbacks.big_map,
            lambda element_types: FunctionPrototype(
                t.Unit(),
                t.Dict(element_types[0].get_attribute_type("0"), element_types[0].get_attribute_type("1")),
            )
        )
        big_map_set = StdlibFunctionSpec(
            self.compile_callbacks.map_set,
            lambda el_type: FunctionPrototype(
                el_type,
                t.Dict(el_type.key_type, el_type.value_type),
            )
        )
        big_map_get = StdlibFunctionSpec(
            self.compile_callbacks.dict_safe,
            lambda big_map_type: FunctionPrototype(
                big_map_type.key_type,
                big_map_type.value_type,
            )
        )
        big_map_object = StdLibClassSpec()
        big_map_object.create_constructor(big_map_constructor)
        big_map_object.create_method("get", big_map_get)
        big_map_object.create_method("add", big_map_set, False)

        return big_map_object

    def map(self):
        map_constructor = StdlibFunctionSpec(
            self.compile_callbacks.map,
            lambda element_types: FunctionPrototype(
                t.Unit(),
                t.Dict(element_types[0].get_attribute_type("0"), element_types[0].get_attribute_type("1")),
            )
        )
        map_set = StdlibFunctionSpec(
            self.compile_callbacks.map_set,
            lambda el_type: FunctionPrototype(
                el_type,
                t.Dict(el_type.key_type, el_type.value_type),
            )
        )
        map_get = StdlibFunctionSpec(
            self.compile_callbacks.dict_safe,
            lambda map_type: FunctionPrototype(
                map_type.key_type,
                map_type.value_type,
            )
        )
        map_object = StdLibClassSpec()
        map_object.create_constructor(map_constructor)
        map_object.create_method("get", map_get)
        map_object.create_method("add", map_set, False)

        return map_object

    def sender(self):
        return StdlibVariable(t.Address(), self.compile_callbacks.sender)

    def source(self):
        return StdlibVariable(t.Address(), self.compile_callbacks.source)

    def amount(self):
        return StdlibVariable(t.Mutez(), self.compile_callbacks.amount)

    def balance(self):
        return StdlibVariable(t.Mutez(), self.compile_callbacks.balance)

    def unit(self):
        return StdlibVariable(t.Unit(), self.compile_callbacks.unit)

    def timestamp(self):
        timestamp_constructor = StdlibFunctionSpec(
            self.compile_callbacks.datetime_from_timestamp,
            lambda _: FunctionPrototype(
                t.PythonInt(),
                t.Datetime()
            )
        )
        timestamp_now = StdlibFunctionSpec(
            self.compile_callbacks.datetime_now,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Datetime()
            )
        )
        timestamp_object = StdLibClassSpec()
        timestamp_object.create_constructor(timestamp_constructor)
        timestamp_object.create_method("now", timestamp_now, True)

        return timestamp_object

    def datetime(self):
        """Obselete"""
        datetime_constructor = StdlibFunctionSpec(
            self.compile_callbacks.datetime,
            lambda _: MultiArgFunctionPrototype(
                [t.PythonInt(), t.PythonInt(), t.PythonInt(), t.PythonInt(), t.PythonInt()],
                t.Datetime()
            )
        )
        datetime_now = StdlibFunctionSpec(
            self.compile_callbacks.datetime_now,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Datetime()
            ),
        )
        datetime_object = StdLibClassSpec()
        datetime_object.create_constructor(datetime_constructor)
        datetime_object.create_method("now", datetime_now, True)

        return datetime_object

    def dict_get(self):
        dict_get = StdlibFunctionSpec(
            self.compile_callbacks.dict_safe,
            lambda dict_type: FunctionPrototype(
                t.Unit(),
                dict_type.value_type,
            )
        )
        dict_object = StdLibClassSpec()
        dict_object.create_method("get", dict_get)
        return dict_object

    def abs(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.abs,
            lambda: FunctionPrototype(
                t.Int(),
                t.Nat()
            )
        )

    def bytes(self):
        bytes_constructor = StdlibFunctionSpec(
            self.compile_callbacks.pack,
            lambda _: FunctionPrototype(
                t.Unknown(),
                t.Bytes()
            )
        )
        bytes_unpack = StdlibFunctionSpec(
            self.compile_callbacks.unpack,
            lambda ty: FunctionPrototype(
                ty,
                ty
            )
        )
        bytes_blake2b = StdlibFunctionSpec(
            self.compile_callbacks.blake2b,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Bytes()
            )
        )

        bytes_object = StdLibClassSpec()
        bytes_object.create_constructor(bytes_constructor)
        bytes_object.create_method("unpack", bytes_unpack, False)
        bytes_object.create_method("blake2b", bytes_blake2b, False)

        return bytes_object

    def timedelta(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.timedelta,
            lambda: MultiArgFunctionPrototype(
                [t.Int(), t.Int(), t.Int(), t.Int(), t.Int()],
                t.Int()
            )
        )

    def transaction(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.transaction,
            lambda contract_type: MultiArgFunctionPrototype(
                [t.Contract([contract_type]), t.Mutez(), contract_type],
                t.Operation()
            )
        )

    def contract(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.contract,
            lambda contract_type: FunctionPrototype(
                [t.Address()],
                t.Contract()
            )
        )

    def mutez(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.mutez,
            lambda: FunctionPrototype(t.PythonInt(), t.Mutez())
        )

    def nat(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.nat,
            lambda: FunctionPrototype(t.PythonInt(), t.Nat())
        )

    def int(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.int,
            lambda: FunctionPrototype(t.PythonInt(), t.Int())
        )

    def string(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.string,
            lambda: FunctionPrototype(t.PythonString(), t.String())
        )

    def address(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.address,
            lambda: FunctionPrototype(t.PythonString(), t.Address())
        )


class TypeChecker:
    def __init__(self, std_lib: StdLib, type_parser: t.TypeParser) -> None:
        self.std_lib = std_lib
        self.type_parser = type_parser

    def get_name_type(self, node, e: Env):
        if node.id in e.types:
            return e.types[node.id]
        elif node.id in self.std_lib.constants_mapping:
            if type(self.std_lib.constants_mapping[node.id]) == StdlibVariable:
                return self.std_lib.constants_mapping[node.id].type

            return self.std_lib.constants_mapping[node.id]
        else:
            raise E.NameException(node.id, node.lineno)

    def get_list_type(self, node, e: Env):
        if len(node.elts):
            elt_type = self.get_expression_type(node.elts[0], e)
            return t.List(elt_type)
        else:
            return t.List(t.Unknown())

    def get_dict_type(self, node, e: Env):
        if len(node.keys):
            key_type = self.get_expression_type(node.keys[0], e)
            value_type = self.get_expression_type(node.values[0], e)
            return t.Dict(key_type, value_type)
        else:
            return t.Dict(t.Unknown(), t.Unknown())

    def get_constant_type(self, node, e: Env):
        if type(node.value) == str:
            return t.PythonString()
        elif type(node.value) == int:
            return t.PythonInt()
        elif type(node.value) == bool:
            return t.Bool()
        else:
            raise E.TypeException(["str", "int", "bool"], node.value, node.lino)

    def get_subscript_type(self, node, e: Env):
        parent_type = self.get_expression_type(node.value, e)
        if type(parent_type) == t.Dict:
            return parent_type.value_type
        elif type(parent_type) == t.List:
            return parent_type.element_type
        elif type(parent_type) == StdLibClassSpec:
            cast_type = self.type_parser.parse(node.slice, e)
            return parent_type.constructor.get_prototype([cast_type]).return_type
        else:
            raise E.TypeException(polymorphic_types, parent_type, e)

    def get_attribute_type(self, node, e: Env):
        record = self.get_expression_type(node.value, e)
        if type(record) == StdLibClassSpec:
            if type(node.value) == ast.Name:
                record = record.constructor.get_prototype(t.Unknown()).return_type
            elif type(record.value) == ast.Call:
                arg_types = [self.get_expression_type(arg, e) for arg in node.args]
                record = record.constructor.get_prototype(arg_types).return_type

        attr_value_type = type(record)
        if attr_value_type in self.std_lib.types_mapping:
            if node.attr in self.std_lib.types_mapping[attr_value_type].methods:
                return self.std_lib.types_mapping[attr_value_type].methods[node.attr].get_prototype(record).return_type

        if node.attr in record.attribute_names:
            return record.get_attribute_type(node.attr)
        else:
            raise E.AttributeException(record, node.attr, node.lineno)

    def get_call_type(self, node, e: Env):
        if type(node.func) == ast.Name and node.func.id in e.types:
            if type(e.types[node.func.id]) == t.Record:
                return e.types[node.func.id]
            else:
                return e.types[node.func.id].return_type
        elif type(node.func) == ast.Name and node.func.id in self.std_lib.constants_mapping:
            if type(self.std_lib.constants_mapping[node.func.id]) == StdlibFunctionSpec:
                return self.std_lib.constants_mapping[node.func.id].get_prototype().return_type
            elif type(self.std_lib.constants_mapping[node.func.id]) == StdLibClassSpec:
                arg_types = [self.get_expression_type(arg, e) for arg in node.args]
                return self.std_lib.constants_mapping[node.func.id].constructor.get_prototype(arg_types).return_type
            else:
                raise E.CompilerException(f"Stdlib expression {node.func.id} cannot be typed", node.lineno)
        else:
            return self.get_expression_type(node.func, e)

    def get_compare_type(self, node, e: Env):
        return t.Bool()

    def get_binop_type(self, node, e: Env):
        return self.get_expression_type(node.left, e)

    def get_expression_type(self, node, e: Env):
        if type(node) == ast.Name:
            return self.get_name_type(node, e)
        elif type(node) == ast.List:
            return self.get_list_type(node, e)
        elif type(node) == ast.Dict:
            return self.get_dict_type(node, e)
        elif type(node) == ast.Constant:
            return self.get_constant_type(node, e)
        elif type(node) == ast.Subscript:
            return self.get_subscript_type(node, e)
        elif type(node) == ast.Attribute:
            return self.get_attribute_type(node, e)
        elif type(node) == ast.Call:
            return self.get_call_type(node, e)
        elif type(node) == ast.BinOp:
            return self.get_binop_type(node, e)
        elif type(node) == ast.Compare:
            return self.get_compare_type(node, e)
        else:
            raise E.CompilerException(f"Expression {node} cannot be typed", node.lineno)

class Compiler:
    def __init__(self, src: str = "", isDebug=False):
        self.ast = ast.parse(src)
        self.isDebug = isDebug
        self.type_parser = t.TypeParser()
        self.contract = Contract(
            storage_type=t.Int(),
            storage=0,
            entrypoints={},
            instructions=[],
        )

        compile_callbacks = StdLibCompileCallbacks(
            sender=self.get_sender,
            source=self.get_source,
            amount=self.get_amount,
            balance=self.compile_balance,
            unit=self.compile_unit,
            datetime=self.compile_datetime,
            dict_safe=self._compile_dict_safe_get,
            abs=self._compile_abs,
            blake2b=self._compile_blake2b,
            pack=self._compile_pack,
            unpack=self._compile_unpack,
            timedelta=self._compile_timedelta,
            datetime_now=self.compile_datetime_now,
            datetime_from_timestamp=self.compile_datetime_from_timestamp,
            transaction=self._compile_transaction,
            contract=self._compile_cast_address_to_contract,
            mutez=self._compile_mutez,
            nat=self._compile_nat,
            int=self._compile_int,
            string=self._compile_string,
            address=self._compile_address,
            list=self.compile_list_new,
            list_prepend=self.compile_list_prepend,
            map=self.compile_dict_new,
            map_set=self.compile_dict_set,
            big_map=self.compile_big_map,
        )
        stdlib = StdLib(compile_callbacks)
        self.type_checker = TypeChecker(stdlib, self.type_parser)
        self.std_lib_types = stdlib.types_mapping
        self.std_lib = stdlib.constants_mapping

    def _compile_pack(self, node: ast.Call, e: Env) -> List[Instr]:
        instructions = self._compile(node.args[0], e)
        return instructions + [Instr("PACK", [], {})]

    def _compile_unpack(self, cast_type_name: ast.Name, e: Env) -> List[Instr]:
        cast_type = self.type_parser.parse(cast_type_name, e)
        return [
            Instr("UNPACK", [cast_type], {}),
            Instr("IF_NONE", [
                [
                    Instr("PUSH", [t.String(), "Cannot unpack"], {}),
                    Instr("FAILWITH", [], {})
                ],
                [],
            ], {}),
        ]

    def _compile_blake2b(self, e: Env) -> List[Instr]:
        return [Instr("BLAKE2B", [], {})]

    def _compile_abs(self, node: ast.Call, e: Env) -> List[Instr]:
        instructions = self._compile(node.args[0], e)
        return instructions + [Instr("ABS", [], {})]

    def compile_datetime_from_timestamp(self, timestamp: ast.Call, e: Env) -> List[Instr]:
        if type(timestamp) == ast.Call:
            if type(timestamp.args[0]) == ast.Constant:
                value = timestamp.args[0].value
                if type(value) == int:
                    return [Instr("PUSH", [t.Datetime(), value], {})]

        raise E.CompilerException("Can only construct a Timestamp object from a Python integer literal", timestamp.lineno)

    def _compile_timedelta(self, node: ast.Call, e: Env) -> List[Instr]:
        timedelta_spec = []
        for arg in node.args:
            if type(arg) == ast.Constant:
                timedelta_spec.append(arg.value)
            else:
                raise E.CompilerException("timedelta constructor can only be called with integer literal arguments currently", node.lineno)

        e.sp += 1
        seconds = int(timedelta(*timedelta_spec).total_seconds())
        return [Instr("PUSH", [t.Int(), seconds], {})]

    def compile_datetime(self, node: ast.Call, e: Env) -> List[Instr]:
        timestamp_spec = []
        for arg in node.args:
            if type(arg) == ast.Constant:
                timestamp_spec.append(arg.value)
            else:
                raise E.CompilerException("datetime constructor can only be called with integer literal arguments currently", node.lineno)

        e.sp += 1
        timestamp = int(time.mktime(datetime(*timestamp_spec).timetuple()))
        return [Instr("PUSH", [t.Datetime(), timestamp], {})]

    def compile_datetime_now(self, e: Env) -> List[Instr]:
        e.sp += 1
        return [Instr("NOW", [], {})]

    def print_ast(self):
        print(pprint.pformat(ast_to_tree(self.ast)))

    def compile_module(self, m: ast.Module, e: Env) -> List[Instr]:
        instructions: List[Instr] = []
        for key, value in ast.iter_fields(m):
            if key == "body":
                for childNode in value:
                    if type(childNode) == ast.ClassDef:
                        if childNode.name == "Contract":
                            instructions += self._compile(childNode, e, instructions)
                        else:
                            instructions += self._compile(childNode, e)
                    else:
                        instructions += self._compile(childNode, e)

        return instructions

    def _compile_reassign(self, reassign_ast: ast.Assign, e: Env) -> List[Instr]:
        instructions: List[Instr] = []
        var_name = reassign_ast.targets[0]
        value = reassign_ast.value
        var_addr = e.vars[var_name.id]
        instructions = self._compile(value, e)
        free_vars_instructions, _ = self.free_var(var_name.id, e)
        instructions = instructions + free_vars_instructions + [
            Instr("DUG", [e.sp - var_addr], {}),
        ]
        e.vars[var_name.id] = var_addr

        try:
            if reassign_ast.value.func.id in e.types:
                e.types[var_name.id] = reassign_ast.value.func.id
        except:
            pass

        try:
            print_val = value.value
        except:
            print_val = "[object]"
        return [Comment(f"Reassigning {var_name.id} = {print_val}")] + instructions

    def compile_big_map(self, node: ast.Call, e: Env) -> List[Instr]:
        instructions = [
            Instr(
                "EMPTY_BIG_MAP",
                [
                    self.current_type.key_type,
                    self.current_type.value_type,
                ],
                {}
            )
        ]
        e.sp += 1  # account for pushing dict

        return instructions

    def compile_dict_new(self, node: ast.Call, e: Env) -> List[Instr]:
        instructions = [
            Instr(
                "EMPTY_MAP",
                [
                    self.current_type.key_type,
                    self.current_type.value_type,
                ],
                {}
            )
        ]
        e.sp += 1  # account for pushing dict

        return instructions

    def compile_dict_set(self, key, value, e: Env) -> List[Instr]:
        set_dict = [
            *self._compile(value, e),
            Instr("SOME", [], {}),
            *self._compile(key, e),
            Instr("UPDATE", [], {})
        ]
        e.sp -= 2
        return set_dict

    def compile_dict(self, dict_ast: ast.Dict, e: Env, dict_type: t.Dict=None) -> List[Instr]:
        if dict_type:
            key_type = dict_type.key_type
            value_type = dict_type.value_type
        elif len(dict_ast.keys):
            key_type = self.type_checker.get_expression_type(dict_ast.keys[0], e)
            value_type = self.type_checker.get_expression_type(dict_ast.values[0], e)
        else:
            raise E.CompilerException(f"Empty dictionary declared without a type annotation and cannot be inferred", {dict_ast.lineno})

        instructions = [Instr("EMPTY_MAP", [key_type, value_type], {})]
        e.sp += 1  # account for pushing dict

        if len(dict_ast.keys):
            for key, value in zip(dict_ast.keys, dict_ast.values):
                instructions += self._compile(value, e)
                instructions += [Instr("SOME", [], {})]
                instructions += self._compile(key, e)
                instructions += [Instr("UPDATE", [], {})]
                e.sp -= 2

        return instructions

    def compile_literal(self, literal, e: Env) -> List[Instr]:
        if type(literal) == ast.Dict:
            return self.compile_dict(literal, e)
        if type(literal) == ast.List:
            return self.compile_list(literal, e)
        else:
            return self.compile_expr(literal, e)

    def _is_literal(self, literal_ast):
        if type(literal_ast) == ast.Dict:
            return True
        elif type(literal_ast) == ast.List:
            return True
        else:
            return False

    @debug
    def compile_ann_assign(self, assign: ast.AnnAssign, e: Env) -> List[Instr]:
        try:
            # is reassignment
            if assign.targets[0].id in e.vars.keys():
                raise E.CompilerException("Cannot reassign with annotation", assign.targets[0].lineno)
        except:
            pass

        instructions: List[Instr] = []
        var_name = assign.target

        compiled_value = self._compile(assign.value, e, current_type=self.type_parser.parse(assign.annotation, e, lineno=assign.lineno))

        value = assign.value
        instructions = self._compile(var_name, e) + compiled_value
        e.vars[var_name.id] = e.sp

        e.types[var_name.id] = self.type_parser.parse(assign.annotation, e)

        return instructions

    def _fetch_variable(self, var_name: str, e: Env) -> List[Instr]:
        jump_length = e.sp - e.vars[var_name]
        e.sp += 1
        return [
            Instr("DUP", [jump_length + 1], {}),
        ]

    def _replace_var(self, var_name: str, e: Env) -> List[Instr]:
        # override new record with old record
        old_record_location = e.vars[var_name]
        free_old_record, _ = self.free_var(var_name, e)
        move_back_new_record= [
            Instr("DUG", [e.sp - old_record_location], {}),
        ]
        e.vars[var_name] = old_record_location

        return free_old_record + move_back_new_record

    def _get_set_nested_expr_spec(self, node, e: Env, spec = None):
        if spec is None:
            spec = []

        def var_spec(var_name):
            return {
                "type": "FETCH",
                "value": var_name.id,
                "lineno": var_name.lineno
            }

        def attr_spec(record, attr_name, lineno):
            return {
                "type": "ATTR",
                "value": {
                    "record": record,
                    "key": attr_name
                },
                "lineno": lineno
            }

        def subscript_spec(subscript_ast: ast.expr):
            return {
                "type": "SUBSCRIPT",
                "value": subscript_ast,
                "lineno": subscript_ast.lineno
            }

        if type(node) == ast.Name:
            spec.append(var_spec(node))
        elif type(node) == ast.Attribute:
            record = self.type_checker.get_expression_type(node.value, e)
            record_key = node.attr
            spec += self._get_set_nested_expr_spec(node.value, e)
            spec.append(attr_spec(record, record_key, node.lineno))
        elif type(node) == ast.Subscript:
            # TODO throw error if list
            spec += self._get_set_nested_expr_spec(node.value, e)
            spec.append(subscript_spec(node.slice))

        return spec

    def compile_assign_record(self, node, e: Env, instructions = None):
        if instructions is None:
            instructions = []

        key_type = self.type_checker.get_expression_type(node.targets[0], e)
        value_type = self.type_checker.get_expression_type(node.value, e)
        if key_type != value_type:
            raise E.TypeException(key_type, value_type, node.lineno)

        #instructions += self._get_record_with_replace(node.targets[0], e)
        spec = self._get_set_nested_expr_spec(node.targets[0], e)

        not_a_valid_nesting_error_message = "Only attribute and subscript notations are currently allowed when assigning to a nested expression"

        # fetch record to update
        for i, spec_element in enumerate(spec[:-1]):
            if spec_element["type"] == "FETCH":
                instructions += self._fetch_variable(spec_element["value"], e)
            elif spec_element["type"] == "ATTR":
                instructions += RecordUtils.navigate_to_tree_leaf(spec_element["value"]["record"], spec_element["value"]["key"])
            elif spec_element["type"] == "SUBSCRIPT":
                instructions += self._compile(spec_element["value"], e)
                instructions += self._compile_get_subscript(e)
            else:
                raise CompilerException(not_a_valid_nesting_error_message, spec_element["lino"])

            instructions += [Instr("DUP", [], {})]
            e.sp += 1

        instructions = instructions[:-1]
        e.sp -= 1

        instructions += self._compile(node.value, e)

        for i, spec_element in enumerate(reversed(spec)):
            if spec_element["type"] == "FETCH":
                # replace var
                instructions += self._replace_var(spec_element["value"], e)
            elif spec_element["type"] == "ATTR":
                instructions += RecordUtils.update_tree_leaf(spec_element["value"]["record"], spec_element["value"]["key"], e)
            elif spec_element["type"] == "SUBSCRIPT":
                instructions += [Instr("SOME", [], {})]
                instructions += self._compile(spec_element["value"], e)
                instructions += [Instr("UPDATE", [], {})]
                e.sp -= 2
            else:
                raise CompilerException(not_a_valid_nesting_error_message, spec_element["lino"])

        return instructions

    @debug
    def compile_assign(self, assign: ast.Assign, e: Env) -> List[Instr]:
        # TODO remove try and condition on type instead
        try:
            if assign.targets[0].id in e.vars.keys():
                return self._compile_reassign(assign, e)
        except:
            pass

        # Handle record key assignments
        if type(assign.targets[0]) == ast.Attribute or type(assign.targets[0]) == ast.Subscript:
            return self.compile_assign_record(assign, e)

        # type variable
        e.types[assign.targets[0].id] = self.type_checker.get_expression_type(assign.value, e)

        instructions: List[Instr] = []
        var_name = assign.targets[0]

        if self._is_literal(assign.value):
            compiled_value = self.compile_literal(assign.value, e)
        else:
            compiled_value = self._compile(assign.value, e)

        value = assign.value
        instructions = self._compile(var_name, e) + compiled_value
        e.vars[var_name.id] = e.sp

        if type(assign.value) == ast.Call():
            if assign.value.func.id in e.types:
                e.types[var_name.id] = e.types[assign.value.func.id].return_type#assign.value.func.id

        try:
            print_val = value.value
        except:
            print_val = "[object]"
        return [Comment(f"{var_name.id} = {print_val}")] + instructions

    @debug
    def compile_expr(self, expr: ast.Expr, e: Env) -> List[Instr]:
        return self._compile(expr.value, e)

    def _is_string_address(self, string: str) -> bool:
        is_tz_address = len(string) == 36 and string[:2] == "tz"
        is_kt_address = len(string) == 36 and string[:2] == "KT"
        return is_tz_address or is_kt_address

    @debug
    def compile_constant(self, constant: ast.Constant, e: Env, force_type = None) -> List[Instr]:
        e.sp += 1  # Account for PUSH

        constant_type: t.Type = t.Int()
        if force_type != None:
            constant_type = force_type
        elif type(constant.value) == str:
            if self._is_string_address(constant.value):
                constant_type = t.Address()
            else:
                constant_type = t.String()
        elif type(constant.value) == int:
            constant_type = t.PythonInt()
        elif type(constant.value) == bool:
            constant_type = t.Bool()
        else:
            raise E.CompilerException(f"Can only compile {base_types}", constant.lineno)

        return [
            Instr("PUSH", [constant_type, constant.value], {}),
        ]

    def compile_unit(self, name: ast.Name, e: Env) -> List[Instr]:
        e.sp += 1
        return [Instr("UNIT", [], {})]

    def compile_balance(self, name: ast.Name, e: Env) -> List[Instr]:
        e.sp += 1
        return [Instr("BALANCE", [], {})]

    @debug
    def compile_name(self, name: ast.Name, e: Env) -> List[Instr]:
        if name.id in self.std_lib and type(self.std_lib[name.id]) == StdlibVariable:
            return self.std_lib[name.id].compile_callback(name, e)

        var_name = name

        if type(name.ctx) == ast.Load:
            if var_name.id not in e.vars:
                raise E.NameException(var_name.id, name.lineno)
            return self._fetch_variable(var_name.id, e)
        elif type(name.ctx) == ast.Store:
            # will get set to actual value in `compile_assign`
            e.vars[var_name.id] = 42
            return []
        else:
            raise E.CompilerException("Can only 'load' and 'store' name", name.lineno)

    @debug
    def compile_binop(self, t: ast.BinOp, e: Env) -> List[Instr]:
        left = self._compile(t.right, e)
        right = self._compile(t.left, e)
        op = self._compile(t.op, e)
        return left + right + op

    @debug
    def compile_sub(self, t: ast.Sub, e: Env) -> List[Instr]:
        e.sp -= 1  # Account for SUB
        return [
            Instr("SUB", [], {}),
        ]

    @debug
    def compile_add(self, t: ast.Add, e: Env) -> List[Instr]:
        e.sp -= 1  # Account for ADD
        return [
            Instr("ADD", [], {}),
        ]

    @debug
    def compile_mult(self, t: ast.Mult, e: Env) -> List[Instr]:
        e.sp -= 1  # Account for MUL
        return [
            Instr("MUL", [], {}),
        ]

    def compile_floor_div(self, node: ast.FloorDiv, e: Env) -> List[Instr]:
        e.sp -= 1  # Account for DIV
        return [
            Instr("EDIV", [], {}),
            Instr("IF_NONE", [
                [
                    Instr("PUSH", [t.String(), "Division by 0 not allowed"], {}),
                    Instr("FAILWITH", [], {})
                ],
                [],
            ], {}),
            Instr("CAR", [], {}),
        ]

    def compile_modulo(self, node: ast.Mod, e: Env) -> List[Instr]:
        e.sp -= 1  # Account for MOD
        return [
            Instr("EDIV", [], {}),
            Instr("IF_NONE", [
                [
                    Instr("PUSH", [t.String(), "Division by 0 not allowed"], {}),
                    Instr("FAILWITH", [], {})
                ],
                [],
            ], {}),
            Instr("CDR", [], {}),
        ]

    @debug
    def create_list(self, e: Env, elt_type: Type) -> List[Instr]:
        e.sp += 1  # Account for pushing list
        return [
            Instr("NIL", [elt_type], {}),
        ]

    @debug
    def append_before_list_el(self, el, e) -> List[Instr]:
        instructions = self._compile(el, e) + [Instr("CONS", [], {})]
        e.sp -= 1
        return instructions

    def compile_list_prepend(self, node: ast.Call, e: Env) -> List[Instr]:
        element = self._compile(node, e)
        return element + [Instr("CONS", [], {})]

    @debug
    def compile_list_new(self, node: ast.Call, e: Env) -> List[Instr]:
        list_type = self.current_type
        if len(node.args):
            elt_type = self.type_checker.get_expression_type(node.args[0], e)
        else:
            if type(list_type) == t.List:
                elt_type = list_type.element_type
            else:
                raise E.CompilerException(f"Empty List declared without a type annotation and cannot be inferred", {node.lineno})

        instructions = self.create_list(e, elt_type)
        for el in reversed(node.args):
            instructions += self.append_before_list_el(el, e)
        return instructions

    @debug
    def compile_list(self, l: ast.List, e: Env) -> List[Instr]:
        list_type = self.current_type
        if len(l.elts):
            elt_type = self.type_checker.get_expression_type(l.elts[0], e)
        else:
            if list_type and type(list_type) == t.List:
                elt_type = list_type.element_type
            else:
                raise E.CompilerException(f"Empty List declared without a type annotation and cannot be inferred", {l.lineno})

        instructions = self.create_list(e, elt_type)
        for el in reversed(l.elts):
            instructions += self.append_before_list_el(el, e)
        return instructions

    def free_var(self, var_name, e: Env):
        var_location = e.vars[var_name]
        comment = [Comment(f"Freeing var {var_name} at {var_location}, e.sp = {e.sp}")]

        jump = e.sp - var_location
        e.sp -= 1  # account for freeing var
        del e.vars[var_name]

        return (
            comment
            + [
                Instr(
                    "DIP",
                    [
                        jump,
                        [
                            Instr("DROP", [], {}),
                        ],
                    ],
                    {},
                ),
            ],
            e,
        )

    def _get_function_prototype(self, f: ast.FunctionDef, e: Env) -> FunctionPrototype:
        return FunctionPrototype(
            self.type_parser.parse(f.args.args[0].annotation, e, lineno=f.args.args[0].lineno),
            self.type_parser.parse(f.returns, e, lineno=f.returns.lineno if f.returns else 0),
        )

    @debug
    def compile_defun(self, f: ast.FunctionDef, e: Env) -> List[Instr]:
        e.sp += 1  # account for body push

        e.vars[f.name] = e.sp

        prototype = self._get_function_prototype(f, e)
        e.types[f.name] = prototype
        arg_type, return_type = prototype.arg_type, prototype.return_type

        # get init env keys
        init_var_names = set(e.vars.keys())

        # We work on an env copy to prevent from polluting the environment
        # with vars that we'd need to remove.
        func_env = e.copy()

        # store argument in env
        for arg_ast in f.args.args:
            func_env.sp += 1
            func_env.vars[arg_ast.arg] = func_env.sp
            func_env.types[arg_ast.arg] = prototype.arg_type

        body_instructions = self._compile_block(f.body, func_env)

        # freeing the argument
        body_instructions += self.free_var(f.args.args[0].arg, func_env)[0]

        comment = [Comment(f"Storing function {f.name} at {e.vars[f.name]}")]
        return comment + [
            Instr(
                "LAMBDA",
                [arg_type, return_type, body_instructions],
                {},
            ),
        ]

    @debug
    def compile_ccall(self, c: ast.Call, e: Env):
        """Call to class constructor"""

        # type check arguments
        for i, arg in enumerate(c.args):
            actual_type = self.type_checker.get_expression_type(arg, e)
            expected_type = e.types[c.func.id].attribute_types[i]

            # TODO solve callable vs fnuctionprototype casting
            if type(expected_type) == t.Callable:
                expected_type = FunctionPrototype(expected_type.param_type, expected_type.return_type)

            if type(actual_type) == type(expected_type) == t.Dict and actual_type.key_type == t.Unknown():
                pass
            elif actual_type != expected_type:
                raise E.FunctionParameterTypeException(c.func.id, expected_type, actual_type, c.args[0].lineno)

        instructions = RecordUtils.compile_record(e.types[c.func.id], c.args, self._compile, e)
        return instructions

    def _compile_dict_safe_get(self, key, default, e: Env) -> List[Instr]:
        key = self._compile(key, e)

        e.sp -= 1  # account for get

        if_not_env = e.copy()
        if_not_env.sp -= 1  # account for if none
        default = self._compile(default, if_not_env)
        return key + [
            Instr("GET", [], {}),
            Instr("IF_NONE", [default, []], {}),
        ]


    def _initialize_operations(self, e: Env) -> List[Instr]:
        instructions = []

        if "__OPERATIONS__" not in e.vars:
            instructions += [
                Instr("NIL", [t.Operation()], {})
            ]
            e.sp += 1  # account for pushing empty list
            e.vars["__OPERATIONS__"] = e.sp

        return instructions

    def _compile_cast_address_to_contract(self, f: ast.Call, e: Env) -> List[Instr]:
        instructions = []

        # create the contract
        for arg in f.args:
            instructions += self._compile(arg, e)

        # cast the address to contract
        instructions += [
            Instr("CONTRACT", [t.Unit()], {}),
            Instr("IF_NONE", [
                [
                    Instr("PUSH", [t.String(), "Contract does not exist"], {}),
                    Instr("FAILWITH", [], {})
                ],
                [],
            ], {}),
        ]

        return instructions


    def _compile_transaction(self, f: ast.Call, e: Env) -> List[Instr]:
        # fetch the operation list
        instructions = self._fetch_variable("__OPERATIONS__", e)

        # create the transaction
        for arg in f.args:
            instructions += self._compile(arg, e)

        # add the transaction to the list
        instructions += [
            Instr("TRANSFER_TOKENS", [], {}),
            Instr("CONS", [], {}),
        ]

        e.sp -= 2  # account for transfer_tokens
        e.sp -= 1  # account for cons


        # replace __OPERATIONS__
        operations_addr = e.vars["__OPERATIONS__"]
        free_old_ops_instructions, e = self.free_var("__OPERATIONS__", e)
        instructions += free_old_ops_instructions
        instructions += [
            Instr("DUG", [e.sp - operations_addr], {}),
        ]
        e.vars["__OPERATIONS__"] = operations_addr

        return instructions

    def _compile_mutez(self, f: ast.Call, e: Env) -> List[Instr]:
        return self.compile_constant(f.args[0], e, force_type=t.Mutez())

    def _compile_nat(self, f: ast.Call, e: Env) -> List[Instr]:
        return self.compile_constant(f.args[0], e, force_type=t.Nat())

    def _compile_int(self, f: ast.Call, e: Env) -> List[Instr]:
        return self.compile_constant(f.args[0], e, force_type=t.Int())

    def _compile_string(self, f: ast.Call, e: Env) -> List[Instr]:
        return self.compile_constant(f.args[0], e, force_type=t.String())

    def _compile_address(self, f: ast.Call, e: Env) -> List[Instr]:
        return self.compile_constant(f.args[0], e, force_type=t.Address())

    @debug
    def compile_fcall(self, f: ast.Call, e: Env):
        if type(f.func) == ast.Attribute:
            func_class = self.type_checker.get_expression_type(f.func.value, e)
            func_class_type = type(func_class)
            if func_class_type == StdLibClassSpec:
                arg_types = [self.type_checker.get_expression_type(arg, e) for arg in f.args]
                func_class_type = type(func_class.constructor.get_prototype(arg_types).return_type)
            if func_class_type in self.std_lib_types:
                std_lib_obj = self.std_lib_types[func_class_type]
                if f.func.attr in std_lib_obj.methods:
                    instructions = []
                    if f.func.attr not in std_lib_obj.static_methods:
                        instructions += self._compile(f.func.value, e)
                    instructions += std_lib_obj.methods[f.func.attr].compile_callback(*f.args, e)
                    return instructions

        if type(f.func) == ast.Subscript:
            function_name = f.func.value.id
        else:
            function_name = f.func.id

        if function_name in self.std_lib:
            std_lib_function = self.std_lib[function_name]
            if type(std_lib_function) == StdlibFunctionSpec:
                return std_lib_function.compile_callback(f, e)
            elif type(std_lib_function) == StdLibClassSpec:
                if type(f.func) == ast.Subscript:
                    cast_type = self.type_checker.get_expression_type(f.func, e)
                    self.current_type = cast_type
                return std_lib_function.constructor.compile_callback(f, e)
            else:
                raise E.CompilerException(f"Stdlib expression {node.func.id} cannot be typed", node.lineno)

        # if dealing with a record instantiation, compile as such
        if function_name in e.types.keys() and type(e.types[function_name]) is t.Record:
            return self.compile_ccall(f, e)

        # typecheck argtype
        actual_type = self.type_checker.get_expression_type(f.args[0], e)
        if type(e.types[f.func.id]) == FunctionPrototype:
            expected_type = e.types[f.func.id].arg_type
        else:
            expected_type = e.types[f.func.id].param_type
        if actual_type != expected_type:
            raise E.FunctionParameterTypeException(f.func.id, expected_type, actual_type, f.args[0].lineno)

        func_addr = e.vars[function_name]
        jump_length = e.sp - func_addr
        comment = [
            Comment(f"Moving to function {function_name} at {func_addr}, e.sp = {e.sp}")
        ]

        load_function = [
            Instr("DIG", [jump_length], {}),
            Instr("DUP", [], {}),
            Instr("DUG", [jump_length + 1], {}),
        ]

        e.sp += 1  # Account for DUP

        # fetch arg name for function
        load_arg = self._compile(f.args[0], e)

        e.sp += 1  # Account for pushing argument

        execute_function = [Instr("EXEC", [], {})]

        e.sp -= 2  # Account popping EXEC and LAMBDA

        instr = comment + load_function + load_arg + execute_function


        return instr

    @debug
    def compile_return(self, r: ast.FunctionDef, e: Env):
        return self._compile(r.value, e)

    def get_init_env(self):
        return Env({}, -1, {}, {})

    @debug
    def compile_entrypoint(self, f: ast.FunctionDef, e: Env, prologue_instructions: List[Instr]) -> List[Instr]:
        e = e.copy()
        # we update the variable pointers to account for the fact that the first
        # element on the stack is Pair(param, storage).
        # we are targetting a stack that will look like [storage, {prologue_instructions}, param]
        # hence, we need to add 1 to all the addresses of the variables in `prologue_instructions`
        e.vars = {var_name: address + 1 for var_name, address in e.vars.items()}

        e.sp += 1  # account for pushing Pair(param, storage)
        e.sp += 1  # account for breaking up Pair(param, storage)

        # Save the storage and entrypoint argument on the stack
        self.contract.instructions = [
            Instr("UNPAIR", [], {}), # [storage, param]
        ] + prologue_instructions + [
            Instr("DIG", [e.sp - 1], {}),  # fetch the entrypoint argument
        ]

        # the storage is at the bottom of the stack
        e.vars["__STORAGE__"] = 0

        # the parameter is a the top of the stack
        # N.B. all variables declared in the prologue instructions) are
        #      laying between the storage and the parameter (hence the +1 above)
        e.vars[f.args.args[0].arg] = e.sp


        init_operations_instructions = self._initialize_operations(e)

        # type argument if record

        e.types[f.args.args[0].arg] = self.type_parser.parse(f.args.args[0].annotation, e, lineno=f.args.args[0].lineno)

        block_instructions, operations_addr = self._compile_block(f.body, e, return_operations=True)
        if operations_addr:
            e.vars["__OPERATIONS__"] = operations_addr

        entrypoint_instructions = block_instructions

        if "__OPERATIONS__" in e.vars:
            get_operations = self._fetch_variable("__OPERATIONS__", e)
            pass
        else:
            get_operations = [Instr("NIL", [t.Operation()], {})]
            e.sp += 1

        epilogue = get_operations + [
            Instr("PAIR", [], {}),
        ]
        e.sp -= 1

        free_vars_instructions = self.free_vars(list(e.vars.keys()), e)

        entrypoint_instructions = init_operations_instructions + entrypoint_instructions + epilogue + free_vars_instructions

        prototype = self._get_function_prototype(f, e)
        entrypoint = Entrypoint(prototype, entrypoint_instructions)
        self.contract.add_entrypoint(f.name, entrypoint)
        return []

    def free_vars(self, var_names: List[str], e: Env) -> List[Instr]:
        # Free from the top of the stack. this ensures that the variable pointers
        # are not changed as variables are freed from the stack
        sorted_keys = sorted(var_names, key=lambda var_name: e.vars[var_name], reverse=True)

        # remove env vars from memory
        free_var_instructions = []
        for var_name in sorted_keys:
            instr, _ = self.free_var(var_name, e)
            free_var_instructions += instr

        return free_var_instructions

    def _compile_block(self, block_ast: List[ast.AST], block_env: Env, return_operations = False) -> Union[List[Instr], Tuple[List[Instr], Union[bool, int]]]:
        """frees newly declared variables at the end of the block, hence °e°
        should be the same befor and after the block"""
        # get init env keys
        init_var_names = set(block_env.vars.keys())
        if return_operations:
            init_var_names.add("__OPERATIONS__")

        # iterate body instructions
        block_instructions = []
        for i in block_ast:
            block_instructions += self._compile(i, block_env)

        # get new func_env keys
        new_var_names = set(block_env.vars.keys())

        # intersect init and new env keys
        intersection = list(new_var_names - init_var_names)

        free_var_instructions = self.free_vars(intersection, block_env)

        instructions = block_instructions + free_var_instructions
        if return_operations:
            return instructions, block_env.vars.get("__OPERATIONS__", None)

        return instructions

    @debug
    def compile_storage(self, storage_ast, e: Env):
        e.types["__STORAGE__"] = self.type_checker.get_expression_type(storage_ast, e)
        self.contract.storage_type = self.type_checker.get_expression_type(storage_ast, e)

    @debug
    def _compile_contract(self, contract_ast: ast.ClassDef, e: Env, prologue_instructions: List[Instr]) -> List[Instr]:
        instructions = []
        for entrypoint in contract_ast.body:

            if entrypoint.name == "deploy":
                if type(entrypoint.body[0]) == ast.Return:
                    self.compile_storage(entrypoint.body[0].value, e)
                else:
                    raise CompilerException("The deploy function can only have a single return statement indicating the storage type.")
            else:
                instructions += self.compile_entrypoint(entrypoint, e, prologue_instructions)
        return instructions

    @debug
    def compile_record(self, record_ast: ast.ClassDef, e: Env) -> List[Instr]:
        attribute_names = [attr.target.id for attr in record_ast.body]
        attribute_types = []
        attribute_annotations = []
        for attr_name, attr in zip(attribute_names, record_ast.body):
            attribute_annotations.append(attr.annotation)
            attribute_types.append(self.type_parser.parse(attr.annotation, e, "%" + attr_name, lineno=attr.lineno))

        e.types[record_ast.name] = t.Record(record_ast.name, attribute_names, attribute_types)
        return []

    def handle_get_storage(self, storage_get_ast: ast.Attribute, e: Env) -> List[Instr]:
        return self.compile_name(ast.Name(id='__STORAGE__', ctx=ast.Load()), e)

    def check_get_storage(self, storage_get_ast: ast.Attribute) -> bool:
        # tmp fix
        if type(storage_get_ast.value) == ast.Subscript:
            return False

        try:
            return (
                storage_get_ast.value.value.id == "self"
                and storage_get_ast.value.attr == "storage"
            )
        except:
            return (
                storage_get_ast.value.id == "self"
                and storage_get_ast.attr == "storage"
            )

    def check_get_sender(self, sender_ast: ast.Attribute) -> bool:
        return (
            sender_ast.value.id == "self"
            and sender_ast.attr == "sender"
        )

    def get_sender(self, sender_ast: ast.Name, e: Env) -> List[Instr]:
        e.sp += 1  # account for pushing sender
        return [Instr("SENDER", [], {})]

    def get_source(self, sender_ast: ast.Name, e: Env) -> List[Instr]:
        e.sp += 1  # account for pushing source
        return [Instr("SOURCE", [], {})]

    def get_amount(self, amount_ast: ast.Name, e: Env) -> List[Instr]:
        e.sp += 1  # account for pushing amount
        return [Instr("AMOUNT", [], {})]

    def _compile_attribute(self, node, e: Env) -> List[Instr]:
        instructions = []

        record_type = self.type_checker.get_expression_type(node.value, e)
        instructions += self._compile(node.value, e)
        instructions += RecordUtils.navigate_to_tree_leaf(record_type, node.attr, node.lineno)

        return instructions

    @debug
    def compile_attribute(self, attribute_ast: ast.Attribute, e: Env) -> List[Instr]:
        if self.check_get_storage(attribute_ast):
            return self.handle_get_storage(attribute_ast, e)

        return self._compile_attribute(attribute_ast, e)

    @debug
    def compile_compare(self, compare_ast: ast.Compare, e: Env) -> List[Instr]:
        compare_instructions = (
            self._compile(compare_ast.comparators[0], e)
            + self._compile(compare_ast.left, e)
            + [Instr("COMPARE", [], {})]
        )
        # Account for COMPARE
        e.sp -= 1

        operator_type = type(compare_ast.ops[0])
        if operator_type == ast.Eq:
            operator_instructions = [Instr("EQ", [], {})]
        elif operator_type == ast.NotEq:
            operator_instructions = [Instr("NEQ", [], {})]
        elif operator_type == ast.Lt:
            operator_instructions = [Instr("LT", [], {})]
        elif operator_type == ast.Gt:
            operator_instructions = [Instr("GT", [], {})]
        elif operator_type == ast.LtE:
            operator_instructions = [Instr("LE", [], {})]
        elif operator_type == ast.GtE:
            operator_instructions = [Instr("GE", [], {})]
        elif operator_type == ast.In:
            # remove COMPARE instruction
            del compare_instructions[-1]
            operator_instructions = [Instr("MEM", [], {})]
        else:
            raise E.CompilerException(f"Comparison operator {compare_ast} not yet supported", compare_ast.lineno)

        return compare_instructions + operator_instructions

    def compile_if(self, if_ast: ast.If, e: Env) -> List[Instr]:
        test_instructions = self._compile(if_ast.test, e)

        # Account for "IF" poping the boolean sitting at the top of the stack
        e.sp -= 1

        if_true_instructions = self._compile_block(if_ast.body, e.copy())
        if_false_instructions = self._compile_block(if_ast.orelse, e.copy())
        if_instructions = [Instr("IF", [if_true_instructions, if_false_instructions], {})]
        return test_instructions + if_instructions

    def compile_raise(self, raise_ast: ast.Raise, e: Env) -> List[Instr]:
        try:
            raise_ast.exc.args[0]
        except:
            breakpoint()
            pass
        return self._compile(raise_ast.exc.args[0], e) + [Instr("FAILWITH", [], {})]

    def _compile_get_subscript(self, e: Env) -> List[Instr]:
        e.sp -= 1  # account for get
        return [
            Instr("GET", [], {}),
            Instr("IF_NONE", [
                [
                    Instr("PUSH", [t.String(), "Key does not exist"], {}),
                    Instr("FAILWITH", [], {})
                ],
                [],
            ], {}),
        ]

    def compile_subscript(self, subscript: ast.Subscript, e: Env) -> List[Instr]:
        dictionary = self._compile(subscript.value, e)
        key = self._compile(subscript.slice, e)
        get_instructions = self._compile_get_subscript(e)
        return dictionary + key + get_instructions

    def compile_unary_op(self, node: ast.UnaryOp, e: Env) -> List[Instr]:
        return self._compile(node.operand, e) + [Instr("NOT", [], {})]

    def compile_for(self, node: ast.For, e: Env) -> List[Instr]:
        instructions = []

        instructions += self._compile(node.iter, e)

        # account for iterated element
        iterated_element_name = node.target.id

        # sp does not change as the list is just replaced with the elements
        e.sp += 0
        e.vars[iterated_element_name] = e.sp
        # type iterated element
        iterable_type = self.type_checker.get_expression_type(node.iter, e)
        if type(iterable_type) == t.List:
            e.types[iterated_element_name] = iterable_type.element_type
        elif type(iterable_type) == t.Dict:
            raise E.CompilerException("Dictionary iteration not yet supported", node.iter.lineno)
        else:
            raise E.NotAnIterableException(iterable_type.python_name())

        # compile for block
        iter_instructions = self._compile_block(node.body, e.copy())

        # freeing i at block end
        iter_instructions += self.free_var(iterated_element_name, e)[0]
        #e.sp -= 1
        #del e.vars[iterated_element_name]

        # compile iter
        instructions += [Instr("ITER", [iter_instructions], {})]

        return instructions

    def compile(self):
        return self._compile(self.ast)

    def compile_new(self):
        e = self.get_init_env()
        e.sp = 1  # account for storage and entrypoint arg
        self.contract.instructions = self._compile(self.ast, e)
        print("e.sp = ", e.sp, self.env.sp)
        self._compile(self.ast, self.env)
        return self.contract

    def _compile(self, node_ast, e: Optional[Env] = None, instructions = None, current_type: Optional[t.Type] = None) -> List[Instr]:
        e = self.get_init_env() if not e else e
        self.env = e  # saving as attribute for debug purposes

        self.current_type = current_type

        if not instructions:
            instructions = []

        if type(node_ast) == ast.Module:
            instructions += self.compile_module(node_ast, e)
            if self.isDebug:
                self.print_instructions(instructions)
        elif type(node_ast) == ast.Assign:
            instructions += self.compile_assign(node_ast, e)
        elif type(node_ast) == ast.AnnAssign:
            instructions += self.compile_ann_assign(node_ast, e)
        elif type(node_ast) == ast.Attribute:
            instructions += self.compile_attribute(node_ast, e)
        elif type(node_ast) == ast.Expr:
            instructions += self.compile_expr(node_ast, e)
        elif type(node_ast) == ast.If:
            instructions += self.compile_if(node_ast, e)
        elif type(node_ast) == ast.Constant:
            instructions += self.compile_constant(node_ast, e)
        elif type(node_ast) == ast.Compare:
            instructions += self.compile_compare(node_ast, e)
        elif type(node_ast) == ast.Name:
            instructions += self.compile_name(node_ast, e)
        elif type(node_ast) == ast.BinOp:
            instructions += self.compile_binop(node_ast, e)
        elif type(node_ast) == ast.FloorDiv:
            instructions += self.compile_floor_div(node_ast, e)
        elif type(node_ast) == ast.Mod:
            instructions += self.compile_modulo(node_ast, e)
        elif type(node_ast) == ast.Add:
            instructions += self.compile_add(node_ast, e)
        elif type(node_ast) == ast.Mult:
            instructions += self.compile_mult(node_ast, e)
        elif type(node_ast) == ast.Sub:
            instructions += self.compile_sub(node_ast, e)
        elif type(node_ast) == ast.List:
            instructions += self.compile_list(node_ast, e)
        elif type(node_ast) == ast.FunctionDef:
            instructions += self.compile_defun(node_ast, e)
        elif type(node_ast) == ast.Return:
            instructions += self.compile_return(node_ast, e)
        elif type(node_ast) == ast.Raise:
            instructions += self.compile_raise(node_ast, e)
        elif type(node_ast) == ast.Call:
            instructions += self.compile_fcall(node_ast, e)
        elif type(node_ast) == ast.ClassDef:
            if node_ast.name == "Contract":
                instructions += self._compile_contract(node_ast, e, instructions)
            elif len(node_ast.bases) and node_ast.bases[0].id == "Contract":
                instructions += self._compile_contract(node_ast, e, instructions)
            elif "dataclass" in [decorator.id if type(decorator) == ast.Name else decorator.func.id for decorator in node_ast.decorator_list]:
                instructions += self.compile_record(node_ast, e)
            else:
                raise E.CompilerException("Classes can only be called 'Contract' or be 'dataclasses'", node_ast.lineno)
        elif type(node_ast) == ast.Dict:
            instructions += self.compile_dict(node_ast, e, current_type)
        elif type(node_ast) == ast.Subscript:
            instructions += self.compile_subscript(node_ast, e)
        elif type(node_ast) == ast.UnaryOp:
            instructions += self.compile_unary_op(node_ast, e)
        elif type(node_ast) == ast.ImportFrom:
            # Skip for now
            pass
        elif type(node_ast) == ast.BoolOp:
            instructions += self.compile_bool_op(node_ast, e)
            pass
        elif type(node_ast) == ast.For:
            instructions += self.compile_for(node_ast, e)
        else:
            raise E.CompilerException("f{node_ast} not supported by the compiler yet", node_ast.lineno)

        if self.isDebug:
            print(e)

        return instructions

    def compile_bool_op(self, node: ast.BoolOp, e: Env) -> List[Instr]:
        # AND / x : y : S  =>  (x & y) : S
        # y is pushed first
        y = self._compile(node.values[1], e)
        x = self._compile(node.values[0], e)
        operand_instr = None
        if type(node.op) == ast.And:
            operand_instr = Instr("AND", [], {})
        elif type(node.op) == ast.Or:
            operand_instr = Instr("OR", [], {})
        else:
            raise E.CompilerException("Only 'and' and 'or' boolean operations are supported at the moment", node.lineno)
        e.sp -= 1  # account for bool_op
        return y + x + [operand_instr]

    def compile_expression(self, e: Env = None):
        self.ast = macro_expander(self.ast, self.std_lib)
        instructions = self._compile(self.ast, e)
        return CompilerBackend().compile_instructions(instructions)

    def compile_contract(self):
        self.ast = macro_expander(self.ast, self.std_lib)
        self.compile()
        return CompilerBackend().compile_contract(self.contract)

    @staticmethod
    def print_instructions(instructions):
        print("\n".join([f"{i.name} {i.args} {i.kwargs}" for i in instructions]))


class VM:
    def __init__(self, sender ="tz3M4KAnKF2dCSjqfa1LdweNxBGQRqzvPL88"):
        self.reset_stack()
        self.context = ExecutionContext()
        self.set_sender(sender)

    def execute(self, micheline):
        self.result = InterpreterResult(stdout=[])
        code_section = CodeSection.match(micheline)
        code_section.args[0].execute(self.stack, self.result.stdout, self.context)
        return self

    def load_contract(self, micheline):
        self.contract = ContractInterface.from_micheline(micheline)
        return self

    def reset_stack(self):
        self.stack = MichelsonStack()
        return self

    def set_sender(self, sender):
        self.context.sender = sender
        return self

    def stdout(self):
        print("\n".join(self.result.stdout))
        return self

