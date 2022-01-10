import typing

import deepl

from langpy.compiler.tokens import EntryToken
from langpy.translator.translator_base import TranslatorBase
from deepl import Translator
import re


class PendingTranslation:
    def __init__(self, prepared_token, to_translate):
        self.prepared_token: EntryToken = prepared_token
        self.to_translate: str = to_translate


class TranslationChunk:
    MAX_SIZE = 10

    def __init__(self, chunk_id: int):
        self.id = chunk_id
        self.to_translate = []

    def __len__(self):
        return len(self.to_translate)

    def add_pending(self, p: PendingTranslation):
        self.to_translate.append(p)


class DeeplTranslator(TranslatorBase):

    def __init__(self, manager, tokenizer, target):
        super().__init__(manager, tokenizer, target)
        self.deepl = Translator(manager.config["deepl_key"])
        self.chunks = []
        self.current_chunk = None

    def _check_available(self):
        pass

    def on_iter_done(self, ret):
        for chunk in self.chunks:
            self._translate_chunk(chunk)

    def _translate_chunk(self, chunk):
        i: PendingTranslation
        to_translate = []
        for i in chunk.to_translate:
            to_translate.append(i.to_translate)
        results = self._bulk_translation(to_translate)
        for index, pending in enumerate(chunk.to_translate):
            pending.prepared_token.set_value(results[index])

    def _bulk_translation(self, source: list[str]):
        translate: list[str] = []
        reg = re.compile("{\w*}")
        for text in source:
            translate.append(self._insert_ignore_tags(text, reg))
        results: typing.Union[list[deepl.TextResult], deepl.TextResult] = \
            self.deepl.translate_text(translate,
                                      tag_handling="xml",
                                      ignore_tags=["xignore"],
                                      target_lang=self.target_language.upper())

        if not isinstance(results, list):
            results = [results]
        ret = [i.text.replace("<xignore>", "").replace("</xignore>", "") for i in results]
        return ret

    def _translate_token(self, source: EntryToken) -> EntryToken:
        new = source.copy_empty()
        if self.current_chunk is None or len(self.current_chunk) >= TranslationChunk.MAX_SIZE:
            self.current_chunk = TranslationChunk(len(self.chunks) + 1)
            self.chunks.append(self.current_chunk)
        self.current_chunk.add_pending(PendingTranslation(new, source.value))
        return new

    def _insert_ignore_tags(self, value: str, regex):
        match = regex.findall(value)
        for i in match:
            value = value.replace(i, "<xignore>" + i + "</xignore>")
        return value
