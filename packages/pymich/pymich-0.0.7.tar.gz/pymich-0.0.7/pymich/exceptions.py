class CompilerException(Exception):
    """Raised when the compiler fails

    Attributes:
        message -- error message
    """

    def __init__(self, message, lineno):
        self.message = message + f" at line {lineno}"

class NotAnIterableException(CompilerException):
    def __init__(self, actual_type):
        self.message = f"{actual_type} is not an iterable"

class MalformedAnnotationException(CompilerException):
    def __init__(self, message):
        self.message = message

class TypeException(CompilerException):
    def __init__(self, expected_type, actual_type, lineno):
        self.message = f"Unexpected type: expected {expected_type}, got {actual_type} at line {lineno}"

class AttributeException(TypeException):
    def __init__(self, record_type, attribute_name, lineno):
        self.message = f"{record_type} Record has no attribute {attribute_name} at line {lineno}"

class NameException(TypeException):
    def __init__(self, token_name, lineno):
        self.message = f"Variable '{token_name}' does not exist at line {lineno}"

class FunctionNameException(TypeException):
    def __init__(self, function_name, lineno):
        self.message = f"Function '{function_name}' does not exist at line {lineno}"

class FunctionParameterTypeException(TypeException):
    def __init__(self, function_name, expected_type, actual_type, lineno):
        self.message = f"Function '{function_name}' expected a parameter of type {expected_type} but got {actual_type} at line {lineno}"

class TypeAnnotationDoesNotExistException(TypeException):
    def __init__(self, annotation_name, expected_type_annotations, lineno):
        self.message = f"Type annotation '{annotation_name}' does not exist, expected {expected_type_annotations} at line {lineno}"

