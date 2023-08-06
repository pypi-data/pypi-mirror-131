import cli2
import json
import sys

from pymich.exceptions import CompilerException

from enum import Enum
from pymich.compiler import Compiler, VM


MICHELSON = "michelson"
MICHELINE = "micheline"


def compile(input_path: str, output_path: str, output_format: str = MICHELINE):
    """
    Compiles a Python file to Micheline.

    :param input_path: path to the Python file to compile
    :param output_path: path of file to write micheline to
    :param output_format: output format for the contract, one of "michelson" or "micheline"
    """
    with open(input_path) as f:
        source = f.read()

    try:
        micheline = Compiler(source).compile_contract()

        if output_format == MICHELINE:
            with open(output_path, 'w') as f:
                f.write(json.dumps(micheline))
        elif output_format == MICHELSON:
            vm = VM()
            vm.load_contract(micheline)
            with open(output_path, 'w') as f:
                f.write(vm.contract.to_michelson())
        else:
            print(f"Only 'michelson' and 'micheline' parameters are supported", file=sys.stderr)
    except CompilerException as e:
        print(e.message, file=sys.stderr)


cli = cli2.Command(compile)

if __name__ == '__main__':
    cli.entry_point()
