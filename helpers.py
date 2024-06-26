import allure
import requests
from faker import Faker
from config import URL, ENDPOINT_INGREDIENTS


MESSAGE_BAD_ORDER = 'Ingredient ids must be provided'
MESSAGE_INCORRECT_ORDER = 'One or more ids provided are incorrect'
MESSAGE_USER_EXISTS = 'User already exists'
MESSAGE_NOT_ENOUGH_USER_DATA = 'Email, password and name are required fields'
MESSAGE_INCORRECT_USER_DATA = 'email or password are incorrect'
MESSAGE_SHOULD_BE_AUTHORISED = 'You should be authorised'


def create_user_data():
    with allure.step('Создаём данные пользователя'):
        fake = Faker(locale='ru_RU')
        user_data = {
            "email": fake.email(),
            "password": fake.password(length=9),
            "name": fake.name()
        }
        return user_data


def create_order_data():
    with allure.step('Создаём список ингредиентов для заказа'):
        response = requests.get(f'{URL}{ENDPOINT_INGREDIENTS}')
        list_hash_ing = [
            response.json()['data'][0]['_id'],
            response.json()['data'][2]['_id'],
            response.json()['data'][9]['_id']
        ]
        order_data = {
            "ingredients": list_hash_ing
        }
        return order_data


def create_order_with_invalid_hash():
    with allure.step('Создаём список ингредиентов c невалидными хэшами'):
        order_data = {
            "ingredients": ["a1c0c5a71d1f82001bdaa", "b1c0c5a71d1f82001bdaaabbbbb"]
        }
        return order_data


def create_order_with_non_existent_hash():
    with allure.step('Создаём список ингредиентов с несуществующими хэшами'):
        order_data = {
            "ingredients": ["a1c0c5a71d1f82001bdaaaaa", "b1c0c5a71d1f82001bdaaabb"]
        }
        return order_data
