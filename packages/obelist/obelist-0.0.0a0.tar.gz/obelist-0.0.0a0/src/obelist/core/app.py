import sh

import pathlib

import obelist
from obelist import errors
from .config import Configuration
from .parse import Parser


class Application:

    _PKG_CONFIG_DIR = "data/configs"

    _USER_CONFIG_DIR = ".obelist"

    _CONFIG_GLOB = "**/*.yaml"

    _quiet = None
    _verbose = None

    _root_path = None

    _config_search_paths = []

    _configs = []
    _parsers = {}

    _parser = None

    def configure_output(self, quiet=False, verbose=False):
        self._quiet = quiet
        self._verbose = verbose

    def _build_config_search_paths(self, dir_path):
        search_dir = dir_path.joinpath(f"{self._USER_CONFIG_DIR}")
        if not dir_path.samefile(self._root_path):
            parent = dir_path.parent
            yield from self._build_config_search_paths(parent)
        yield search_dir

    def _find_root(self):
        try:
            stdout = sh.git("rev-parse", "--git-dir")
            root_dir = str(stdout)
            self._root_path = pathlib.Path(root_dir).parent
        except sh.CommandNotFound:
            self._root_path = pathlib.Path.cwd().root

    def set_config_search_paths(self, search_path):
        search_path = list(search_path)
        pwd_path = pathlib.Path(".").resolve()
        if not search_path:
            search_path.append(obelist.configs_dir_path)
            self._find_root()
            for path in self._build_config_search_paths(pwd_path):
                search_path.append(path)
        for path in reversed(search_path):
            absolute_path = path.resolve()
            self._config_search_paths.append(absolute_path)

    def get_config_search_paths(self):
        return self._config_search_paths

    def _get_config_files(self):
        for dir_path in self._config_search_paths:
            if dir_path.is_dir():
                yield from dir_path.glob(self._CONFIG_GLOB)

    def _load_config(self, config_path):
        config = Configuration(config_path)
        self._configs.append(config)
        parser = Parser(self, config)
        self._parsers[config.id] = parser

    def load_configs(self):
        for file_path in self._get_config_files():
            self._load_config(file_path)

    def get_configs(self):
        return self._configs

    def debug(self, config_id):
        raise errors.NotImplementedError()

    def parse(self, parser_id, input, format):
        try:
            self._parser = self._parsers[parser_id]
        except KeyError as err:
            raise errors.NoParserError()
        self._parser.parse(input, format)

    def print(self, sort_by, error_on):
        return self._parser.print(sort_by, error_on)
