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
    PARAMETER_REGEX = re.compile(r"(?<!//){(\w*)}")

    def __init__(self, var_name, value, comment=""):
        self.var_name: str = var_name
        self.value = ""
        self.comment = comment
        self.parameters = []
        self.set_value(value)

    def __process(self, value: str) -> str:
        lines = value.split("\n")
        for i, line in enumerate(lines):
            lines[i] = line.strip()
        return "\n".join(lines)

    def set_value(self, value: str):
        self.parameters = self._get_params(value)
        self.value = self.__process(value)

    def _get_params(self, value):
        par = self.PARAMETER_REGEX.findall(value)
        ret = []
        for i in par:
            if i not in ret:
                ret.append(i)
        return ret
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.var_name == other.var_name

    def __repr__(self):
        return f"EntryToken <var_name={self.var_name}, value='{self.value}', comment={self.comment}, " \
               f"params={self.parameters}>"

    def copy_empty(self):
        ret = EntryToken(self.var_name, "", comment=self.comment)
        return ret
