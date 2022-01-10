import os
import pickle

import yaml


class CachedTokens:
    FILE_NAME = "tokens.pcl"

    def __init__(self, location: str):
        self.path = location
        self._last_used = None

    @property
    def last_used(self) -> list:
        return self._last_used

    def write(self):
        with open(self.path + self.FILE_NAME, "bw") as f:
            pickle.dump(self, f)

    def set_new_cache_state(self, tokens: list):
        self._last_used = tokens
        self.write()


class ProjectManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.config = self._load_yaml("langpy_config.yaml")

    def _load_yaml(self, file):
        with open(self.base_path + "/" + file, "r") as f:
            data = yaml.full_load(f)
        return data

    def _write_file(self, file, content, mode="w"):
        with open(self.base_path + "/" + file, mode) as f:
            f.write(content)

    def get_template_folder(self):
        return self.config["template_folder"]

    def get_default_template(self):
        return self.get_template(self.config["default"])

    def get_template(self, lang: str):
        try:
            path = self.get_template_folder() + "/" + self.config["templates"][lang]["file_name"]
            return self._load_yaml(path)
        except (OSError, KeyError):
            raise

    def create_cache_env(self):
        if not os.path.exists(self.base_path + "/.langcache"):
            os.mkdir(self.base_path + "/" + ".langcache")

    def get_cached_tokens(self) -> CachedTokens:
        self.create_cache_env()
        if not os.path.exists(self.base_path + "/.langcache/tokens.pcl"):
            return CachedTokens(self.base_path + "/.langcache/")
        with open(self.base_path + "/.langcache/tokens.pcl", "br") as f:
            return pickle.load(f)
