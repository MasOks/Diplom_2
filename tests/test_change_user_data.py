import allure
import pytest
import requests
from config import URL, ENDPOINT_REGISTER, ENDPOINT_USER
from helpers import MESSAGE_SHOULD_BE_AUTHORISED


class TestPatchUser:

    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize(
        'changed_field',
        ('email', 'name')
    )
    def test_change_user_data_with_authorization(self, payload_user, changed_field):
        with allure.step(f'Изменение данных поля: {changed_field}'):
            response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
            access_token = response.json()['accessToken']
            del payload_user['password']
            payload_user[changed_field] = 'newchangeddata'
            response = requests.patch(
                f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token}, json=payload_user
            )

            assert response.status_code == 200
            assert response.json()['success'] is True
            assert response.json()['user'][f'{changed_field}'] == 'newchangeddata'

            requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Запрос изменения данных пользователя без авторизации")
    @pytest.mark.parametrize(
        'changed_field',
        ('email', 'name')
    )
    def test_impossible_change_user_data_without_authorization(self, payload_user, changed_field):
        with allure.step(f'Изменение данных поля: {changed_field}'):
            response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
            access_token = response.json()['accessToken']
            del payload_user['password']
            payload_user[changed_field] = 'newchangeddata'
            response = requests.patch(f'{URL}{ENDPOINT_USER}', json=payload_user)

            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == MESSAGE_SHOULD_BE_AUTHORISED

            requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})
