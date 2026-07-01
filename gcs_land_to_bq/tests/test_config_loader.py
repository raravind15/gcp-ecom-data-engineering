from unittest.mock import mock_open

from utils import config_loader


def test_load_yaml_config(mocker):

    yaml_content = """
target_dataset: ds_raw
target_table: customers_raw
"""

    mock_file = mock_open(
        read_data=yaml_content
    )

    mocker.patch(
        "builtins.open",
        mock_file
    )

    config = config_loader.load_yaml_config(
        "customers"
    )

    assert config["target_dataset"] == "ds_raw"

    assert config["target_table"] == "customers_raw"

    mock_file.assert_called_once_with(
        "configs/customers.yaml",
        "r"
    )