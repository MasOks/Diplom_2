import allure
import requests
from config import URL, ENDPOINT_ORDERS, ENDPOINT_REGISTER, ENDPOINT_LOGIN, ENDPOINT_USER
from helpers import MESSAGE_SHOULD_BE_AUTHORISED


class TestGetOrder:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_from_authorized_user(self, payload_user):
        requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        del payload_user['name']
        response = requests.post(f'{URL}{ENDPOINT_LOGIN}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.get(f'{URL}{ENDPOINT_ORDERS}', headers={'Authorization': access_token})

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'orders' in response.json()

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Запрос получения заказов без авторизации пользователя")
    def test_get_orders_without_authorization_user(self, payload_user):
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.get(f'{URL}{ENDPOINT_ORDERS}')

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == MESSAGE_SHOULD_BE_AUTHORISED

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})
