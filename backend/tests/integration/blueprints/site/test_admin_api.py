# we shoudl write this with pytest 

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_get_dashboard():
    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    json_data = response.json()
    assert "user_count" in json_data
    assert "active_podcasts" in json_data
    assert "site_uptime_days" in json_data

def test_list_users():
    response = client.get("/admin/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert "email" in users[0]

def test_list_podcasts():
    response = client.get("/admin/podcasts")
    assert response.status_code == 200
    podcasts = response.json()
    assert isinstance(podcasts, list)
    assert len(podcasts) > 0
    assert "title" in podcasts[0]

def test_listening_trends():
    response = client.get("/admin/stats/listening-trends")
    assert response.status_code == 200
    data = response.json()
    assert "dates" in data and "listens" in data
    assert isinstance(data["dates"], list)
    assert isinstance(data["listens"], list)

def test_site_uptime():
    response = client.get("/admin/site-uptime")
    assert response.status_code == 200
    uptime_data = response.json()
    assert "uptime_days" in uptime_data
    assert "last_downtime" in uptime_data
    assert "downtime_duration_minutes" in uptime_data