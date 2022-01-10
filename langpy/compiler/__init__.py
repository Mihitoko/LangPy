from .pycompiler import PyCompiler
from .compiler_base import CompilerBase

_all_compilers = {
    "py": PyCompiler
}


def get_compiler(source_lang: str, **flags) -> CompilerBase:
    try:
        ret = _all_compilers[source_lang]
        return ret(**flags)
    except KeyError:
        raise ValueError(f"Cannot compile to desired source language.\nAvailable source languages: "
                         f"{', '.join(_all_compilers.keys())}")
