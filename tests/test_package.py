import pytest
import requests
from unittest.mock import patch
import sys
import os

# Add the package root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blastwrapper import put_query, check_status, get_results

BASE_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

# Sample test data
FAKE_RID = "TEST12345"
FAKE_SEQUENCE = "ATCGATCGATCG"
FAKE_BLAST_RESPONSE = "RID = TEST12345\n"

### 1️⃣ Test `put_query` ###
@patch("requests.get")
def test_put_query_success(mock_get):
    """Test successful query submission returns an RID."""
    mock_get.return_value.text = FAKE_BLAST_RESPONSE  # Mock API response
    
    rid = put_query(FAKE_SEQUENCE)
    assert rid == FAKE_RID

@patch("requests.get")
def test_put_query_failure(mock_get):
    """Test API failure during query submission."""
    mock_get.return_value.text = "Error submitting job."
    
    with pytest.raises(SystemExit):
        put_query(FAKE_SEQUENCE)

### 2️⃣ Test `check_status` ###
@patch("requests.get")
def test_check_status_ready(mock_get):
    """Test check_status when job is complete."""
    mock_get.return_value.text = "Status=READY"
    
    status = check_status(FAKE_RID, 60)
    assert status == "READY"

@patch("requests.get")
def test_check_status_not_ready(mock_get):
    """Test check_status when job is still running."""
    mock_get.return_value.text = "Status=WAITING"
    
    status = check_status(FAKE_RID, 60)
    assert status == "NOT READY"

### 3️⃣ Test `get_results` ###
@patch("requests.get")
def test_get_results_success(mock_get):
    """Test fetching results when job is complete."""
    mock_response = requests.Response()
    mock_response._content = b"Mock BLAST Results"
    mock_get.return_value = mock_response

    response = get_results(FAKE_RID)
    assert response.text == "Mock BLAST Results"

@patch("requests.get")
def test_get_results_invalid_rid(mock_get):
    """Test fetching results with an invalid RID."""
    mock_response = requests.Response()
    mock_response._content = b"Error: RID not found"
    mock_get.return_value = mock_response

    response = get_results("INVALID_RID")
    assert "Error: RID not found" in response.text
