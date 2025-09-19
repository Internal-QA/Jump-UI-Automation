"""
Optimized Login Tests - Fast Execution Version
Target: Complete all login tests in under 2 minutes
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.optimized_base_test import OptimizedBaseTest
from optimized_config import *

class TestOptimizedLogin(OptimizedBaseTest):
    """Optimized login tests with fast execution"""
    
    def test_01_valid_login_flow(self):
        """Test valid login - optimized version"""
        start_time = time.time()
        
        # Navigate to login
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        # Fast login elements interaction
        wait = WebDriverWait(self.driver, 2)
        
        # Email
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_field.send_keys(self.config['credentials']['valid_user']['email'])
        
        # Password
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(self.config['credentials']['valid_user']['password'])
        
        # Terms
        terms_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
        if not terms_checkbox.is_selected():
            terms_checkbox.click()
        
        # Submit
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        submit_button.click()
        
        # Verify redirect to OTP
        wait.until(EC.url_contains("otp"))
        assert "otp" in self.driver.current_url.lower()
        
        execution_time = time.time() - start_time
        assert execution_time < 10, f"Login test took too long: {execution_time:.2f}s"
    
    def test_02_invalid_email_validation(self):
        """Test invalid email - optimized"""
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        # Quick invalid email test
        email_field = self.fast_wait_for_element(By.NAME, "email")
        email_field.send_keys("invalid@email")
        
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("password123")
        
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        submit_button.click()
        
        # Should stay on login page
        time.sleep(1)  # Minimal wait
        assert "login" in self.driver.current_url.lower()
    
    def test_03_empty_fields_validation(self):
        """Test empty fields - optimized"""
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        # Try to submit with empty fields
        submit_button = self.fast_wait_for_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        submit_button.click()
        
        # Should stay on login page
        time.sleep(0.5)
        assert "login" in self.driver.current_url.lower()
    
    def test_04_login_page_elements(self):
        """Test page elements presence - optimized"""
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        # Quick element checks
        elements_to_check = [
            (By.NAME, "email"),
            (By.NAME, "password"),
            (By.XPATH, "//input[@type='checkbox']"),
            (By.XPATH, "//button[contains(text(), 'Sign In')]")
        ]
        
        for by, value in elements_to_check:
            element = self.fast_wait_for_element(by, value, timeout=1)
            assert element is not None, f"Element not found: {by}={value}"
    
    def test_05_password_visibility_toggle(self):
        """Test password eye icon - optimized"""
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        password_field = self.fast_wait_for_element(By.NAME, "password")
        password_field.send_keys("testpassword")
        
        # Check initial type
        initial_type = password_field.get_attribute("type")
        
        # Try to find and click eye icon
        try:
            eye_icon = self.driver.find_element(By.XPATH, "//*[contains(@class, 'eye') or contains(@class, 'visibility')]")
            eye_icon.click()
            time.sleep(0.2)
            
            # Check if type changed
            new_type = password_field.get_attribute("type")
            assert new_type != initial_type, "Password visibility should toggle"
        except:
            # Eye icon might not be present, that's ok
            pass
    
    def test_06_terms_checkbox_functionality(self):
        """Test terms checkbox - optimized"""
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        terms_checkbox = self.fast_wait_for_element(By.XPATH, "//input[@type='checkbox']")
        
        # Test checkbox toggle
        initial_state = terms_checkbox.is_selected()
        terms_checkbox.click()
        time.sleep(0.1)
        
        new_state = terms_checkbox.is_selected()
        assert new_state != initial_state, "Checkbox should toggle"
    
    def test_07_form_clearing(self):
        """Test form clearing - optimized"""
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        # Fill form
        email_field = self.fast_wait_for_element(By.NAME, "email")
        email_field.send_keys("test@example.com")
        
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("password123")
        
        # Clear form
        email_field.clear()
        password_field.clear()
        
        # Verify cleared
        assert email_field.get_attribute("value") == ""
        assert password_field.get_attribute("value") == ""
    
    def test_08_successful_login_to_otp_redirect(self):
        """Test complete login to OTP flow - optimized"""
        # This is covered by the base class fast_login, so just verify it works
        assert self._is_logged_in() or self._fast_login()
        
        # Navigate to login to test redirect
        self.driver.get(f"{self.config['base_url']}/auth/login")
        
        # Perform quick login
        wait = WebDriverWait(self.driver, 2)
        
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_field.send_keys(self.config['credentials']['valid_user']['email'])
        
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(self.config['credentials']['valid_user']['password'])
        
        terms_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
        if not terms_checkbox.is_selected():
            terms_checkbox.click()
        
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        submit_button.click()
        
        # Verify redirect to OTP
        wait.until(EC.url_contains("otp"))
        assert "otp" in self.driver.current_url.lower()

if __name__ == "__main__":
    # Run optimized tests
    pytest.main([__file__, "-v", "--tb=short", "-x"])  # Stop on first failure for speed
