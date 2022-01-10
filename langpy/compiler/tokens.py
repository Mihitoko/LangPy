import re


class LanguageGroupToken:
    def __init__(self, var_name, comment=None):
        self.var_name = var_name
        self.comment = comment
        self.tree = []

    def add_item(self, item):
        self.tree.append(item)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.var_name == other.var_name

    def __repr__(self):
        return f"GroupToken <var_name={self.var_name}, comment='{self.comment}', tree={self.tree}>"


class EntryToken:
    PARAMETER_REGEX = re.compile(r"{(\w*)}")

    def __init__(self, var_name, value, comment=None):
        self.var_name: str = var_name
        self.value = self.__process(value)
        self.comment = comment
        self.parameters = self.PARAMETER_REGEX.findall(self.value)

    def __process(self, value: str) -> str:
        lines = value.split("\n")
        for i, line in enumerate(lines):
            lines[i] = line.strip()
        return "\n".join(lines)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.var_name == other.var_name

    def __repr__(self):
        return f"EntryToken <var_name={self.var_name}, value='{self.value}', comment={self.comment}, " \
               f"params={self.parameters}>"
