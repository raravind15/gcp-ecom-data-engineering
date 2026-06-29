from unittest.mock import MagicMock
from config import *
import storage_service

def test_copy_file(mocker):

    mock_storage_client=MagicMock()
    mock_source_bucket=MagicMock()
    mock_source_blob=MagicMock()
    mock_landing_bucket=MagicMock()

    mocker.patch("config.get_storage_client",
                 return_value=mock_storage_client)
    mock_storage_client.bucket.side_effect=[mock_source_bucket,mock_landing_bucket]
    mock_source_bucket.blob.return_value=mock_source_blob

    storage_service.copy_file("customers.parquet")

    mock_source_bucket.copy_blob.assert_called_once_with(mock_source_blob,mock_landing_bucket,"customers.parquet")