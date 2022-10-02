import pytest


@pytest.mark.parametrize("title, content, status_code", [
    ('First Post', 'Skating in Hawaii', 201),
    ('Top Ten Recipes for nights', 'Description of food', 201),
    ('We love python', 'Snakes are wonderful', 201)
])
def test_create_post(authorized_client, title, content, status_code):
    response = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content
        }
    )

    assert response.status_code == status_code


def test_get_posts(authorized_client, test_posts):
    response = authorized_client.get(
        "/posts/"
    )

    assert response.status_code == 200


@pytest.mark.parametrize("post_id, status_code", [
    ('1', 200),
    ('5', 404),
    ('five', 422)
])
def test_get_specific_post(authorized_client, test_posts, post_id, status_code):
    response = authorized_client.get(
        f"/posts/{post_id}"
    )

    assert response.status_code == status_code


@pytest.mark.parametrize("post_id, status_code", [
    ('1', 204),
    ('5', 404),
    ('five', 422)
])
def test_delete_post(authorized_client, test_posts, post_id, status_code):
    response = authorized_client.delete(
        f"/posts/{post_id}"
    )

    assert response.status_code == status_code


@pytest.mark.parametrize("post_id, status_code", [
    ('1', 200),
    ('5', 404),
    ('five', 422)
])
def test_update_post(authorized_client, test_posts, post_id, status_code):
    response = authorized_client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated title",
            "content": "Updated content"
        }
    )

    assert response.status_code == status_code
