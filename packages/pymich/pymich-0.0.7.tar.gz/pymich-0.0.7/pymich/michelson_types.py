from __future__ import annotations

from time import time

from copy import deepcopy
from typing import Dict, Generic, Iterator
from typing import Optional, List as PythonList
from typing import Set as PythonSet
from typing import Tuple, TypeVar, Union, overload
from dataclasses import dataclass
from typing import no_type_check, Any
from typing import cast, Type



class MichelsonType:
    pass


ParameterType = TypeVar('ParameterType', bound=Union[MichelsonType, bool])
KeyType = TypeVar('KeyType', bound=Union[MichelsonType, bool])
ValueType = TypeVar('ValueType', bound=Union[MichelsonType, bool])

python_len = len


class Unit(MichelsonType):
    def __init__(self) -> None:
        pass


class Int(MichelsonType):
    def __init__(self, value: int):
        self.value = value

    def __neg__(self) -> Int:
        return Int(-self.value)

    @overload
    def __add__(self, other: Nat) -> Int: ...

    @overload
    def __add__(self, other: Int) -> Int: ...

    @overload
    def __add__(self, other: Timestamp) -> Timestamp: ...

    def __add__(self, other: Union[Nat, Int, Timestamp]) -> Union[Int, Timestamp]:
        if isinstance(other, (Nat, Int)):
            return Int(self.value + other.value)

        return Timestamp(self.value + other.timestamp)

    def __sub__(self, other: Union[Nat, Int]) -> Int:
        return Int(self.value - other.value)

    def __mul__(self, other: Union[Nat, Int]) -> Int:
        return Int(self.value * other.value)

    def __floordiv__(self, other: Union[Nat, Int]) -> Int:
        return Int(self.value // other.value)

    def __mod__(self, other: Union[Nat, Int]) -> Int:
        return Int(self.value % other.value)

    def __copy__(self) -> Int:
        return Int(self.value)

    def __lt__(self, other: Int) -> bool:
        return self.value < other.value

    def __le__(self, other: Int) -> bool:
        return self.value <= other.value

    def __eq__(self, other: Int) -> bool:  # type: ignore
        return self.value == other.value

    def __gt__(self, other: Int) -> bool:
        return self.value > other.value

    def __ge__(self, other: Int) -> bool:
        return self.value >= other.value

    def is_nat(self) -> Optional[Nat]:
        if self.value >= 0:
            return Nat(self.value)

        return None

    def __abs__(self) -> Nat:
        return Nat(abs(self.value))

    def __str__(self) -> str:
        return self.value.__str__()

    def __hash__(self) -> int:
        return hash(self.value)


class Nat(MichelsonType):
    def __init__(self, value: int):
        self.value = value

    @overload
    def __add__(self, other: Nat) -> Nat: ...

    @overload
    def __add__(self, other: Int) -> Int: ...

    def __add__(self, other: Union[Nat, Int]) -> Union[Nat, Int]:
        if isinstance(other, Int):
            return Int(self.value + other.value)

        return Nat(self.value + other.value)

    def __sub__(self, other: Union[Nat, Int]) -> Int:
        return Int(self.value - other.value)

    @overload
    def __mul__(self, other: Nat) -> Nat: ...

    @overload
    def __mul__(self, other: Int) -> Int: ...

    def __mul__(self, other: Union[Nat, Int]) -> Union[Nat, Int]:
        if isinstance(other, Int):
            return Int(self.value * other.value)

        return Nat(self.value * other.value)

    @overload
    def __floordiv__(self, other: Nat) -> Nat: ...

    @overload
    def __floordiv__(self, other: Int) -> Int: ...

    def __floordiv__(self, other: Union[Nat, Int]) -> Union[Nat, Int]:
        if isinstance(other, Int):
            return Int(self.value // other.value)

        return Nat(self.value // other.value)

    @overload
    def __mod__(self, other: Nat) -> Nat: ...

    @overload
    def __mod__(self, other: Int) -> Int: ...

    def __mod__(self, other: Union[Nat, Int]) -> Union[Nat, Int]:
        if isinstance(other, Int):
            return Int(self.value % other.value)

        return Nat(self.value % other.value)

    def __neg__(self) -> Int:
        return Int(-self.value)

    def __copy__(self) -> Nat:
        return Nat(self.value)

    def __bool__(self) -> bool:
        return self.value != 0

    def __lt__(self, other: Nat) -> bool:
        return self.value < other.value

    def __le__(self, other: Nat) -> bool:
        return self.value <= other.value

    def __eq__(self, other: Nat) -> bool:  # type: ignore
        return self.value == other.value

    def __gt__(self, other: Nat) -> bool:
        return self.value > other.value

    def __ge__(self, other: Nat) -> bool:
        return self.value >= other.value

    def to_int(self) -> Int:
        return Int(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value.__str__()


class String(MichelsonType):
    def __init__(self, value: str):
        self.value = value

    def __add__(self, other: String) -> String:
        """String concatenation"""
        return String(self.value + other.value)

    def __nat_len__(self) -> Nat:
        return Nat(python_len(self.value))

    def __lt__(self, other: String) -> bool:
        return self.value < other.value

    def __le__(self, other: String) -> bool:
        return self.value <= other.value

    def __eq__(self, other: String) -> bool:  # type: ignore
        return self.value == other.value

    def __gt__(self, other: String) -> bool:
        return self.value > other.value

    def __ge__(self, other: String) -> bool:
        return self.value >= other.value

    def __getslice__(self, i: int, j: int) -> String:
        return String(self.value[i:j])

    def __copy__(self) -> String:
        return String(self.value)

    def __repr__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value.__str__()


class Address(MichelsonType):
    def __init__(self, address: str):
        self.address = address

    def __copy__(self) -> Address:
        return Address(self.address)

    def __str__(self) -> str:
        return self.address.__str__()

    def __hash__(self) -> int:
        return hash(self.address)

    def __eq__(self, other: Address) -> bool:  # type: ignore
        return self.address == other.address

class Bytes(MichelsonType):
    def __init__(self, value: MichelsonType):
        self.value = deepcopy(value)

    def unpack(self, _: Type[ParameterType]) -> ParameterType:
        return cast(ParameterType, self.value)

    def blake2b(self) -> NotImplementedError:
        return NotImplementedError()

    def kekkac(self) -> NotImplementedError:
        return NotImplementedError()

    def sha256(self) -> NotImplementedError:
        return NotImplementedError()

    def sha512(self) -> NotImplementedError:
        return NotImplementedError()

    def sha3(self) -> NotImplementedError:
        return NotImplementedError()

    def __copy__(self) -> Bytes:
        return Bytes(self.value)

    def __nat_len__(self) -> Nat:
        return Nat(0)

    def concat(self) -> NotImplementedError:
        return NotImplementedError()

    def __getslice__(self, i: int, j: int) -> NotImplementedError:
        return NotImplementedError()

    def __lt__(self, other: Bytes) -> NotImplementedError:
        return NotImplementedError()

    def __le__(self, other: Bytes) -> NotImplementedError:
        return NotImplementedError()

    def __eq__(self, other: Bytes) -> bool:  # type: ignore
        return self.value == other.value

    def __gt__(self, other: Bytes) -> NotImplementedError:
        return NotImplementedError()

    def __ge__(self, other: Bytes) -> NotImplementedError:
        return NotImplementedError()


class Mutez(MichelsonType):
    def __init__(self, amount: int):
        self.amount = amount

    def __add__(self, other: Mutez) -> Mutez:
        return Mutez(self.amount + other.amount)

    def __sub__(self, other: Mutez) -> Mutez:
        return Mutez(self.amount - other.amount)

    def __mul__(self, other: Nat) -> Mutez:
        return Mutez(self.amount * other.value)

    @overload
    def __floordiv__(self, other: Mutez) -> Mutez: ...

    @overload
    def __floordiv__(self, other: Nat) -> Nat: ...

    def __floordiv__(self, other: Union[Mutez, Nat]) -> Union[Mutez, Nat]:
        if isinstance(other, Nat):
            return Nat(self.amount // other.value)

        return Mutez(self.amount // other.amount)

    def __mod__(self, other: Union[Mutez, Nat]) -> Mutez:
        if isinstance(other, Nat):
            return Mutez(self.amount % other.value)

        return Mutez(self.amount % other.amount)

    def __lt__(self, other: Mutez) -> bool:
        return self.amount < other.amount

    def __le__(self, other: Mutez) -> bool:
        return self.amount <= other.amount

    def __eq__(self, other: Mutez) -> bool:  # type: ignore
        return self.amount == other.amount

    def __gt__(self, other: Mutez) -> bool:
        return self.amount > other.amount

    def __ge__(self, other: Mutez) -> bool:
        return self.amount >= other.amount

    def __str__(self) -> str:
        return self.amount.__str__() + "mutez"

    def __hash__(self) -> int:
        return hash(self.amount)


class Timestamp(MichelsonType):
    def __init__(self, timestamp: int):
        self.timestamp = timestamp

    @staticmethod
    def now() -> Timestamp:
        return Timestamp(int(time()))

    def __add__(self, delta: Int) -> Timestamp:
        return Timestamp(self.timestamp + delta.value)

    @overload
    def __sub__(self, other: Timestamp) -> Int: ...

    @overload
    def __sub__(self, other: Int) -> Timestamp: ...

    def __sub__(self, other: Union[Timestamp, Int]) -> Union[Timestamp, Int]:
        if isinstance(other, Int):
            return Timestamp(self.timestamp - other.value)

        return Timestamp(self.timestamp - other.timestamp)

    def __lt__(self, other: Timestamp) -> bool:
        return self.timestamp < other.timestamp

    def __le__(self, other: Timestamp) -> bool:
        return self.timestamp <= other.timestamp

    def __eq__(self, other: Timestamp) -> bool:  # type: ignore
        return self.timestamp == other.timestamp

    def __gt__(self, other: Timestamp) -> bool:
        return self.timestamp > other.timestamp

    def __ge__(self, other: Timestamp) -> bool:
        return self.timestamp >= other.timestamp

    def __str__(self) -> str:
        return self.timestamp.__str__()

    def __hash__(self) -> int:
        return hash(self.timestamp)


class Set(MichelsonType, Generic[ParameterType]):
    """Michelson set abstraction. It differs with a regular Python
    set in that when instanciating or adding an element to a set,
    a copy of that element is added rather than the element itself."""
    def __init__(self, *args: ParameterType):
        self.__values: PythonSet[ParameterType] = set()
        for arg in args:
            self.__values.add(deepcopy(arg))

    def __contains__(self, value: ParameterType) -> bool:
        return value in self.__values

    def add(self, element: ParameterType) -> None:
        """Adds a COPY of the value"""
        el_copy = deepcopy(element)
        self.__values.add(el_copy)

    def remove(self, element: ParameterType) -> None:
        """Removes an element from the set"""
        self.remove(element)

    def __nat_len__(self) -> Nat:
        return Nat(python_len(self.__values))

    def __iter__(self) -> Iterator[ParameterType]:
        return iter(self.__values)

    def __copy__(self) -> Set[ParameterType]:
        return Set(*self.__values)

    def __str__(self) -> str:
        return self.__values.__str__()

    def __hash__(self) -> int:
        return hash((i for i in self.__values))


class List(MichelsonType, Generic[ParameterType]):
    def __init__(self, *elements: ParameterType):
        self.__list: PythonList[ParameterType] = []
        for element in elements:
            self.__list.append(deepcopy(element))

    def __copy__(self) -> List[ParameterType]:
        return List(*self.__list)

    def prepend(self, element: ParameterType) -> List[ParameterType]:
        return List(deepcopy(element), *self.__list)

    def __nat_len__(self) -> Nat:
        return Nat(python_len(self.__list))

    def __iter__(self) -> Iterator[ParameterType]:
        return iter(self.__list)

    def __str__(self) -> str:
        return self.__list.__str__()

    def __hash__(self) -> int:
        return hash((i for i in self.__list))


class BigMap(MichelsonType, Generic[KeyType, ValueType]):
    """Michelson big map abstraction. It differs with a regular Python
    dictionary in that it:
    - is instanciated from literals by deepcopying the literal key/values
    - adding an element will add a copy of that element
    - getting an element will return a copy of that element
    - it is not iterable
    """

    def __init__(self) -> None:
        self.__dictionary: Dict[KeyType, ValueType] = {}
        pass
        #self.__dictionary: Dict[KeyType, ValueType] = {}
        #for key, value in dictionary.items():
        #    self.__dictionary[deepcopy(key)] = deepcopy(value)

    def __getitem__(self, key: KeyType) -> ValueType:
        return deepcopy(self.__dictionary[key])

    def __delitem__(self, key: KeyType) -> None:
        del self.__dictionary[key]

    def get(self, key: KeyType, default: ValueType) -> ValueType:
        """Returns a copy of the value"""
        if key in self.__dictionary:
            return self.__getitem__(key)

        return default

    def __contains__(self, key: KeyType) -> bool:
        return key in self.__dictionary

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        """Store a COPY of the value"""
        self.__dictionary[key] = deepcopy(value)

    def add(self, key: KeyType, value: ValueType) -> BigMap[KeyType, ValueType]:
        """Returns a COPY of self with a COPY of the value added"""
        new_map = deepcopy(self)
        new_map[key] = value
        return new_map

    def remove(self, key: KeyType) -> BigMap[KeyType, ValueType]:
        """Returns a COPY of the value"""
        new_map = deepcopy(self)
        del new_map[key]
        return new_map

    def __nat_len__(self) -> Nat:
        return Nat(python_len(self.__dictionary))

    def __copy__(self) -> BigMap[KeyType, ValueType]:
        new_map = BigMap[KeyType, ValueType]()
        for k, v in self.__dictionary.items():
            new_map[k] = v
        return new_map

    def __str__(self) -> str:
        return self.__dictionary.__str__()

class Map(MichelsonType, Generic[KeyType, ValueType]):
    """Michelson big map abstraction. It differs with a regular Python
    dictionary in that it:
    - is instanciated from literals by deepcopying the literal key/values
    - adding an element will add a copy of that element
    - getting an element will return a copy of that element
    """

    def __init__(self) -> None:
        self.__dictionary: Dict[KeyType, ValueType] = {}
        pass
        #self.__dictionary: Dict[KeyType, ValueType] = {}
        #for key, value in dictionary.items():
        #    self.__dictionary[deepcopy(key)] = deepcopy(value)

    def __getitem__(self, key: KeyType) -> ValueType:
        return deepcopy(self.__dictionary[key])

    def __delitem__(self, key: KeyType) -> None:
        del self.__dictionary[key]

    def get(self, key: KeyType, default: ValueType) -> ValueType:
        """Returns a copy of the value"""
        if key in self.__dictionary:
            return self.__getitem__(key)

        return default

    def __contains__(self, key: KeyType) -> bool:
        return key in self.__dictionary

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        """Store a COPY of the value"""
        self.__dictionary[key] = deepcopy(value)

    def add(self, key: KeyType, value: ValueType) -> Map[KeyType, ValueType]:
        """Returns a COPY of self with a COPY of the value added"""
        new_map = deepcopy(self)
        new_map[key] = value
        return new_map

    def remove(self, key: KeyType) -> Map[KeyType, ValueType]:
        """Returns a COPY of the value"""
        new_map = deepcopy(self)
        del new_map[key]
        return new_map

    def __iter__(self) -> Iterator[Tuple[KeyType, ValueType]]:
        return iter(self.__dictionary.items())

    def __nat_len__(self) -> Nat:
        return Nat(python_len(self.__dictionary))

    def __copy__(self) -> Map[KeyType, ValueType]:
        new_map = Map[KeyType, ValueType]()
        for k, v in self.__dictionary.items():
            new_map[k] = v
        return new_map

    def __str__(self) -> str:
        return self.__dictionary.__str__()

    def __hash__(self) -> int:
        return hash(self.__dictionary)


class Record(MichelsonType):
    @no_type_check
    def __getattr__(self, __name: str) -> Any:
        return deepcopy(object.__getattribute__(self, __name))

    @no_type_check
    def __setattr__(self, __name: str, value: MichelsonType) -> None:
        object.__setattr__(self, __name, deepcopy(value))


class Contract(MichelsonType):
    def __init__(self, address: Address) -> None:
        self._address = address


class Operation(MichelsonType):
    def __init__(self) -> None:
        pass
