# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Tests for the LogAnlaytics Uploader class."""

from pathlib import Path
from unittest.mock import patch
import pytest

from requests.models import Response
import pandas as pd

from msticpy.data.uploaders.loganalytics_uploader import LAUploader
from msticpy.common.exceptions import MsticpyConnectionError

from ...unit_test_lib import get_test_data_path

_TEST_DATA = get_test_data_path()


@patch("requests.post")
def test_df_upload(mock_put):
    """Check DataFrame upload."""
    response = Response()
    response.status_code = 200
    mock_put.return_value = response
    la_uploader = LAUploader(workspace='1234', workspace_secret='password', debug=True)
    data_path = Path(_TEST_DATA).joinpath('syslog_data.csv')
    data = pd.read_csv(data_path)
    la_uploader.upload_df(data, 'test')


@patch("requests.post")
def test_file_upload(mock_put):
    """Check file upload."""
    response = Response()
    response.status_code = 200
    mock_put.return_value = response
    la_uploader = LAUploader(workspace='1234', workspace_secret='password', debug=True)
    data_path = Path(_TEST_DATA).joinpath('syslog_data.csv')
    la_uploader.upload_file(data_path, 'test')


@patch("requests.post")
def test_folder_upload(mock_put):
    """Check folder upload."""
    response = Response()
    response.status_code = 200
    mock_put.return_value = response
    la_uploader = LAUploader(workspace='1234', workspace_secret='password', debug=True)
    data_path = Path(_TEST_DATA).joinpath('uploader')
    la_uploader.upload_folder(data_path, 'test')


@patch("requests.post")
def test_upload_fails(mock_put):
    """Check upload failure."""
    response = Response()
    response.status_code = 503
    mock_put.return_value = response
    la_uploader = LAUploader(workspace='1234', workspace_secret='password', debug=True)
    data_path = Path(_TEST_DATA).joinpath('syslog_data.csv')
    data = pd.read_csv(data_path)
    with pytest.raises(MsticpyConnectionError) as err:
        la_uploader.upload_df(data, 'test')
        assert 'LogAnalytics data upload failed with code 503' in str(err.value)
