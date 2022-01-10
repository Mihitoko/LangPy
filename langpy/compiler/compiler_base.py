import abc
import typing
from abc import ABC, abstractmethod
import io

from langpy.compiler.tokens import LanguageGroupToken, EntryToken


class CompilerBase(ABC):
    def __init__(self, **flags):
        self.flags = flags

    @property
    @abstractmethod
    def out_file_name(self):
        """
        Insert outfile with extension in property
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def compile_schema(self, token_stream: list[typing.Union[LanguageGroupToken, EntryToken]], abstract=False,
                       name: str = None) -> io.StringIO:

        raise NotImplementedError

    @abstractmethod
    def create_access_file(self, to_compile: dict) -> io.StringIO:
        raise NotImplementedError

