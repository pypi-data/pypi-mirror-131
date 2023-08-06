from pymich.michelson_types import *

SENDER = Address("tz1")
SOURCE = Address("tz1")
AMOUNT = Mutez(0)
BALANCE = Mutez(0)

def transaction(contract: Contract, amount: Mutez, type: Type[ParameterType]) -> Operation:
    return Operation()

def len(
    data: Union[
        BigMap[KeyType, ValueType],
        Map[KeyType, ValueType],
        Set[ValueType],
        List[ValueType],
        String,
        Bytes,
    ]
) -> Nat:
    return data.__nat_len__()
