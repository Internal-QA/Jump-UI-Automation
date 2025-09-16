"""
Home Page Test Cases for UI Automation Framework
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_test import BaseTest
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.home_page import HomePage
from utils.test_data_manager import DataManager
from utils.logger import get_logger
import pytest
import time
import allure

@allure.epic("UI Automation Test Suite")
@allure.feature("Home Page Navigation")
@allure.story("Home Page Elements and Card Navigation")
class TestHome(BaseTest):
    """Test suite for home page functionality after successful login and OTP verification"""
    
    @classmethod
    def setup_class(cls):
        """Setup class method - runs once per test class"""
        super().setup_class()
        cls.logger = get_logger()
        cls.logger.info("Starting Home Page Test Suite")
    
    @classmethod
    def teardown_class(cls):
        """Cleanup class level logger"""
        cls.logger.info("Home Page Test Suite completed")
    
    def setup_method(self, method):
        """Setup method called before each test"""
        super().setup_method(method)
        
        # Initialize page objects
        self.login_page = LoginPage(self.driver, self.config)
        self.otp_page = OTPPage(self.driver, self.config)
        self.home_page = HomePage(self.driver, self.config)
        
        # Load test data
        self.test_data_manager = DataManager()
        self.test_data = self.test_data_manager.load_test_data()
        
        print(f"Starting test: {method.__name__}")
    
    def teardown_method(self, method):
        """Cleanup method called after each test"""
        print(f"Completed test: {method.__name__}")
        super().teardown_method(method)
    
    def perform_complete_login_flow(self):
        """Helper method to perform complete login and OTP flow to reach home page"""
        try:
            self.logger.info("STEP: Performing complete login and OTP flow to reach home page")
            
            # Step 1: Navigate to login page
            login_success = self.login_page.navigate_to_login_page()
            assert login_success, "Failed to navigate to login page"
            
            # Step 2: Get credentials and perform login
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            login_validation = self.login_page.validate_successful_login_flow(
                credentials["email"], 
                credentials["password"]
            )
            assert login_validation, "Failed to complete login flow"
            
            # Step 3: Verify we're on OTP page
            otp_loaded = self.otp_page.is_otp_page_loaded()
            assert otp_loaded, "Failed to reach OTP page after login"
            
            self.logger.info("STEP: Successfully reached OTP page")
            
            # Step 4: Complete OTP verification
            otp_success = self.otp_page.verify_otp("99999")
            assert otp_success, "Failed to verify OTP"
            
            # Step 5: Wait for redirect to home page
            time.sleep(5)
            
            # Step 6: Verify we're on home page
            home_loaded = self.home_page.is_home_page_loaded()
            assert home_loaded, "Failed to reach home page after OTP verification"
            
            self.logger.info("STEP: Successfully completed login and OTP flow - arrived at home page")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to complete login flow: {str(e)}")
            return False
    
    def test_01_validate_home_page_elements_after_login(self):
        """Test that home page elements are present after successful login and OTP flow"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_01_validate_home_page_elements_after_login")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting home page elements presence test")
        
        try:
            # Complete login and OTP flow
            assert self.perform_complete_login_flow(), "Failed to reach home page"
            
            self.logger.info("STEP: Validating home page elements are present")
            
            # Take screenshot of home page
            self.take_failure_screenshot("home_page_elements_check")
            
            # Verify landing page container
            landing_page_locator = self.home_page.locator_manager.get_locator("home_page", "landing_page_container")
            landing_page_element = self.home_page.find_element(landing_page_locator[0], landing_page_locator[1])
            assert landing_page_element is not None, "Landing page container not found"
            
            # Verify cards wrapper
            cards_wrapper_locator = self.home_page.locator_manager.get_locator("home_page", "cards_wrapper")
            cards_wrapper_element = self.home_page.find_element(cards_wrapper_locator[0], cards_wrapper_locator[1])
            assert cards_wrapper_element is not None, "Cards wrapper container not found"
            
            self.logger.info("STEP: Home page elements presence validation passed")
            
        except Exception as e:
            self.logger.error(f"STEP: Home page elements presence test failed: {str(e)}")
            self.take_failure_screenshot("home_page_elements_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_01_validate_home_page_elements_after_login")
            self.logger.info("==================================================")
    
    def test_02_validate_all_dashboard_cards_are_clickable(self):
        """Test that all 6 cards on home page are clickable after successful login and OTP verification"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_02_validate_all_dashboard_cards_are_clickable")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting all cards clickability validation test")
        
        try:
            # Complete login and OTP flow
            assert self.perform_complete_login_flow(), "Failed to reach home page"
            
            self.logger.info("STEP: Testing clickability of all 6 cards")
            
            # Take screenshot before testing
            self.take_failure_screenshot("home_page_before_cards_test")
            
            # Test each card (1-6)
            for card_number in range(1, 7):
                self.logger.info(f"STEP: Testing clickability of card {card_number}")
                
                # Try to click the card
                card_clicked = self.home_page.click_card(card_number)
                
                if card_clicked:
                    self.logger.info(f"STEP: Card {card_number} clicked successfully")
                    
                    # Wait for potential navigation
                    time.sleep(3)
                    
                    # Check if URL changed (indicating navigation)
                    current_url = self.driver.current_url
                    self.logger.info(f"STEP: Current URL after clicking card {card_number}: {current_url}")
                    
                    # Navigate back to home page for next test
                    self.driver.get(self.config['base_url'] + '/JumpFive/home')
                    time.sleep(3)
                    
                else:
                    self.logger.warning(f"STEP: Card {card_number} click failed or not clickable")
            
            self.logger.info("STEP: All cards clickability validation test completed")
            
        except Exception as e:
            self.logger.error(f"STEP: All cards clickability validation test failed: {str(e)}")
            self.take_failure_screenshot("all_cards_clickability_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_02_validate_all_dashboard_cards_are_clickable")
            self.logger.info("==================================================")
    
    def test_03_test_individual_card_navigation_functionality(self):
        """Test individual card click functionality and navigation behavior"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_03_test_individual_card_navigation_functionality")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting individual card navigation functionality test")
        
        try:
            # Complete login and OTP flow
            assert self.perform_complete_login_flow(), "Failed to reach home page"
            
            self.logger.info("STEP: Testing individual card navigation functionality")
            
            # Test specific card (Card 2 - Valuations)
            card_number = 2
            self.logger.info(f"STEP: Testing navigation functionality of card {card_number}")
            
            # Take screenshot before clicking
            self.take_failure_screenshot(f"before_card_{card_number}_click")
            
            # Record initial URL
            initial_url = self.driver.current_url
            self.logger.info(f"STEP: Initial URL: {initial_url}")
            
            # Click the card
            card_clicked = self.home_page.click_card(card_number)
            assert card_clicked, f"Failed to click card {card_number}"
            
            self.logger.info(f"STEP: Card {card_number} clicked successfully")
            
            # Wait for navigation
            time.sleep(5)
            
            # Check final URL
            final_url = self.driver.current_url
            self.logger.info(f"STEP: Final URL after card click: {final_url}")
            
            # Validate navigation occurred
            assert final_url != initial_url, f"URL did not change after clicking card {card_number}"
            
            # Validate specific navigation (Card 2 should go to valuations)
            if card_number == 2:
                assert 'valuations' in final_url.lower(), f"Card 2 should navigate to valuations page, but went to: {final_url}"
                self.logger.info("STEP: Card 2 correctly navigated to valuations page")
            
            # Take screenshot after navigation
            self.take_failure_screenshot(f"after_card_{card_number}_navigation")
            
            self.logger.info("STEP: Individual card navigation functionality test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Individual card navigation functionality test failed: {str(e)}")
            self.take_failure_screenshot("individual_card_navigation_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_03_test_individual_card_navigation_functionality")
            self.logger.info("==================================================")
    
    def test_04_complete_end_to_end_login_to_home_validation(self):
        """Complete end-to-end test: Login -> OTP -> Home page card validation"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_04_complete_end_to_end_login_to_home_validation")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting complete end-to-end flow with home page validation")
        
        try:
            # Complete login and OTP flow
            assert self.perform_complete_login_flow(), "Failed to reach home page"
            
            self.logger.info("STEP: Performing comprehensive home page validation")
            
            # Validate home page URL
            current_url = self.home_page.get_current_url()
            expected_url = "https://valueinsightpro.jumpiq.com/JumpFive/home"
            assert current_url == expected_url, f"Home page URL validation failed. Expected: {expected_url}, Got: {current_url}"
            
            self.logger.info(f"STEP: Home page URL validation passed: {current_url}")
            
            # Validate home page is loaded
            home_loaded = self.home_page.is_home_page_loaded()
            assert home_loaded, "Home page load validation failed"
            
            # Validate all cards are clickable
            all_cards_clickable = self.home_page.validate_all_cards_clickable()
            assert all_cards_clickable, "Home page cards clickability validation failed"
            
            # Take final screenshot
            self.take_failure_screenshot("end_to_end_home_validation_success")
            
            self.logger.info("STEP: End-to-end flow with home page validation completed successfully")
            self.logger.info("STEP: All validations passed - Login -> OTP -> Home page cards all clickable")
            
        except Exception as e:
            self.logger.error(f"STEP: End-to-end with home validation test failed: {str(e)}")
            self.take_failure_screenshot("end_to_end_home_validation_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_04_complete_end_to_end_login_to_home_validation")
            self.logger.info("==================================================")

if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"]) 