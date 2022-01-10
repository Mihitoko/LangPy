import yaml
from .compiler import get_compiler
from .compiler.tokenizer import Tokenizer
import os


def init():
    path = os.getcwd()
    os.mkdir(path + "/locales")
    os.mkdir(path + "/locales/language")
    os.mkdir(path + "/locales/templates")
    data = {
        "default": "en",
        "out": "/locales/language",
        "template_folder": "/locales/templates",
        "templates": {
            "en": {
                "file_name": "en.yaml",
                "class_name": "EnLanguageSchema"
            }
        }
    }
    _write_file(path, "langpy_config.yaml", yaml.dump(data))
    _write_file(path + "/locales/templates", "en.yaml", "# Put your language data here.\n"
                                                         "# Refer to the docs to soo how the structure has to be\n")


def compile_job(path, **flags):
    config = _load_yaml(path, "langpy_config.yaml")
    # Setting up stuff
    target_lang = config.get("target", "py")
    compiler = get_compiler(target_lang)
    to_compile: dict = config["templates"]
    schema = config["default"]
    out = config["out"]
    template_folder = path + config["template_folder"]
    main = to_compile.get(schema)
    data = _load_yaml(template_folder, main["file_name"])
    to_compile: dict = config["templates"]
    loaded_tokenizer = Tokenizer(data)
    # Write schema file.
    output = compiler.compile_schema(loaded_tokenizer.get_token_tree(), abstract=True)
    _write_file(path + out, "schema.py", output.getvalue())
    # Writing actual language files.
    for k, v in to_compile.items():
        data = _load_yaml(template_folder, v["file_name"])
        tokens = loaded_tokenizer.tokenize(k, data, validate=True)
        output = compiler.compile_schema(tokens, abstract=False, name=v["class_name"])
        _write_file(path + out, f"{k}.py", output.getvalue())
    _write_file(path + out, compiler.out_file_name, compiler.create_access_file(to_compile).getvalue())


def new_template(path, lang):
    config = _load_yaml(path, "langpy_config.yaml")
    folder = path + config["template_folder"]
    loaded_tokenizer = Tokenizer(_load_yaml(folder, config["templates"][config["default"]]["file_name"]))
    _write_file(folder, lang + ".yaml", yaml.dump(loaded_tokenizer.new_template()))
    first = lang[0].upper()
    config["templates"].update({lang: {
        "file_name": lang + ".yaml",
        "class_name": first + lang[1:] + "LanguageSchema"
    }})
    _write_file(path, "langpy_config.yaml", yaml.dump(config))


def _load_yaml(path, file):
    with open(path + "/" + file, "r") as f:
        data = yaml.full_load(f)
    return data


def _write_file(path, file, content, mode="w"):
    with open(path + "/" + file, mode) as f:
        f.write(content)
