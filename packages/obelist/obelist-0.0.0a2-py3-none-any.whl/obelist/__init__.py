import pathlib
from importlib.metadata import distribution

dist = distribution("obelist")
version = dist.version

root_dir_path = pathlib.Path(__file__).parent
data_dir_path = root_dir_path.joinpath("data")
schemas_dir_path = data_dir_path.joinpath("schemas")
configs_dir_path = data_dir_path.joinpath("configs")
# Silence vulture
root_dir_path
data_dir_path
schemas_dir_path
configs_dir_path

DEFAULT_COLUMNS = 79
