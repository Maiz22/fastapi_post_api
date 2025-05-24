from fastapi.testclient import TestClient
from app.main import app


def test_get_posts() -> None:
    with TestClient(app) as client:
        response = client.get("/posts")
        assert response.status_code == 200


def test_get_one_post_success() -> None:
    with TestClient(app) as client:
        response = client.get("/posts/1")
        assert response.status_code == 200


def test_get_one_post_not_exist() -> None:
    with TestClient(app) as client:
        response = client.get("post/9999999")
        assert response.status_code == 404


def test_create_post_success() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/posts",
            json={
                "title": f"automated post",
                "content": "this is a post created by the test automation",
            },
        )
        assert response.status_code == 201
        assert response.json()["title"] == "automated post"


def test_create_post_no_title() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/posts", json={"content": "this is a post created by the test automation"}
        )
        assert response.status_code == 422


def test_create_post_no_content() -> None:
    with TestClient(app) as client:
        response = client.post("/posts", json={"title": "automated post title"})
        assert response.status_code == 422


def test_create_post_no_json() -> None:
    with TestClient(app) as client:
        response = client.post("/posts")
        assert response.status_code == 422


def test_put_post_success() -> None:
    with TestClient(app) as client:
        response = client.put(
            "/posts/1",
            json={
                "title": f"automated put request",
                "content": "this is a post created by the test automation",
            },
        )
        assert response.status_code == 201
        assert response.json()["title"] == "automated put request"


def test_put_post_not_exist() -> None:
    with TestClient(app) as client:
        response = client.put(
            "/posts/9999999",
            json={
                "title": f"automated put request",
                "content": "this is a post created by the test automation",
            },
        )
        assert response.status_code == 404
