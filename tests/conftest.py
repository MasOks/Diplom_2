import pytest
import helpers


@pytest.fixture()
def payload_user():
    return helpers.create_user_data()


@pytest.fixture()
def payload_order():
    return helpers.create_order_data()


@pytest.fixture()
def payload_invalid_hash():
    return helpers.create_order_with_invalid_hash()


@pytest.fixture()
def payload_non_existent_hash():
    return helpers.create_order_with_non_existent_hash()
