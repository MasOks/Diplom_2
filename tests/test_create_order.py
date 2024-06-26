import allure
import requests
from config import URL, ENDPOINT_ORDERS, ENDPOINT_REGISTER, ENDPOINT_USER
from helpers import MESSAGE_BAD_ORDER, MESSAGE_INCORRECT_ORDER


class TestPostOrder:

    @allure.title("Создание заказа (с ингредиентами) с авторизацией пользователя")
    def test_create_order_with_ingredients_and_authorization_user(self, payload_user, payload_order):
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.post(f'{URL}{ENDPOINT_ORDERS}', headers={'Authorization': access_token}, json=payload_order)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Запрос на создание заказа (с ингредиентами) без авторизации пользователя")
    def test_create_order_with_ingredients_without_authorization_user(self, payload_user, payload_order):
        """
            Ожидаемый результат (из документации API для Stellar Burgers):
            Только авторизованные пользователи могут делать заказы. Нужно предоставлять токен при
            запросе к серверу в поле Authorization.

            Фактический результат:
            Заказ создается без авторизации пользователя.
        """
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.post(f'{URL}{ENDPOINT_ORDERS}', json=payload_order)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Запрос на создание заказа без ингредиентов с авторизацией пользователя")
    def test_cannot_create_order_without_ingredients(self, payload_user):
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.post(f'{URL}{ENDPOINT_ORDERS}', headers={'Authorization': access_token})

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == MESSAGE_BAD_ORDER

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Запрос на создание заказа с невалидным хешем ингредиентов с авторизацией пользователя")
    def test_cannot_create_order_with_invalid_hash_of_ingredients(self, payload_user, payload_invalid_hash):
        """
            В задании к диплому:
            Проверить создание заказа с неверным хешем ингредиентов.

            В документации API для Stellar Burgers говорится только о невалидном хэше (ожидаемый результат):
            Если в запросе передан невалидный хэш ингредиента (количество символов в хэше не 24), то вернётся
            код ответа 500 Internal Server Error.
        """
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.post(
            f'{URL}{ENDPOINT_ORDERS}', headers={'Authorization': access_token}, json=payload_invalid_hash
        )

        assert response.status_code == 500

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})

    @allure.title("Запрос на создание заказа с несуществующим хешем ингредиента с авторизацией пользователя")
    def test_cannot_create_order_with_non_existent_hash_of_ingredient(self, payload_user, payload_non_existent_hash):
        """
            В задании к диплому:
            Проверить создание заказа с неверным хешем ингредиентов.

            Добавила проверку с несуществующим хешем ингредиента (количество символов в хэше 24, но
            такого хэша нет в списке ингредиентов, полученных по запросу к ручке "/api/ingredients").
        """
        response = requests.post(f'{URL}{ENDPOINT_REGISTER}', json=payload_user)
        access_token = response.json()['accessToken']
        response = requests.post(
            f'{URL}{ENDPOINT_ORDERS}', headers={'Authorization': access_token}, json=payload_non_existent_hash
        )

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == MESSAGE_INCORRECT_ORDER

        requests.delete(f'{URL}{ENDPOINT_USER}', headers={'Authorization': access_token})
