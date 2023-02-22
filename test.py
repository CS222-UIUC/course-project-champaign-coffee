# TEST CASES
# in order to run test cases, type `pytest test.py` in terminal

import requests

def test_initial_server():
    response = requests.get('http://127.0.0.1:5000/')
    assert response.status_code == 200
