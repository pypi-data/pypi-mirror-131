import collections

import charset_normalizer
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from obelist import errors


class Configuration(collections.UserDict):

    # _SCHEMA_FILENAME = "schemas/config.json"
    # _schema_path = None
    # _schema = None

    _file_path = None

    id = None
    filename = None
    valid = None

    _dict = None

    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path.resolve()
        self.id = self._file_path.stem
        self.filename = str(self._file_path)
        # file_path = pathlib.Path(__file__)
        # schema_path = file_path.parent.joinpath(self._SCHEMA_FILENAME)
        # self._schema_path = schema_path.resolve()
        # self._parse_schema()
        # self._validate_config()
        self._parse_config()

    # def _parse_schema(self):
    #     with open(self._schema_path) as file:
    #         try:
    #             self._schema = json.load(file)
    #         except json.JSONDecodeError as err:
    #             raise _errors.ParseError(err)
    #     # ic(self._schema)

    # TODO: DRY out this method (used elsewhere)
    def _decode(self, bytes):
        # TODO: Catch encoding errors
        charset_data = charset_normalizer.from_bytes(bytes).best()
        return str(charset_data)

    def _parse_config(self):
        with open(self._file_path, "rb") as file:
            bytes = file.read()
            content = self._decode(bytes)
            try:
                config_dict = yaml.load(content, Loader=Loader)
            except yaml.YAMLError as err:
                raise errors.YamlError(message=err)
        self.update(config_dict)
        # ic(self)

    # def _validate_config(self):
    #     try:
    #         jsonschema.validate(instance=None, schema=self._schema)
    #     except exceptions.ValidationError as err:
    #         raise _errors.SchemaError(err)
