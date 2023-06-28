import pytest
from api.api_hub import RecommendedProductsAPI


@pytest.fixture
def client():
    return RecommendedProductsAPI()

def test_recommended_products(client: RecommendedProductsAPI):
    recommended_product = client.get_recommended_products()
    assert recommended_product, f"Recommended products were not received"
    assert len(recommended_product) == 25, f"Total number of latest products: {len(recommended_product)}"


