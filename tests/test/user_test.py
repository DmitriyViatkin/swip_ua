import pytest
from io import BytesIO
from tests.conf_test import auth_headers, client



@pytest.mark.user
def test_get_all_user(client, auth_headers):

    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    
    assert "email" in data[0]


@pytest.mark.user
def test_update_user_success(client, auth_headers):
    """ Update user"""

    user_id = 24
    payload={
        "first_name":"Джорж",
        "last_name":"Буш",
        "phone": "+380970000009"
    }
    response = client.put(f"/users/update/{user_id}", json= payload, headers= auth_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Джорж"

@pytest.mark.user
def test_update_user_forbidden(client, auth_headers):
    """ Update user"""

    user_id = 25
    payload={
        "first_name":"Джорж",
        "last_name":"Буш",
        "phone": "+380970000009"
    }
    response = client.put(f"/users/update/{user_id}", json= payload, headers= auth_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden: cannot update other user"

@pytest.mark.user
def test_upload_photo_success(client, auth_headers):
    """
    Позитивний тест: Завантаження валідної картинки (JPEG).
    """
    user_id = 24


    file_content = b"fake-image-binary-content"
    file = {
        "file": ("test_avatar.jpg", BytesIO(file_content), "image/jpeg")
    }

    response = client.post(
        f"/users/update-photo/{user_id}",
        headers=auth_headers,
        files=file
    )

    assert response.status_code == 200
    assert "photo" in response.json()
    assert "user_24_test_avatar.jpg" in response.json()["photo"]

@pytest.mark.user
def test_upload_photo_invalid_type(client, auth_headers):
    """
    Негативний тест: Спроба завантажити текстовий файл замість картинки.
    """
    user_id = 24


    file = {
        "file": ("danger.txt", BytesIO(b"not-an-image"), "text/plain")
    }

    response = client.post(
        f"/users/update-photo/{user_id}",
        headers=auth_headers,
        files=file
    )


    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"

@pytest.mark.user
def test_send_message(client, auth_headers):
    payload = {
        "recipient_id":25,
        "text":'Test message'}
    response = client.post("message/send", json = payload, headers= auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["sender_id"] == 24
    assert data["recipient_id"] == 25
    assert 'id' in data
@pytest.mark.user
def check_history_message(client, auth_headers):

    contact_id = 25
    response = client.get(f"/message/history/{contact_id}", headers= auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert "content" in data[0] or "test" in data[0]
        message = data[0]
        assert message["sender_id"] in [24,25]
        assert message["recipient_id"] in [24,25]

@pytest.mark.user
def test_get_history_unauthorized(client):
    """
    Перевірка, що неавторизований користувач не отримає доступ.
    """
    response = client.get("/message/history/{}")
    assert response.status_code == 403


@pytest.mark.user
def test_favorites_cycle(client, auth_headers):
    """
    Позитивний тест: додаємо в обране та перевіряємо список 'me'.
    """
    advert_id = 34
    payload = {"advert_id": advert_id}

    # 1. Додаємо
    add_response = client.post(
        "/favorites/add",
        json=payload,
        headers=auth_headers
    )
    assert add_response.status_code == 201


    list_response = client.get("/favorites/me", headers=auth_headers)
    assert list_response.status_code == 200

    data = list_response.json()
    assert isinstance(data, list)

    assert any(item["advert_id"] == advert_id for item in data)


@pytest.mark.user
def test_add_to_favorites_duplicate(client, auth_headers):
    """
    Негативний тест: не можна додати одне й те саме оголошення двічі.
    """
    payload = {"advert_id": 34}


    client.post("/favorites/add", json=payload, headers=auth_headers)


    response = client.post("/favorites/add", json=payload, headers=auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Оголошення вже в обраному"


@pytest.mark.user
def test_remove_from_favorites(client, auth_headers):
    advert_id = 34

    response = client.delete(f"/favorites/{advert_id}", headers=auth_headers)


    assert response.status_code == 204


@pytest.mark.user
def test_update_subscription_success(client, auth_headers):
    sub_id = 1

    payload = {
        "auto_renewal": True
    }

    response = client.put(
        f"/users/user/subscription/{sub_id}",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200

    assert response.json()["auto_renewal"] is True


@pytest.mark.user
def test_update_subscription_success(client, auth_headers):
    # Використовуємо ID користувача, під яким ми авторизовані (наприклад, 24)
    user_id = 24
    payload = {
        "auto_renewal": True
    }

    response = client.put(
        f"/users/user/subscription/{user_id}",
        json=payload,
        headers=auth_headers
    )


    assert response.status_code == 200




@pytest.mark.filter
def test_get_results_by_id(client, auth_headers):

    create_resp = client.post(
        "/filters/search",
        json={"rooms": 1, "type_build": "apartment_building"},
        headers=auth_headers
    )
    assert create_resp.status_code == 201
    filter_id = create_resp.json()["filter"]["id"]  # <-- теперь правильно


    resp = client.get(f"/filters/{filter_id}/results", headers=auth_headers)
    assert resp.status_code == 200
    ads = resp.json()
    assert isinstance(ads, list)


@pytest.mark.filter
def test_update_filter(client, auth_headers):
    create_resp = client.post(
        "/filters/search",
        json={"rooms": 1, "type_build": "apartment_building"},
        headers=auth_headers
    )
    filter_id = create_resp.json()["filter"]["id"]

    update_resp = client.patch(
        f"/filters/update/{filter_id}",
        json={"rooms": 2},  # данные для обновления
        headers=auth_headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["rooms"] == 2


@pytest.mark.filter
def test_delete_filter_success(client, auth_headers):
    create_resp = client.post(
        "/filters/search",
        json={"rooms": 1, "type_build": "apartment_building"},
        headers=auth_headers
    )
    filter_id = create_resp.json()["filter"]["id"]

    delete_resp = client.delete(f"/filters/{filter_id}/delete", headers=auth_headers)
    assert delete_resp.status_code == 204




