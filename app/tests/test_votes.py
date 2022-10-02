import pytest


@pytest.mark.parametrize("post_id, dir, status_code", [
    ('1', '1', 201),
    ('5', '1', 404)
])
def test_vote(authorized_client, test_posts, post_id, dir, status_code):
    response = authorized_client.post(
        "/vote/",
        json={
            "post_id": post_id,
            "dir": dir
        }
    )

    assert response.status_code == status_code


def test_already_voted(authorized_client, test_posts):
    first_vote = authorized_client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 1
        }
    )

    second_vote = authorized_client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 1
        }
    )

    assert second_vote.status_code == 409


def test_remove_vote(authorized_client, test_posts):
    first_vote = authorized_client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 1
        }
    )

    second_vote = authorized_client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 0
        }
    )

    assert second_vote.status_code == 201

