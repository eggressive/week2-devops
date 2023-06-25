import random
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask.testing import FlaskClient
import pytest
from unittest.mock import patch

from ..app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.ok
    assert response.data == b"healthy"

def test_home(client):
    response = client.get("/")
    assert response.ok

@patch('random.choice')
def test_quote(mock_random_choice, client):
    expected_quotes = [
        "The greatest glory in living lies not in never falling, but in rising every time we fall. -Nelson Mandela",
        "The way to get started is to quit talking and begin doing. -Walt Disney",
        "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking. -Steve Jobs",
        "If life were predictable it would cease to be life, and be without flavor. -Eleanor Roosevelt",
        "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough. -Oprah Winfrey",
        "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success. -James Cameron",
    ]
    mock_random_choice.return_value = expected_quotes[0]
    response = client.get("/quote")
    assert response.ok
    soup = BeautifulSoup(response.data, 'html.parser')
    assert expected_quotes[0] in soup.text
