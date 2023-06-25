import pytest
from flask import Flask, render_template, jsonify
from unittest.mock import patch

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.data == b"healthy"

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

@patch("requests.get")
def test_quote(mock_get, client):
    expected_quote = "Test quote"
    mock_get.return_value = MockResponse(expected_quote)
    response = client.get("/get_quote")
    assert response.status_code == 200
    assert expected_quote in response.data.decode("utf-8")

class MockResponse:
    def __init__(self, text):
        self.text = text
    def json(self):
        return {"quote": self.text}
