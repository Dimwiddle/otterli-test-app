import random
import pytest
from api.api_hub import ProductAPI, CategoriesAPI, ProductDetailsAPI
from utils.data_functions import find_duplicates_in_list

SAMPE_LIST = [3532, 1971, 2037, 5583, 1583, 2749, 5518, 5962, 4232, 4299]

@pytest.fixture(scope="module")
def product_sample():
    p_client = ProductAPI()
    sample_list = []
    for r in range(20):
        sample_list.append(random.randint(100, 6000))
    sample_products = p_client.get_selected_products(SAMPE_LIST)
    return sample_products 

#Search test - search for 'chicken skewers'. It's returning duplicates
SEARCH_TERMS = ["Chicken skewers"]
@pytest.mark.products
@pytest.mark.api
def test_duplicate_products():
    """Verify that there are no duplicates in the response"""
    client = ProductAPI()
    for term in SEARCH_TERMS:
        response = client.search_product(term)
        duplicated_ids = find_duplicates_in_list(response, "id")
        assert not duplicated_ids, f"Duplicates were found for {','.join(duplicated_ids)}"


@pytest.mark.api
@pytest.mark.categories
def test_product_categories():
    """Verify that the category search is working as expected"""
    product_client = ProductAPI()
    categories_client = CategoriesAPI()
    all_categories = categories_client.get_all_categories()
    details_client = ProductDetailsAPI()
    for category in random.sample(all_categories, 5) :
        print(f"Checking category {category['name']}...")
        products = product_client.get_products_by_category(category['name'])[:5]
        for product in products:
            details = details_client.get_product_details(product['id'])
            assert category['name'] in details['categories'], f"{category['name']} wasn't found in product ID {details['id']}"
        print(f"Check complete!")

@pytest.mark.api
@pytest.mark.favourites
def test_product_selection(product_sample):
    """Verify that the select filter returns the expected results"""
    product_client = ProductAPI()
    sample_list = []
    for r in range(20):
        sample_list.append(random.randint(100, 6000))
    response = product_client.get_selected_products(select_ids=sample_list)
    for product in response:
        assert product['id'] in sample_list, f"Product {product['id']} was not in selected IDs"
    

def test_product_rating_ordering():
    """Verify that the product ratings ordering is working as expected."""
    product_client = ProductAPI()
    base_query = product_client.base_url
    ordering = ["rating", "-rating"]
    for order in ordering:
        query = product_client.apply_ordering(base_query, order)
        response = product_client.send_query(query)
        results = product_client.return_results(response)
        if not results:
            assert False, f"No ratings found"
        else:
            ratings = [row['reviews']['avg_rating'] for row in results]
            for i in range(0, len(ratings)):
                current_index = i
                next_index = i + 1
                if next_index >= len(ratings):
                    break
                if order == "rating":
                    assert ratings[current_index] <= ratings[next_index], f"{ratings[current_index]} is bigger than {ratings[next_index]}"
                if order == "-rating":
                    assert ratings[current_index] >= ratings[next_index], f"{ratings[current_index]} is smaller than {ratings[next_index]}"


@pytest.mark.xfail(reason="https://otterli.atlassian.net/browse/OTR-311")
@pytest.mark.api
@pytest.mark.price_ordering
def test_product_price_ordering():
    """Verify that the product ratings ordering is working as expected."""
    product_client = ProductAPI()
    
    ordering = ["price", "-price"]
    for order in ordering:
        response = product_client.get_products_by_category("BBQ", ordering=order, return_raw_response=True)
        results = response['results']
        if not results:
            assert False, f"No price found"
        else:
            price = [row['vendors'][0]['price']['price'] for row in results]
            for i in range(0, len(price)):
                current_index = i
                next_index = i + 1
                if next_index >= len(price):
                    break
                if order == "price":
                    assert price[current_index] <= price[next_index], f"{price[current_index]} should be bigger than {price[next_index]}"
                if order == "-price":
                    assert price[current_index] >= price[next_index], f"{price[current_index]} should be smaller than {price[next_index]}"

@pytest.mark.product_search
def test_product_search():
    """Test the searching of different search words."""
    search_terms = ["ice cream", "soda", "crisps"]
    product_client = ProductAPI()

    for term in search_terms:
        response = product_client.search_product(term)
        print(response)