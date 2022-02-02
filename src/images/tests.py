import pytest

from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image


@pytest.fixture()
def user_A(db):
    user = User.objects.create_user('dummy', 'dummy@test.com', '1234567!')
    return user

@pytest.fixture()
def url_api():
    url = "http://testserver/api"
    return url

@pytest.fixture
def photo_file():
    file = BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

def test_api_page(client, url_api):
    url = url_api + '/'
    data = {
        "images": url + "images/",
        "top5": url + "top5/",
        "random": url + "random/"
    }
    response = client.get(url) 
    assert response.status_code == 200
    assert response.json() == data

def test_create_the_image(client, user_A, photo_file, url_api):
    client.force_login(user_A)
    url = url_api + '/images/'
    response = client.post(
            url,
            {
                "picture": photo_file,
                "body": "photo1"
            },
        )
    assert response.status_code == 201
    assert response.json()['is_fan'] == False
    assert response.json()['is_report'] == False
    assert response.json()['total_likes'] == 0
    assert response.json()['total_reports'] == 0

@pytest.fixture
def create_the_image(client, user_A, photo_file, url_api):
    client.force_login(user_A)
    url = url_api + '/images/'

    response = client.post(
            url,
            {
                "picture": photo_file,
                "body": "photo1"
            },
        )
    return response

def test_likes_the_image(client, user_A, url_api, create_the_image):
    client.force_login(user_A)
    create_the_image
    url_like = url_api + "/images/1/like/"
    response = client.post(
            url_like,
            {
                "id": 1,
                "is_fan": True
            },
        )
    assert response.status_code == 200

    url_fans = url_api + "/images/1/fans/"
    response = client.get(url_fans)
    assert response.status_code == 200

    body = {
        "username": "dummy",
        "full_name": ""
    }
    assert response.json()[0] == body

    url = url_api + "/images/1/"
    response = client.get(url)
    assert response.json()['total_likes'] == 1
    assert response.json()['total_reports'] == 0

    url_unlike = url_api + "/images/1/unlike/"
    response = client.post(
            url_unlike,
            {
                "id": 1,
                "is_fan": False
            },
        )
    assert response.status_code == 200

    response = client.get(url)
    assert response.json()['total_likes'] == 0
    assert response.json()['total_reports'] == 0

def test_reports_the_image(client, user_A, url_api, create_the_image):
    client.force_login(user_A)
    create_the_image
    url_report = url_api + "/images/1/report/"
    response = client.post(
            url_report,
            {
                "id": 1,
                "is_report": True
            },
        )
    assert response.status_code == 200
    
    url_reports = url_api + "/images/1/reports/"
    response = client.get(url_reports)
    assert response.status_code == 200
    body = {
        "username": "dummy",
        "full_name": ""
    }
    assert response.json()[0] == body

    url = url_api + "/images/1/"
    response = client.get(url)
    assert response.json()['total_likes'] == 0
    assert response.json()['total_reports'] == 1

    url_unreport = url_api + "/images/1/unreport/"
    response = client.post(
            url_unreport,
            {
                "id": 1,
                "is_report": False
            },
        )
    assert response.status_code == 200

    response = client.get(url)
    assert response.json()['total_likes'] == 0
    assert response.json()['total_reports'] == 0
