"""
Optimized Base Test Class for Fast Execution
Reduces test time from hours to minutes
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import yaml
import os
from utils.logger import get_logger
from optimized_config import *

class OptimizedBaseTest:
    """Optimized base test class with session reuse and fast execution"""
    
    # Class-level shared resources
    _shared_driver = None
    _logged_in = False
    _session_cookies = None
    _last_login_time = None
    
    @classmethod
    def setup_class(cls):
        """Setup once per test class - creates shared browser session"""
        cls.logger = get_logger()
        cls.logger.info("Setting up optimized test session")
        
        # Load config once
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            cls.config = yaml.safe_load(file)
        
        # Create optimized driver
        cls._shared_driver = cls._create_optimized_driver()
        
    @classmethod
    def _create_optimized_driver(cls):
        """Create optimized Chrome driver for fast execution"""
        options = Options()
        
        # Add performance options
        for option in CHROME_OPTIONS:
            options.add_argument(option)
        
        # Additional performance settings
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        
        # Set optimized timeouts
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @classmethod
    def teardown_class(cls):
        """Cleanup shared resources"""
        if cls._shared_driver:
            cls._shared_driver.quit()
            cls._shared_driver = None
    
    def setup_method(self, method):
        """Fast setup for each test method"""
        self.driver = self._shared_driver
        self.start_time = time.time()
        
        # Fast login if not already logged in
        if not self._logged_in or self._need_fresh_login():
            self._fast_login()
    
    def teardown_method(self, method):
        """Fast cleanup after each test"""
        execution_time = time.time() - self.start_time
        self.logger.info(f"Test {method.__name__} completed in {execution_time:.2f} seconds")
        
        # Only take screenshot on failure if enabled
        if SCREENSHOTS_ON_FAILURE_ONLY and hasattr(self, '_test_failed') and self._test_failed:
            self._fast_screenshot(method.__name__)
    
    def _need_fresh_login(self):
        """Check if we need a fresh login (every 30 minutes)"""
        if not self._last_login_time:
            return True
        return (time.time() - self._last_login_time) > 1800  # 30 minutes
    
    def _fast_login(self):
        """Optimized login that reuses session when possible"""
        try:
            if REUSE_BROWSER_SESSION and self._session_cookies:
                # Try to reuse existing session
                self.driver.get(self.config['base_url'])
                for cookie in self._session_cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                
                # Check if still logged in
                if self._is_logged_in():
                    self.logger.info("Reusing existing login session")
                    return True
            
            # Perform fast login
            self.logger.info("Performing optimized login")
            
            # Navigate to login
            self.driver.get(f"{self.config['base_url']}/auth/login")
            
            # Fast element interactions with reduced waits
            wait = WebDriverWait(self.driver, ELEMENT_WAIT_TIMEOUT)
            
            # Email field
            email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
            email_field.clear()
            email_field.send_keys(self.config['credentials']['valid_user']['email'])
            
            # Password field  
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.config['credentials']['valid_user']['password'])
            
            # Terms checkbox
            terms_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not terms_checkbox.is_selected():
                terms_checkbox.click()
            
            # Submit
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            submit_button.click()
            
            # Wait for OTP page with reduced timeout
            wait.until(EC.url_contains("otp"))
            
            # Fast OTP entry
            otp_field = wait.until(EC.element_to_be_clickable((By.NAME, "otp")))
            otp_field.send_keys("99999")
            
            verify_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
            verify_button.click()
            
            # Wait for home page
            wait.until(EC.url_contains("home"))
            
            # Save session cookies
            if REUSE_BROWSER_SESSION:
                self._session_cookies = self.driver.get_cookies()
                self._last_login_time = time.time()
            
            self._logged_in = True
            self.logger.info("Fast login completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Fast login failed: {str(e)}")
            return False
    
    def _is_logged_in(self):
        """Quick check if user is logged in"""
        try:
            current_url = self.driver.current_url
            return 'home' in current_url.lower() or 'dashboard' in current_url.lower()
        except:
            return False
    
    def _fast_screenshot(self, test_name):
        """Take optimized screenshot on failure"""
        try:
            timestamp = int(time.time())
            filename = f"FAILED_{test_name}_{timestamp}.png"
            filepath = os.path.join("screenshots", filename)
            self.driver.save_screenshot(filepath)
        except Exception as e:
            self.logger.warning(f"Screenshot failed: {str(e)}")
    
    def fast_wait_for_element(self, by, value, timeout=ELEMENT_WAIT_TIMEOUT):
        """Optimized element wait with reduced timeout"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            self.logger.warning(f"Element not found: {by}={value}")
            return None
    
    def fast_click(self, by, value):
        """Fast click with minimal wait"""
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except:
            return False
    
    def fast_navigate(self, url_suffix):
        """Fast navigation without unnecessary waits"""
        full_url = f"{self.config['base_url']}{url_suffix}"
        self.driver.get(full_url)
        # Minimal wait for page load
        time.sleep(0.5)
        return True
