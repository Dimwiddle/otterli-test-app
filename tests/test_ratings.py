import random
import pytest
from api.api_hub import RatingsAPI, ProductAPI
from datetime import date


@pytest.fixture(scope="module")
def product_sample():
    p_client = ProductAPI()
    all_products = p_client.get_all_products()
    sample = random.sample(all_products, 1)
    return sample[0]

@pytest.fixture
def client():
    return RatingsAPI()

@pytest.mark.rating
def test_overall_ratings():
    """Verify overall ratings fields for a product"""
    client = RatingsAPI()
    ratings = client.get_rating_by_product(332)
    assert ratings['avg_rating']
    assert ratings['count'] >= 1

@pytest.mark.rating
def test_good_rating_review(client: RatingsAPI, product_sample):
    id = product_sample['id']
    rating = random.randint(3,5)
    review = "I love this!"
    reviewer_ref = "automatedbot323"
    username = "Richbot"
    today = date.today().isoformat()
    r = client.post_rating(rating, id, reviewer_ref, username, review=review)
    assert r['username'] == username
    assert reviewer_ref in r['reviewer_ref']
    assert r['rating'] == rating
    assert r['review'] == review
    assert r['created_date'] == today
    assert r['last_update_date'] == today

@pytest.mark.rating
def test_bad_rating(client: RatingsAPI, product_sample):
    id = product_sample['id']
    rating = random.randint(1,2)
    reviewer_ref = "automatedbot323"
    username = "Richbot"
    error, r = client.post_rating(rating, id, reviewer_ref, username)
    assert error['status'] == 400, f"Status code not as expected: {error['status']}"
    assert r['review'][0] == "Please provide a review for your low rating.", f"Error not as expected: {r}"
    