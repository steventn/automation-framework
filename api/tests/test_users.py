import pytest
from ..core.api.user_api import UserAPI
from ..core.api.schema import UserSchema

@pytest.fixture(scope="module")
def user_api():
    return UserAPI(env="dev")

def test_get_user(user_api):
    response = user_api.get_user(1)
    assert response.status_code == 200

    user = UserSchema(**response.json())
    assert user.id == 1
    assert user.name != ""

def test_list_users(user_api):
    response = user_api.list_users()
    assert response.status_code == 200

    users = response.json()
    assert len(users) > 0
    for u in users:
        UserSchema(**u)

def test_create_user(user_api):
    payload = {
        "name": "John Doe",
        "username": "johnd",
        "email": "johndoe@example.com"
    }
    response = user_api.create_user(payload)
    assert response.status_code in [200, 201]

    user = response.json()
    assert user["name"] == payload["name"]

def test_get_posts(user_api):
    response = user_api.get_posts()
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 100
    for post in posts:
        assert "userId" in post
        assert "id" in post
        assert "title" in post
        assert "body" in post
