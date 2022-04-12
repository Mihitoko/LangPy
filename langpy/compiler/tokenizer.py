import logging
import typing

from langpy.compiler.tokens import LanguageGroupToken, EntryToken
from langpy.errors.common import *

logger = logging.getLogger("langpy")


class Tokenizer:
    def __init__(self, template: dict, **flags):
        self.raw_template = template
        self.flags = flags
        self.__token_tree = self.__parse_dict(template, [])

    def get_token_tree(self) -> list:
        return self.__token_tree

    def get_base_schema(self):
        """
        Alias for get_token_tee()
        :return:
        """
        return self.get_token_tree()

    def tokenize(self, lang: str, data: dict, validate=True):
        logger.info(f"Building token tree for language <{lang}> ...")
        ret = self.__parse_dict(data, [])
        if validate:
            self.validate(ret)
        return ret

    def validate(self, stream: list[typing.Union[LanguageGroupToken, EntryToken]],
                 to_compare: list[typing.Union[LanguageGroupToken, EntryToken]] = None):
        # TODO: Add proper Error handling to validation.
        if to_compare is None:
            to_compare = self.get_base_schema()
        for token in to_compare:
            if isinstance(token, LanguageGroupToken):
                try:
                    other = stream.index(token)
                except ValueError:
                    raise NoPressend()
                return self.validate(token.tree, stream[other].tree)
            elif isinstance(token, EntryToken):
                try:
                    other = stream.index(token)
                except ValueError:
                    raise NoPressend()
                o: EntryToken = stream[other]
                if len(token.parameters) != len(o.parameters):
                    raise InvalidSignature(token, o)
                for i in token.parameters:
                    if i not in o.parameters:
                        raise InvalidSignature(token, o)

    def __parse_dict(self, data: dict[str, dict], carry: list) -> list:
        for k, v in data.items():
            args = [k]
            if "@" in k:
                args = k.split("@")
            var_name = args[len(args) - 1]
            if "group" in args:
                comment = data.get("comment", None)
                g = LanguageGroupToken(var_name, comment=comment)
                carry.append(self.__build_group_recursive(v, g))
                continue
            if k == "comment":
                continue
            if isinstance(v, str):
                value = v
            else:
                value = v["value"]
            t = EntryToken(var_name, value, v.get("comment") if isinstance(v, dict) else None)
            carry.append(t)

        return carry

    def __build_group_recursive(self, data: dict, group: LanguageGroupToken) -> LanguageGroupToken:
        logger.debug(f"Building token group with name <{group.var_name}>")
        for k, v in data.items():
            args = [k]
            if "@" in k:
                args = k.split("@")
            var_name = args[len(args) - 1]
            if "group" in args:
                comment = data.get("comment", None)
                g = LanguageGroupToken(var_name, comment=comment)
                group.add_item(self.__build_group_recursive(v, g))
                continue
            if k == "comment":
                continue
            if isinstance(v, str):
                value = v
            else:
                value = v["value"]
            t = EntryToken(var_name, value, v.get("comment") if isinstance(v, dict) else None)
            group.add_item(t)

        return group

    def new_template(self, token_stream: list = None, with_value=False):
        if token_stream is None:
            token_stream = self.get_token_tree()
        ret = {}
        for token in token_stream:
            if isinstance(token, LanguageGroupToken):
                ret.update({f"group@{token.var_name}": self.new_template(token.tree, with_value=with_value)})
            elif isinstance(token, EntryToken):
                ret[f"{token.var_name}"] = {
                    "comment": f"Original string: <{token.value}>" if not token.comment and not with_value
                    else token.comment,
                    "value": "" if not with_value else token.value
                }
        return ret
