"""
Locator Manager utility for loading XPath selectors from configuration files.
This replaces the complex Python locator classes with a simple config-based approach.
"""

import yaml
import os
from selenium.webdriver.common.by import By


class LocatorManager:
    """Manages XPath locators from YAML configuration file"""
    
    def __init__(self, config_file_path=None):
        """Initialize LocatorManager with config file path"""
        if config_file_path is None:
            # Default to locators.yaml in config directory
            self.config_file_path = os.path.join(
                os.path.dirname(__file__), '..', 'config', 'locators.yaml'
            )
        else:
            self.config_file_path = config_file_path
        
        self.locators = self.load_locators()
    
    def load_locators(self):
        """Load locators from YAML configuration file"""
        try:
            with open(self.config_file_path, 'r') as file:
                locators = yaml.safe_load(file)
                print(f"Locators loaded from: {self.config_file_path}")
                return locators
        except FileNotFoundError:
            print(f"Locators config file not found at: {self.config_file_path}")
            return self.get_default_locators()
        except Exception as e:
            print(f"Error loading locators: {str(e)}")
            return self.get_default_locators()
    
    def get_default_locators(self):
        """Return default locators if config file is not found"""
        return {
            'login_page': {
                'email_field': "//input[@id='company-email']",
                'password_field': "//span[@class='ant-input-affix-wrapper css-bixahu ant-input-outlined ant-input-password input']//input[@type='password']",
                'terms_checkbox': "//input[@type='checkbox']",
                'sign_in_button': "//button[normalize-space()='Sign In']",
                'general_error': "//div[contains(@class, 'error')]",
                'loading_indicator': "//div[contains(@class, 'loading')]"
            }
        }
    
    def get_locator(self, page, element_name):
        """
        Get a specific locator for a page element
        
        Args:
            page (str): Page name (e.g., 'login_page', 'otp_page')
            element_name (str): Element name (e.g., 'email_field', 'sign_in_button')
        
        Returns:
            tuple: (By.XPATH, xpath_string) ready for Selenium
        """
        try:
            xpath = self.locators[page][element_name]
            return (By.XPATH, xpath)
        except KeyError as e:
            print(f"Locator not found: {page}.{element_name} - {str(e)}")
            return None
    
    def get_xpath(self, page, element_name):
        """
        Get just the XPath string for a page element
        
        Args:
            page (str): Page name
            element_name (str): Element name
        
        Returns:
            str: XPath string
        """
        try:
            return self.locators[page][element_name]
        except KeyError as e:
            print(f"XPath not found: {page}.{element_name} - {str(e)}")
            return None
    
    def get_page_locators(self, page):
        """
        Get all locators for a specific page
        
        Args:
            page (str): Page name
        
        Returns:
            dict: Dictionary of all locators for the page
        """
        try:
            return self.locators[page]
        except KeyError as e:
            print(f"Page not found: {page} - {str(e)}")
            return {}
    
    def get_text_message(self, page, message_key):
        """
        Get expected text message for validation
        
        Args:
            page (str): Page name
            message_key (str): Message key
        
        Returns:
            str: Expected text message
        """
        try:
            return self.locators['text_messages'][page][message_key]
        except KeyError as e:
            print(f"Text message not found: {page}.{message_key} - {str(e)}")
            return ""
    
    def add_locator(self, page, element_name, xpath):
        """
        Add a new locator dynamically (in memory only)
        
        Args:
            page (str): Page name
            element_name (str): Element name
            xpath (str): XPath string
        """
        if page not in self.locators:
            self.locators[page] = {}
        
        self.locators[page][element_name] = xpath
        print(f"Added locator: {page}.{element_name} = {xpath}")
    
    def update_locator(self, page, element_name, new_xpath):
        """
        Update an existing locator (in memory only)
        
        Args:
            page (str): Page name
            element_name (str): Element name
            new_xpath (str): New XPath string
        """
        if page in self.locators and element_name in self.locators[page]:
            old_xpath = self.locators[page][element_name]
            self.locators[page][element_name] = new_xpath
            print(f"Updated locator: {page}.{element_name}")
            print(f"  Old: {old_xpath}")
            print(f"  New: {new_xpath}")
        else:
            print(f"Locator not found for update: {page}.{element_name}")
    
    def list_page_elements(self, page):
        """
        List all available elements for a page
        
        Args:
            page (str): Page name
        
        Returns:
            list: List of element names
        """
        try:
            return list(self.locators[page].keys())
        except KeyError:
            print(f"Page not found: {page}")
            return []
    
    def list_all_pages(self):
        """
        List all available pages
        
        Returns:
            list: List of page names
        """
        # Exclude 'text_messages' and 'common' from pages list
        return [page for page in self.locators.keys() 
                if page not in ['text_messages', 'common']]
    
    def save_locators(self, output_file=None):
        """
        Save current locators to YAML file
        
        Args:
            output_file (str): Output file path (optional)
        """
        output_path = output_file or self.config_file_path
        
        try:
            with open(output_path, 'w') as file:
                yaml.dump(self.locators, file, default_flow_style=False, indent=2)
            print(f"Locators saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving locators: {str(e)}")
            return False
    
    def validate_locator(self, page, element_name):
        """
        Validate if a locator exists
        
        Args:
            page (str): Page name
            element_name (str): Element name
        
        Returns:
            bool: True if locator exists, False otherwise
        """
        return (page in self.locators and 
                element_name in self.locators[page] and 
                self.locators[page][element_name] is not None)


# Global instance for easy access
locator_manager = None

def get_locator_manager(config_file=None):
    """Get global locator manager instance"""
    global locator_manager
    if locator_manager is None:
        locator_manager = LocatorManager(config_file)
    return locator_manager 