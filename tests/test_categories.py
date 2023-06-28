import pytest
from api.api_hub import CategoriesAPI

@pytest.fixture
def client():
    return CategoriesAPI()

@pytest.mark.categories
def test_menu_categories(client: CategoriesAPI):
    categories = client.get_menu_categories()
    icon_svgs = [r['icon_svg'] for r in categories['results']]
    assert len(icon_svgs) == 25, f"Total icon_svg's not as expected (25): {len(icon_svgs)}"
    assert categories['count'] == 25, f"Total menu categories not as expected (25): {categories['count']}"

@pytest.mark.categories
def test_all_categories(client: CategoriesAPI):
    categories = client.get_all_categories()
    assert len(categories) >= 25, f"Total categories not as expected (below 25): {categories['count']}"