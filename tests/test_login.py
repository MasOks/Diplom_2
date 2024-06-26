import allure
import requests
import pytest
from config import URL, ENDPOINT_REGISTER, ENDPOINT_LOGIN, ENDPOINT_USER
from helpers import MESSAGE_INCORRECT_USER_DATA


class TestPostLogin:

    @allure.title("Успешная авторизация под существующим пользователем")
    def test_login_exist_user(self, payload_user):
        requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        del payload_user['name']
        response = requests.post(f'{URL}{ENDPOINT_LOGIN}', json=payload_user)

        assert response.status_code == 200
        assert 'accessToken' in response.json()

        access_token = response.json()['accessToken']
        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Нельзя авторизоваться с неверным логином или паролем")
    @pytest.mark.parametrize(
        'wrong_data_field',
        ('email', 'password')
    )
    def test_cannot_login_with_wrong_data_field(self, payload_user, wrong_data_field):
        with allure.step(f'Обязательное поле: {wrong_data_field} заполнено с ошибкой'):
            response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
            access_token = response.json()['accessToken']
            del payload_user['name']
            payload_user[wrong_data_field] = 'notCorrectData'
            response = requests.post(f'{URL}{ENDPOINT_LOGIN}', json=payload_user)

            assert response.status_code == 401
            assert response.json()['message'] == MESSAGE_INCORRECT_USER_DATA

            requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})
