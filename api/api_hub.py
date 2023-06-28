from api.client import Client
from api_settings import get_endpoint

class APIBase(Client):

    @staticmethod
    def apply_filter(current_query, filter)-> str:
        if "?" not in current_query:
            return f"{current_query}?{filter}" 
        else:
         return f"{current_query}&{filter}"
    
    def return_results(self, response, return_raw_response=None):
        if return_raw_response:
            return response
        result = response['results']
        complete = False
        while not complete:
            if response['next']:
                response = self.send_query(response['next'])
                result += response['results']
            else:
                complete = True
        return result

class ProductAPI(APIBase):
    
    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}products/"
    
    def apply_ordering(self,current_query, order_by)-> str:
        """Apply ordering to the search results"""
        ordering = f"ordering={order_by}"
        return self.apply_filter(current_query, ordering)
    
    def apply_selected_products(self,current_query, values: list)-> str:
        """Apply the selected products by ID"""
        values_list = ""
        for value in values:
            values_list += f"{value},"
        selected = f"select={values_list}"
        if "," == selected[-1:]:
            selected = selected[:-1]
        return self.apply_filter(current_query, selected)
    
    def apply_vendors(self, current_query, values: list)-> str:
        """Apply the vendors filter to the current query"""
        values_list = ""
        for value in values:
            values_list += f"{value},"
        vendors = f"vendors={values_list}"
        if "," == vendors[-1:]:
            vendors = vendors[:-1]
        return self.apply_filter(current_query, vendors)
    
    def apply_category(self, current_query, value):
        """Apply ordering to the search results"""
        category = f"category={value}"
        return self.apply_filter(current_query, category)
    
    def search_product(self, search_term, return_raw_response=None):
        """Returns the search result for the given query"""
        url = f"{self.base_url}?search="
        complete = False
        response = self.send_query(f"{url}{search_term}")
        return self.return_results(response, return_raw_response=return_raw_response)
    
    def get_product_by_id(self, id):
        """Returns the product by the ID"""
        return self.send_query(f"{self.base_url}{id}")
    
    def get_products_by_category(self, category, ordering=None, return_raw_response=False):
        """Search for the products with given category parameter"""
        if ordering:
            query = f"{self.base_url}?category={category}"
            query = self.apply_ordering(query, ordering)
            response = self.send_query(query)
        else:
            response = self.send_query(f"{self.base_url}?category={category}")
        return self.return_results(response, return_raw_response=return_raw_response)
    
    def get_all_products(self, return_raw_response=None):
        """Returns all the products"""
        response = self.send_query(self.base_url)
        return self.return_results(response, return_raw_response=return_raw_response)
    
    def get_selected_products(self, select_ids: list, return_raw_response=None):
        """Returns all the selected products by ID"""
        ids = [str(x) for x in select_ids]
        ids = ",".join(ids)
        response = self.send_query(f"{self.base_url}?select={ids}")
        return self.return_results(response, return_raw_response=return_raw_response)


class VendorProductAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}product_vendors/"
    
    def search_vendor_products(self, search_query, return_raw_response=None):
        """Returns the search results for vendor products"""
        url = f"{self.base_url}?search="
        complete = False
        response = self.send_query(f"{url}{search_query}")
        if return_raw_response:
            return response
        result = response['results']
        while not complete:
            if response['next']:
                response = self.send_query(response['next'])
                result += response['results']
            else:
                complete = True
        return result
    
    def get_vendor_product_by_id(self, id):
        """Returns the vendor product by the ID"""
        return self.send_query(f"{self.base_url}{id}")
    
    def get_all_vendor_products(self, return_raw_response=None):
        """Returns all the vendor products"""
        complete = False
        response = self.send_query(self.base_url)
        if return_raw_response:
            return response
        result = response['results']
        while not complete:
            if response['next']:
                response = self.send_query(response['next'])
                result += response['results']
            else:
                complete = True
        return result

class ProductDetailsAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}product_details/"
    
    def get_product_details(self, id):
        return self.send_query(f"{self.base_url}{id}")


class CategoriesAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}categories/"
    
    def get_all_categories(self, raw_response=False):
        r = self.send_query(f"{self.base_url}")
        results = self.return_results(r, return_raw_response=raw_response)
        return results
    
    def get_menu_categories(self):
        url = self.apply_filter(f"{self.base_url}", "icons=True") 
        return self.send_query(url)

 
class RatingsAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}ratings/"
    
    def get_ratings(self):
        return self.send_query(f"{self.base_url}")['results']
    
    def get_rating_by_product(self, product_id):
        url = f"{self.base_url}{product_id}"
        return self.send_query(url)
    
    def post_rating(self, rating, product_id, reviewer_ref, username, review=None):
        url = f"{self.base_url}"
        data = {
                "rating": rating,
                "product": product_id,
                "reviewer_ref":reviewer_ref,
                "review": review,
                "username": username
            }
        return self.post_query(url, data)


class NewProductsAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}latest_products/"
    
    def get_latest_products(self, raw_response=False):
        r = self.send_query(f"{self.base_url}")
        results = self.return_results(r, return_raw_response=raw_response)
        return results


class RecommendedProductsAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.base_url = f"{get_endpoint()}recommended_products/"
    
    def get_recommended_products(self, raw_response=False):
        r = self.send_query(f"{self.base_url}")
        results = self.return_results(r, return_raw_response=raw_response)
        return results

class FeedbackAPI(APIBase):

    def __init__(self):
        super().__init__()
        self.quick_question_url = f"{get_endpoint()}quick_question/"
        self.quick_feedback_url = f"{get_endpoint()}quick_feedback/"
        self.feedback_url = f"{get_endpoint()}feedback"
    
    def get_current_question(self, raw_response=False) -> dict:
        """Returns the current quick question being asked """
        r = self.send_query(self.quick_question_url)
        if raw_response:
            return r
        return self.return_results(r)
    
    def post_question_feedback(self, question: int, answer: str):
        """Send an answer to the current quick question"""
        data = {
            "question": question,
            "feedback": answer
        }
        return self.post_query(self.quick_feedback_url, data)
    
    def post_feedback(self, feedback: dict):
        """Send a feedback form"""
        return self.post_query(self.feedback_url, feedback)
