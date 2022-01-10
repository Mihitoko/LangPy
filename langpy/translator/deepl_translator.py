import deepl

from langpy.compiler.tokens import EntryToken
from langpy.translator.translator_base import TranslatorBase
from deepl import Translator
import re


class DeeplTranslator(TranslatorBase):

    def __init__(self, manager, tokenizer, target):
        super().__init__(manager, tokenizer, target)
        self.deepl = Translator(manager.config["deepl_key"])

    def _check_available(self):
        pass

    def _translate_token(self, source: EntryToken) -> EntryToken:
        tag_str = self._insert_ignore_tags(source.value, re.compile("{\w*}"))
        translated: deepl.TextResult = self.deepl.translate_text(tag_str, tag_handling="xml",
                                                                 ignore_tags=["xignore"],
                                                                 target_lang=self.target_language.upper())
        s = translated.text.replace("<xignore>", "").replace("</xignore>", "")
        new = EntryToken(source.var_name, s)
        print(new)
        return new

    def _insert_ignore_tags(self, value: str, regex):
        match = regex.findall(value)
        for i in match:
            value = value.replace(i, "<xignore>" + i + "</xignore>")
        return value
