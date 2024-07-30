import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.data == b"Welcome to AISecretary!"

def test_manage_tasks(client):
    rv = client.post('/api/tasks', json={'id': 1, 'title': 'Test Task'})
    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data['title'] == 'Test Task'

    rv = client.get('/api/tasks')
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data[0]['title'] == 'Test Task'

def test_handle_task(client):
    client.post('/api/tasks', json={'id': 1, 'title': 'Test Task'})

    rv = client.get('/api/tasks/1')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['title'] == 'Test Task'

    rv = client.put('/api/tasks/1', json={'title': 'Updated Task'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['title'] == 'Updated Task'

    rv = client.delete('/api/tasks/1')
    assert rv.status_code == 204
