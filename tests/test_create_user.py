import allure
import requests
import pytest
from config import URL, ENDPOINT_REGISTER, ENDPOINT_USER
from helpers import MESSAGE_USER_EXISTS, MESSAGE_NOT_ENOUGH_USER_DATA


class TestPostUser:

    @allure.title("Успешное создание пользователя")
    def test_create_new_user(self, payload_user):
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)

        assert response.status_code == 200
        assert 'accessToken' in response.json()

        access_token = response.json()['accessToken']
        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Нельзя создать двух одинаковых пользователей")
    def test_cannot_create_two_identical_users(self, payload_user):
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)

        assert response.status_code == 403
        assert response.json()['message'] == MESSAGE_USER_EXISTS

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Нельзя создать пользователя без заполнения обязательного поля")
    @pytest.mark.parametrize(
        'empty_field',
        ('email', 'password', 'name')
    )
    def test_cannot_create_user_with_empty_field(self, payload_user, empty_field):
        with allure.step(f'Не заполнено обязательное поле: {empty_field}'):
            payload_user[empty_field] = ''
            response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)

            assert response.status_code == 403
            assert response.json()['message'] == MESSAGE_NOT_ENOUGH_USER_DATA
