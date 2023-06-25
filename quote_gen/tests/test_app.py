import random
from flask import Flask
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TEST"] = True
    with app.test_client() as client:
        yield client
        

@pytest.fixture    
def quotes():
    return [
        "The greatest glory in living lies not in never falling, but in rising every time we fall. -Nelson Mandela", 
        "The way to get started is to quit talking and begin doing. -Walt Disney",
        "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking. -Steve Jobs",
        "If life were predictable it would cease to be life, and be without flavor. -Eleanor Roosevelt",
        "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough. -Oprah Winfrey",
        "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success. -James Cameron",
    ]
    

def test_health(client):
    """Test the /health endpoint"""   
    response = client.get("/health")
    assert response.status_code == 200  
    assert response.data == b"healthy"
    

def test_home(client):
    """Test the homepage"""
    response = client.get("/")    
    assert response.status_code == 200
    
        
def test_quote(client, quotes, mocker):    
    """Test the /quote endpoint"""
    mocker.patch("random.randrange", return_value=0)    
    mocker.patch("app.quotes", quotes)   
    response = client.get("/quote")
    assert response.status_code == 200  
    response_quote = response.data.decode("utf-8")    
    assert response_quote == quotes[0]
