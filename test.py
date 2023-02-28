""" in order to run test cases, type `pytest test.py` in terminal """
import requests

def test_initial_server():
    """Test is initial server works locally"""
    response = requests.get('http://127.0.0.1:5000/', timeout=10)
    assert response.status_code == 200
