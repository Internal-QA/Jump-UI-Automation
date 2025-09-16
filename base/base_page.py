from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from datetime import datetime


class BasePage:
    """Base page class containing common methods for all page objects"""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, config['timeouts']['explicit_wait'])
        self.implicit_wait = config['timeouts']['implicit_wait']
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        try:
            self.driver.get(url)
            self.wait_for_page_load()
            return True
        except Exception as e:
            print(f"Error navigating to {url}: {str(e)}")
            return False
    
    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def find_element(self, locator_type, locator_value, timeout=None):
        """Find single element with explicit wait"""
        if timeout is None:
            timeout = self.implicit_wait
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            if locator_type.lower() == "xpath":
                element = wait.until(EC.presence_of_element_located((By.XPATH, locator_value)))
            elif locator_type.lower() == "id":
                element = wait.until(EC.presence_of_element_located((By.ID, locator_value)))
            elif locator_type.lower() == "css":
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locator_value)))
            elif locator_type.lower() == "class":
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, locator_value)))
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            
            return element
        except TimeoutException:
            return None
    
    def find_elements(self, locator_type, locator_value, timeout=None):
        """Find multiple elements with explicit wait"""
        if timeout is None:
            timeout = self.implicit_wait
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            if locator_type.lower() == "xpath":
                elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, locator_value)))
            elif locator_type.lower() == "id":
                elements = wait.until(EC.presence_of_all_elements_located((By.ID, locator_value)))
            elif locator_type.lower() == "css":
                elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locator_value)))
            elif locator_type.lower() == "class":
                elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, locator_value)))
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            
            return elements
        except TimeoutException:
            return []
    
    def click_element(self, locator_type, locator_value, timeout=None):
        """Click on an element with explicit wait"""
        element = self.find_element(locator_type, locator_value, timeout)
        if element:
            try:
                # Wait for element to be clickable
                wait = WebDriverWait(self.driver, timeout or self.implicit_wait)
                if locator_type.lower() == "xpath":
                    clickable_element = wait.until(EC.element_to_be_clickable((By.XPATH, locator_value)))
                elif locator_type.lower() == "id":
                    clickable_element = wait.until(EC.element_to_be_clickable((By.ID, locator_value)))
                elif locator_type.lower() == "css":
                    clickable_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator_value)))
                elif locator_type.lower() == "class":
                    clickable_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, locator_value)))
                
                clickable_element.click()
                return True
            except Exception as e:
                print(f"Error clicking element: {str(e)}")
                return False
        return False
    
    def enter_text(self, locator_type, locator_value, text, clear_first=True, timeout=None):
        """Enter text into an input field"""
        element = self.find_element(locator_type, locator_value, timeout)
        if element:
            try:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                return True
            except Exception as e:
                print(f"Error entering text: {str(e)}")
                return False
        return False
    
    def get_text(self, locator_type, locator_value, timeout=None):
        """Get text from an element"""
        element = self.find_element(locator_type, locator_value, timeout)
        if element:
            try:
                return element.text
            except Exception as e:
                print(f"Error getting text: {str(e)}")
                return None
        return None
    
    def is_element_present(self, locator_type, locator_value, timeout=5):
        """Check if element is present on the page"""
        element = self.find_element(locator_type, locator_value, timeout)
        return element is not None
    
    def is_element_visible(self, locator_type, locator_value, timeout=5):
        """Check if element is visible on the page"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            if locator_type.lower() == "xpath":
                element = wait.until(EC.visibility_of_element_located((By.XPATH, locator_value)))
            elif locator_type.lower() == "id":
                element = wait.until(EC.visibility_of_element_located((By.ID, locator_value)))
            elif locator_type.lower() == "css":
                element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator_value)))
            elif locator_type.lower() == "class":
                element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, locator_value)))
            
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator_type, locator_value, timeout=None):
        """Scroll to an element"""
        element = self.find_element(locator_type, locator_value, timeout)
        if element:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)  # Wait for scroll to complete
                return True
            except Exception as e:
                print(f"Error scrolling to element: {str(e)}")
                return False
        return False
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot and save it with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = self.config['test_data']['screenshot_path']
        
        # Create directory if it doesn't exist
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
        try:
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")
            return None
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self):
        """Navigate back in browser history"""
        self.driver.back()
        self.wait_for_page_load()
    
    def switch_to_window(self, window_handle):
        """Switch to a specific browser window"""
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self):
        """Get all browser window handles"""
        return self.driver.window_handles 