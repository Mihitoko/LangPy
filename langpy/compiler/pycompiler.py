import typing
import io

from .compiler_base import CompilerBase
from .tokens import EntryToken, LanguageGroupToken


class PyCompiler(CompilerBase):

    def __init__(self, **flags):
        super().__init__(**flags)

    @property
    def out_file_name(self):
        return "/__init__.py"

    def compile_schema(self, token_stream: list[typing.Union[LanguageGroupToken, EntryToken]], abstract=False,
                       name: str = None):
        """
        Invokes a Language-schema file compilation.
        This file does not contain any Strings for the translation. It is just a schema so ids can use
        auto-completion.
        :param name:
        :param abstract:
        :param token_stream:
        :return:
        """
        top_lvl_group = LanguageGroupToken("LanguageSchema" if not name else name,
                                           comment="Auto generated, Language schema")
        top_lvl_group.tree = token_stream
        str_buffer = io.StringIO()
        indent = 0
        ret = self._build_schema_group_recursive(indent, top_lvl_group, ab=abstract)
        str_buffer.write(ret.getvalue())
        return str_buffer

    def _build_schema_group_recursive(self, current_indent, group_token: LanguageGroupToken, ab=False, path: list=None) -> io.StringIO:
        """
        Recursively scans token stream for Group Tokens and pareses them into the string buffer.
        :param current_indent:
        :param group_token:
        :return io.StringIO:
        """
        ret = io.StringIO()
        ret.write(f"{' ' * current_indent}class {group_token.var_name}:\n")
        current_indent += 4
        if path is None and ab is True:
            path = []
            ret.write(f"{' ' * current_indent}_path = ''\n")
        elif ab is True:
            path.append(group_token.var_name)
            ret.write(f"{' ' * current_indent}_path = '{'.'.join(path)}'\n")
        if group_token.comment:
            ret.write(f"{' ' * current_indent}\"\"\"\n{' ' * current_indent}{group_token.comment}"
                      f"\n{' ' * current_indent}\"\"\"\n")
        for token in group_token.tree:
            if isinstance(token, EntryToken):
                str_io: io.StringIO = self._build_schema_entry(current_indent, token, schema=ab)
                ret.write(str_io.getvalue())
            if isinstance(token, LanguageGroupToken):
                t = self._build_schema_group_recursive(current_indent, token, ab=ab, path=path.copy() if path else None)
                ret.write(t.getvalue())
        return ret

    def _build_schema_entry(self, current_indent, token, schema=False) -> io.StringIO:
        indent = current_indent
        str_buffer = io.StringIO()
        str_buffer.write(f"{' ' * indent}class {token.var_name}:\n")
        indent += 4
        str_buffer.write(f"{' ' * indent}\"\"\"\n{' ' * indent}{token.comment}"
                         f"\n{' ' * indent}\"\"\"\n")
        if not schema:
            w = token.value.replace("\n", f"\n{' ' * indent}")
            str_buffer.write(f"{' ' * indent}__value = \"\"\"{w}\"\"\"\n")
        else:
            str_buffer.write(f"{' ' * indent}__value = ''\n")
        str_buffer.write(f"{' ' * indent}@classmethod\n")
        com = ""
        if len(token.parameters) >= 1:
            com = ", "
        str_buffer.write(f"{' ' * indent}def get_string(cls{com}{', '.join(token.parameters)}):\n")
        indent += 4
        if not schema:
            s = []
            if len(token.parameters) >= 1:
                for i in token.parameters:
                    s.append(f"{i}={i}")
                str_buffer.write(f"{' ' * indent}return cls.__value.format({', '.join(s)})\n")
            else:
                str_buffer.write(f"{' ' * indent}return cls.__value\n")
        else:
            str_buffer.write(f"{' ' * indent}pass\n")
        return str_buffer

    def create_access_file(self, to_compile: dict):
        ret = io.StringIO()
        ret.write("from .schema import LanguageSchema\n")
        a = []
        for k, v in to_compile.items():
            a.append(f"'{k}': {v['class_name']}")
            ret.write(f"from .{k} import {v['class_name']}\n")

        ret.write(f"access = {{{', '.join(a)}}}\n")
        ret.write("""def get_language(lang: str, path: object = None):
    if not path:
        return access[lang]
    if isinstance(path, str):
        p = path.split(".")
    else:
        p = path._path.split(".")
    new = access[lang]
    for i in p:
        if len(i) == 0:
            continue
        new = getattr(new, i)
    return new""")
        return ret

