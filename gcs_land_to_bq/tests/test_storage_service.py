import logging
from unittest.mock import MagicMock

def test_read_parquet_file(mocker):
    mock_storage_client=MagicMock()
    mock_bucket=MagicMock()
    mock_blob=MagicMock()
    