from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from utils.browser import Browser

class SeleniumBase(object):
    """This Base class is serving basic attributes for every single page inherited from Page class"""
    def __init__(self, driver=None):
        if driver:
            self.driver = driver
        else:
            self.driver = Browser(firefox=True).driver
        self.timeout = 30

    def find_element_by_Locator(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements_by_Locator(self, *locator):
        return self.driver.find_elements(*locator)
    
    def get_element_by_xpath(self, xpath):
        """Returns the element for the xpath given"""
        return self.driver.find_element_by_xpath(xpath)
    
    def get_element_by_id(self, id):
        """Returns the element for the id given"""
        return self.driver.find_element_by_id(id)

    def get_list_of_elements_by_xpath(self, xpath):
        """Returns the list of elements for the xpath given"""
        return self.driver.find_elements_by_xpath(xpath)
    
    def get_element_by_attribute_tag(self, attribute, tag):
        elements = self.driver.find_elements_by_tag_name(tag)
        for element in elements:
            if element.get_attribute(attribute):
                return element
        return None

    def get_text_by_xpath(self, xpath):
        element = self.get_element_by_xpath(xpath)
        return element.text

    def go_to_url(self, url):
        """Navigate to the URL given"""
        try:
            self.driver.get(url)
        except TimeoutException:
            self.refreshPage()

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def hover(self, *locator):
        element = self.find_element_by_Locator(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def wait_for_element_by_ID(self, id):
        """This function will wait for an element to appear on the page before progressing in the script - search for element by ID"""
        try:
         WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.ID,id)), message='Could not find ID')
        finally:
            pass

    def wait_for_element_by_XPATH(self, xpath):
        """This function will wait for an element to appear on the page before progressing in the script - search for element by Xpath"""
        try:
         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,xpath)), message='Could not find xpath')
        finally:
         pass

    def wait_for_element_by_NAME(self, name):
        """This function will wait for an element to appear on the page before progressing in the script - search for element by Name"""
        try:
         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME,name)), message='Could not find name')
        finally:
         pass

    def wait_for_element_by_CLASS_NAME(self, className):
        """This function will wait for an element to appear on the page before progressing in the script - search for element by Class_Name"""
        try:
         WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME,className)), message='Could not find Class Name')
        finally:
         pass

    def wait_for_element_by_Locator(self, *locator):
        """This function will wait for an element to appear on the page before progressing in the script - search for element by Xpath"""
        try:
         WebDriverWait(self.driver,8).until(EC.presence_of_element_located(locator), message='Could nof find Locator')
        finally:
         pass

    def sendKeys_by_ID(self, text ,id):
        """This function will send a string to the assigned locator"""
        if isinstance(text, str):
         element = self.driver.find_element(By.ID, id)
         element.send_keys(text)
        else:
         raise TypeError(text + " is not a string!")

    def sendKeys_by_xpath(self, text, xpath):
        """This function will send a string to the assigned xpath"""
        if isinstance(text, str):
            element = self.driver.find_element(By.XPATH, xpath)
            element.send_keys(text)
        else:
            raise TypeError(text + " is not a string!")

    def click_by_Locator(self, *locator):
        """This function will click the link/button by the locator given"""
        try:
            self.find_element_by_Locator(*locator).click()
        except:
            assert "Could not click locator"

    def click_by_XPATH(self, xpath):
        """This function will click the link/button by the xpath given"""
        try:
            self.driver.find_element(By.XPATH, xpath).click()
        except:
            assert "Could not click xpath"

    def click_by_Name(self, name):
        """This function will click the link/button by the Name given"""
        try:
            self.driver.find_element(By.NAME, name).click()
        except:
            assert "Could not click name: " + name

    def click_by_ID(self, id):
        """This function will click the link/button by the xpath given"""
        try:
            self.driver.find_element(By.ID, id).click()
        except:
            assert "Could not click name: " + id

    def click_by_PLinkText(self, PLink):
        """This function will click on a link by partial text"""
        driver = self.driver
        element = driver.find_element_by_partial_link_text(PLink)
        try:
            element.click()
        except:
            assert "Could not click PLink"

    def click_action_by_xpath(self, xpath):
        """ACtion click as back up if normal click doesn't work
            Argument - Xpath"""
        button = self.driver.find_element_by_xpath(xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(button).click().perform()


    def click_action_by_locator(self, *locator):
        """Action click as back up if normal click doesn't work
        Argument - Locator"""
        button = self.find_element_by_Locator(*locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(button).click().perform()


    def click_action_by_id(self, element_id):
        """Action click as back up if normal click doesn't work
        Argument - Element ID"""
        button = self.driver.find_element_by_id(element_id)
        actions = ActionChains(self.driver)
        actions.move_to_element(button).click().perform()

    def wait_for(self, sec):
        """This function will implictly wait on the page for the given time, in seconds"""
        driver = self.driver
        driver.implicitly_wait(sec)

    def sleep_for(self, sec):
        """Sleep for given time (sec)"""
        time.sleep(sec)

    def clear_field_by_id(self, element_id):
        """This function will clear the text field for the given element. Grab element by ID."""
        driver = self.driver
        element = driver.find_element(By.ID, element_id)
        element.clear()

    def clear_field_by_xpath(self,xpath):
        """This function will clear the text field for the given element. Grab element by Xpath."""
        driver = self.driver
        element = driver.find_element(By.XPATH, xpath)
        element.clear()

    def clear_field_by_name(self,name):
        """This function will clear the text field for the given element. Grab element by name."""
        driver = self.driver
        element = driver.find_element(By.NAME, name)
        element.clear()
    
    def refreshPage(self):
        """Refresh the page"""
        self.driver.get(self.get_url())

    def get_last_chars_of_url(self, x_characters):
        """Returns the last X characters of the URL"""
        url = self.get_url()
        chopped_url = url[-x_characters:]
        return chopped_url

    def find_between_strings(self,string,first,last):
        try:
            start = string.index(first) + len(first)
            end = string.index(last, start)
            return string[start:end]
        except ValueError:
            return("Couldn't find string between given characters")
    
    def verify_text_by_XPATH(self, xpath, expected_text):
        element = self.get_element_by_xpath(xpath)
        if element.text == expected_text:
            return True
        else:
            raise AssertionError("Element Text: " + element.text + " does not equal expected text.")
    
    def verify_text_by_id(self, element_id, expected_text):
        element = self.get_element_by_id(element_id)
        if element.text == expected_text:
            return True
        else:
            raise AssertionError("Element Text: " + element.text + " does not equal expected text.")

    def verify_text_contains_by_XPATH(self, xpath, expected_text):
        element = self.get_element_by_xpath(xpath)
        if expected_text in element.text:
            return True
        else:
            raise AssertionError("Element Text: " + element.text + " does not equal expected text.")
    
    def verify_text_contains_by_id(self, element_id, expected_text):
        element = self.get_element_by_id(element_id)
        if expected_text in element.text:
            return True
        else:
            raise AssertionError("Element Text: " + element.text + " does not equal expected text.")
    
    def __del__(self):
        self.driver.close()