class BaseCompilerException(Exception):
    pass


class ValidationException(Exception):
    def __init__(self, base, target):
        self.base = base
        self.target = target

    def __str__(self):
        return f"Error while Validating {self.base} with {self.target}"


class InvalidSignature(ValidationException):
    def __str__(self):
        return f"Invalid Parameter Signature for {self.base.var_name} and {self.target.var_name}"


class NoPressend(Exception):
    pass