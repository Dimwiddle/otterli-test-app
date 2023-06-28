import pytest
from api.api_hub import NewProductsAPI


@pytest.fixture
def client():
    return NewProductsAPI()

def test_latest_products(client: NewProductsAPI):
    latest_products = client.get_latest_products()
    assert latest_products, f"Latest products were not received"
