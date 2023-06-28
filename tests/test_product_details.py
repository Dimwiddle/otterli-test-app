import random
import pytest
from api.api_hub import ProductAPI, ProductDetailsAPI

SAMPE_LIST = [3532, 1971, 2037, 5583, 1583, 2749, 5518, 5962, 4232, 4299]

@pytest.fixture(scope="module")
def product_sample():
    p_client = ProductAPI()
    # sample_list = []
    # for r in range(10):
    #     sample_list.append(random.randint(100, 6000))
    sample_products = p_client.get_selected_products(SAMPE_LIST)
    return sample_products 

@pytest.mark.product_details
def test_name(product_sample):
    """Verify the vendor products have a name."""
    client = ProductDetailsAPI()
    failed = [] 
    for product in product_sample:
        details = client.get_product_details(product['id'])
        if not details['name']:
            failed.append(product)
    assert not failed, f"Products didn't have a name {failed}"

@pytest.mark.product_details
def test_categories(product_sample):
    """Verify the vendor products have categories."""
    client = ProductDetailsAPI()
    failed = [] 
    for product in product_sample:
        details = client.get_product_details(product['id'])
        if not details['categories']:
            failed.append(details['name'])
    assert not failed, f"Products didn't have a categories {failed}"

@pytest.mark.xfail
@pytest.mark.product_details
def test_units(product_sample):
    """Verify the vendor products have all the required details."""
    client = ProductDetailsAPI()
    failed_units = []
    for product in product_sample:
        details = client.get_product_details(product['id'])
        if not details['units']:
            failed_units.append(product)
    assert not failed_units, f"Products didn't have any units"

@pytest.mark.product_details
def test_image_url(product_sample):
    """Verify the vendor products have all the required images."""
    client = ProductDetailsAPI()
    failed_image = [] 
    for product in product_sample:
        details = client.get_product_details(product['id'])
        if not details['image_url']:
            failed_image.append(product)
    assert not failed_image, f"Products didn't have an image {failed_image}"

@pytest.mark.xfail(reason="https://otterli.atlassian.net/browse/OTR-310")
@pytest.mark.product_details
def test_vendor_url(product_sample):
    """Verify the vendor product has a vendor and it's URL"""
    client = ProductDetailsAPI()
    failed_vendor = []
    failed_url = []
    for product in product_sample:
        details = client.get_product_details(product['id'])
        if not details['vendors']:
            failed_vendor.append(product)
            continue
        for v in details['vendors']:
            if not v['url']:
                failed_url.append(product)
    assert not failed_vendor, f"Products didn't have any vendor: {failed_vendor}"
    assert not failed_url, f"Products didn't have any URL for the product's vendor: {failed_url}"

@pytest.mark.product_details
def test_product_price(product_sample):
    """Verify that the product details contains the price field"""
    client = ProductDetailsAPI()
    failed_vendor = []
    failed_price = []
    for product in product_sample:
        details = client.get_product_details(product['id'])
        if not details['vendors']:
            failed_vendor.append(product)
            continue
        if not details['price']['avg_price']:
            failed_price.append(product)
    assert not failed_vendor, f"Products didn't have any vendors: {failed_vendor}"
    assert not failed_price, f"Products didn't have any price for the product's details: {failed_price}"

      