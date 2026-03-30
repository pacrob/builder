def test_login_page_renders(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Log In" in resp.data


def test_login_success_redirects_to_index(client):
    resp = client.post(
        "/login",
        data={"username": "testuser", "password": "testpass"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Log Time" in resp.data


def test_login_wrong_password_shows_error(client):
    resp = client.post(
        "/login",
        data={"username": "testuser", "password": "wrong"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in resp.data


def test_login_wrong_username_shows_error(client):
    resp = client.post(
        "/login",
        data={"username": "nobody", "password": "testpass"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in resp.data


def test_logout_redirects_to_login(client):
    client.post("/login", data={"username": "testuser", "password": "testpass"})
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Log In" in resp.data


def test_unauthenticated_index_redirects_to_login(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]
