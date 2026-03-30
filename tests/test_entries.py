import pytest
from app import db
from app.models import TimeEntry


@pytest.fixture
def auth_client(client):
    client.post("/login", data={"username": "testuser", "password": "testpass"})
    return client


def test_index_renders_for_logged_in_user(auth_client):
    resp = auth_client.get("/")
    assert resp.status_code == 200
    assert b"Log Time" in resp.data


def test_add_entry_persists(auth_client, app):
    auth_client.post("/", data={"task_name": "Writing", "duration_minutes": "90"})
    with app.app_context():
        entry = TimeEntry.query.one()
    assert entry.task_name == "Writing"
    assert entry.duration_minutes == 90


def test_add_entry_appears_on_index(auth_client):
    auth_client.post("/", data={"task_name": "Design", "duration_minutes": "60"})
    resp = auth_client.get("/")
    assert b"Design" in resp.data


def test_add_entry_missing_task_shows_error(auth_client):
    resp = auth_client.post(
        "/", data={"task_name": "", "duration_minutes": "30"}, follow_redirects=True
    )
    assert b"Task name is required" in resp.data


def test_add_entry_missing_duration_shows_error(auth_client):
    resp = auth_client.post(
        "/", data={"task_name": "Reading", "duration_minutes": ""}, follow_redirects=True
    )
    assert b"Duration is required" in resp.data


def test_add_entry_zero_duration_shows_error(auth_client):
    resp = auth_client.post(
        "/", data={"task_name": "Reading", "duration_minutes": "0"}, follow_redirects=True
    )
    assert b"positive integer" in resp.data


def test_add_entry_non_integer_duration_shows_error(auth_client):
    resp = auth_client.post(
        "/", data={"task_name": "Reading", "duration_minutes": "abc"}, follow_redirects=True
    )
    assert b"whole number" in resp.data


def test_total_hours_calculation(auth_client):
    auth_client.post("/", data={"task_name": "A", "duration_minutes": "90"})
    auth_client.post("/", data={"task_name": "B", "duration_minutes": "30"})
    resp = auth_client.get("/")
    assert b"2.0" in resp.data


def test_no_entries_shows_empty_message(auth_client):
    resp = auth_client.get("/")
    assert b"No entries yet" in resp.data
