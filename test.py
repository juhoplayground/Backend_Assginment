
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app
import fakeredis
import pytest


client = TestClient(app)

@pytest.fixture
def fake_redis():
    return fakeredis.FakeStrictRedis()

def test_make_shorten(fake_redis):
    response = client.post('/shorten', json={'url': 'https://www.google.com/'})
    assert response.status_code == 200
    data = response.json()
    assert 'short_url' in data
    
def test_make_shorten_with_expiration(fake_redis):
    future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    response = client.post('/shorten', json={'url': 'https://www.google.com/', 'input_datetime_str': future_date})
    assert response.status_code == 200
    data = response.json()
    assert 'short_url' in data
    
def test_make_shorten_with_past_expiration(fake_redis):
    past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    response = client.post('/shorten', json={'url': 'https://www.google.com/', 'input_datetime_str': past_date})
    assert response.status_code == 400
    data = response.json()
    assert data['message'] == '만료 기간은 미래 시점으로 입력 해야함'
    
def test_get_url(fake_redis):
    response = client.post('/shorten', json={'url': 'https://www.google.com/'})
    assert response.status_code == 200
    short_url = response.json()['short_url']
    
    get_response = client.get(f'/{short_url}', follow_redirects=False)
    assert get_response.status_code == 301
    assert get_response.headers['location'] == 'https://www.google.com/'

def test_get_url_not_found(fake_redis):
    get_response = client.get('/nonexistentkey')
    assert get_response.status_code == 404
    data = get_response.json()
    assert data['message'] == 'HTTP_404_NOT_FOUND'
    
def test_get_stats(fake_redis):
    shorten_response = client.post('/shorten', json={'url': 'https://google.com/'})
    short_url = shorten_response.json()['short_url']
    
    client.get(f'/{short_url}')
    
    stats_response = client.get(f'/stats/{short_url}')
    assert stats_response.status_code == 200
    data = stats_response.json()
    assert '해당 URL의 조회 수' in data['message']