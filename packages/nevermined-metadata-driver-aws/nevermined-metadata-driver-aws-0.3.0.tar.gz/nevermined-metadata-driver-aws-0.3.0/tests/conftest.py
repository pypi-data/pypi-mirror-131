import configparser
from metadata_driver_aws.config_parser import parse_config
from pathlib import Path

import pytest

from metadata_driver_aws.data_plugin import Plugin


@pytest.fixture
def aws_plugin():
    config_path = Path(__file__).parent / "resources/config.ini"
    config = parse_config(config_path.as_posix(), "metadata-driver")
    return Plugin(config)


@pytest.fixture
def test_file_path():
    test_file_path = Path(__file__).parent / "resources/test_file.md"
    return test_file_path.as_posix()
