import pytest
from model_bakery import baker
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.test import APIClient

from demo.models import Message


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def message_factory():
    def factory(*args, **kwargs):
        return baker.make(Message, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_messages(client, user, message_factory):
    # Arrange — готовим данные
    messages = message_factory(_quantity=10)

    # Act — совершаем действие, которое хотим протестировать
    response = client.get('/messages/')

    # Assert — проверяем результат
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(messages)
    # assert data[0]['text'] == 'test'
    for i, m in enumerate(data):
        assert m['text'] == messages[i].text


@pytest.mark.django_db
def test_create_message(client, user):
    count = Message.objects.count()
    response = client.post('/messages/', data={
        'user': user.id,
        'text': 'test text'
    })
    assert Message.objects.count() == count + 1

    assert response.status_code == 201
