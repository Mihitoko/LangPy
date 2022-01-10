import traceback
from abc import ABC, abstractmethod
import logging

from langpy.compiler.tokenizer import Tokenizer
from langpy.compiler.tokens import LanguageGroupToken, EntryToken
from langpy.projectmanager import CachedTokens, ProjectManager

logger = logging.getLogger("langpy")


class TranslatorBase(ABC):

    def __init__(self, manager: ProjectManager, tokenizer: Tokenizer, target_language: str):
        if self.__class__.mro()[0] == TranslatorBase:
            # Raise error when TranslatorBase is initiated directly
            # TODO: Add proper Exception
            raise Exception
        self.tokenizer = tokenizer
        self.base_stream = tokenizer.get_base_schema()
        self.target_language = target_language
        self.manager = manager

    @abstractmethod
    def _translate_token(self, source: EntryToken) -> EntryToken:
        raise NotImplementedError

    @abstractmethod
    def _check_available(self):
        raise NotImplementedError

    def translate(self, ignore_cache=False):
        cached = self.manager.get_cached_tokens()
        old = self.manager.get_template(self.target_language)
        if old is not None:
            ret = self._recursive_iter(self.base_stream, to_iter=cached.last_used, ignore=ignore_cache,
                                       cached_language=self.tokenizer.tokenize(self.target_language, old,
                                                                               validate=False))
        else:
            ret = self._recursive_iter(self.base_stream, to_iter=cached.last_used, ignore=ignore_cache,
                                       cached_language=[])
        cached.set_new_cache_state(self.base_stream)
        return ret

    def _recursive_iter(self, iter_, ignore, cached_language: list, to_iter: list = None):

        ret = []
        for token in iter_:
            if isinstance(token, EntryToken):
                try:
                    index: EntryToken = to_iter[to_iter.index(token)]
                    if index.value == token.value and not ignore:
                        a: EntryToken = cached_language[cached_language.index(token)]
                        ret.append(a)
                        continue
                except (ValueError, AttributeError):
                    pass
                ret.append(self._translate_token(token))

            elif isinstance(token, LanguageGroupToken):
                group = LanguageGroupToken(token.var_name, comment=token.comment)
                try:
                    old_lang = cached_language[cached_language.index(token)].tree
                except ValueError:
                    old_lang = []
                if to_iter is not None:
                    i = to_iter[to_iter.index(token)].tree
                else:
                    i = []
                group.tree = self._recursive_iter(token.tree, to_iter=i,
                                                  ignore=ignore, cached_language=old_lang)
                print(group.tree)
                ret.append(group)

        return ret
