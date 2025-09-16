"""
OTP Verification Test Cases for UI Automation Framework
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_test import BaseTest
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from utils.test_data_manager import DataManager
from utils.logger import get_logger
import pytest
import time
import allure

@allure.epic("UI Automation Test Suite")
@allure.feature("OTP Verification")
@allure.story("OTP Page Functionality and Verification Flow")
class TestOTP(BaseTest):
    """Test class for OTP verification functionality"""
    
    @classmethod
    def setup_class(cls):
        """Setup class method - runs once per test class"""
        super().setup_class()
        cls.logger = get_logger()
        cls.logger.info("Starting OTP Test Suite")
    
    @classmethod
    def teardown_class(cls):
        """Teardown class method - runs once per test class"""
        cls.logger.info("OTP Test Suite completed")
        super().teardown_class() if hasattr(super(), 'teardown_class') else None
    
    def setup_method(self, method):
        """Setup method called before each test"""
        super().setup_method(method)
        
        # Initialize page objects
        self.login_page = LoginPage(self.driver, self.config)
        self.otp_page = OTPPage(self.driver, self.config)
        
        # Load test data
        self.test_data_manager = DataManager()
        self.test_data = self.test_data_manager.load_test_data()
        
        print(f"Starting test: {method.__name__}")
    
    def teardown_method(self, method):
        """Cleanup method called after each test"""
        print(f"Completed test: {method.__name__}")
        super().teardown_method(method)
    
    def perform_login_to_otp(self):
        """Helper method to login and reach OTP page"""
        try:
            self.logger.info("STEP: Performing login to reach OTP page")
            
            # Navigate to login page
            if not self.login_page.navigate_to_login_page():
                return False
            
            # Get valid credentials
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            email = credentials.get("email")
            password = credentials.get("password")
            
            self.logger.info(f"STEP: Using credentials: {email}")
            
            # Perform login (without redirect check - we'll verify OTP page manually)
            login_success = self.login_page.validate_successful_login_flow(email, password)
            
            if login_success:
                # Wait a moment for redirect to occur
                time.sleep(3)
                
                # Check if we're on OTP page
                if self.otp_page.is_otp_page_loaded():
                    self.logger.info("STEP: Successfully logged in and redirected to OTP page")
                    return True
                else:
                    current_url = self.login_page.driver.current_url
                    self.logger.error(f"STEP: Login successful but not redirected to OTP page. Current URL: {current_url}")
                    return False
            else:
                self.logger.error("STEP: Failed to login")
                return False
                
        except Exception as e:
            self.logger.error(f"STEP: Error during login process: {str(e)}")
            return False
    
    def test_01_validate_otp_page_elements_present(self):
        """Test that OTP page elements are present and accessible"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_01_validate_otp_page_elements_present")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting OTP page elements test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: Verifying OTP page elements")
            
            # Check if OTP page loaded
            assert self.otp_page.is_otp_page_loaded(), "OTP page did not load properly"
            
            # Take screenshot for documentation
            self.take_failure_screenshot("otp_page_elements")
            
            self.logger.info("STEP: OTP page elements test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: OTP page elements test failed: {str(e)}")
            self.take_failure_screenshot("otp_page_elements_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_01_validate_otp_page_elements_present")
            self.logger.info("==================================================")
    
    def test_02_enter_valid_otp_and_verify_success(self):
        """Test OTP verification with valid OTP code (99999)"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_02_enter_valid_otp_and_verify_success")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting valid OTP verification test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: OTP page loaded, now testing valid OTP")
            
            # Enter valid OTP
            valid_otp = "99999"
            assert self.otp_page.enter_otp_code(valid_otp), f"Failed to enter OTP: {valid_otp}"
            self.logger.info(f"STEP: Entered valid OTP: {valid_otp}")
            
            # Click verify button
            assert self.otp_page.click_verify_button(), "Failed to click verify button"
            self.logger.info("STEP: Clicked verify button")
            
            # Verify successful OTP verification and redirect
            redirect_success = self.otp_page.wait_for_redirect_after_verification(timeout=15)
            assert redirect_success, "OTP verification did not redirect to home page"
            
            # Check final URL to confirm we've been redirected
            final_url = self.driver.current_url
            self.logger.info(f"STEP: Final URL after OTP verification: {final_url}")
            
            # Should be redirected to home page or dashboard
            assert ('home' in final_url.lower() or 'dashboard' in final_url.lower() or 
                   final_url.endswith('/') or 'JumpFive' in final_url), f"Invalid redirect URL: {final_url}"
            
            self.logger.info("STEP: Valid OTP verification test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Valid OTP verification test failed: {str(e)}")
            self.take_failure_screenshot("valid_otp_verification_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_02_enter_valid_otp_and_verify_success")
            self.logger.info("==================================================")
    
    def test_03_enter_invalid_otp_and_verify_error_handling(self):
        """Test OTP verification with invalid OTP code"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_03_enter_invalid_otp_and_verify_error_handling")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting invalid OTP verification test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: OTP page loaded, now testing invalid OTP")
            
            # Enter invalid OTP
            invalid_otp = "12345"
            assert self.otp_page.enter_otp_code(invalid_otp), f"Failed to enter OTP: {invalid_otp}"
            self.logger.info(f"STEP: Entered invalid OTP: {invalid_otp}")
            
            # Click verify button
            assert self.otp_page.click_verify_button(), "Failed to click verify button"
            self.logger.info("STEP: Clicked verify button")
            
            # Wait for potential error handling
            time.sleep(3)
            
            # Check that we're still on OTP page (indicating verification failed)
            current_url = self.driver.current_url
            self.logger.info(f"STEP: Current URL after invalid OTP: {current_url}")
            
            # Should still be on OTP page since verification failed
            assert 'otp' in current_url.lower(), f"Should remain on OTP page after invalid OTP, but current URL is: {current_url}"
            
            # Optional: Check for error message if present
            try:
                error_displayed = self.otp_page.is_error_message_displayed()
                self.logger.info(f"STEP: Error message displayed: {error_displayed}")
            except:
                self.logger.info("STEP: No error message check implemented")
            
            self.logger.info("STEP: Invalid OTP verification test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Invalid OTP verification test failed: {str(e)}")
            self.take_failure_screenshot("invalid_otp_verification_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_03_enter_invalid_otp_and_verify_error_handling")
            self.logger.info("==================================================")
    
    def test_04_attempt_verification_with_empty_otp_field(self):
        """Test OTP verification with empty OTP field"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_04_attempt_verification_with_empty_otp_field")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting empty OTP verification test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: OTP page loaded, now testing empty OTP submission")
            
            # Clear OTP field if it has any content
            self.otp_page.clear_otp_field()
            self.logger.info("STEP: OTP field cleared")
            
            # Try to click verify button with empty OTP
            try:
                verify_clicked = self.otp_page.click_verify_button()
                self.logger.info(f"STEP: Verify button click result: {verify_clicked}")
            except:
                self.logger.info("STEP: Verify button may be disabled with empty OTP")
            
            # Wait for potential validation
            time.sleep(2)
            
            # Check that we're still on OTP page
            current_url = self.driver.current_url
            self.logger.info(f"STEP: Current URL after empty OTP submission: {current_url}")
            
            # Should still be on OTP page
            assert 'otp' in current_url.lower(), f"Should remain on OTP page after empty OTP, but current URL is: {current_url}"
            
            # Verify that OTP page is still loaded
            assert self.otp_page.is_otp_page_loaded(), "OTP page should still be loaded"
            
            self.logger.info("STEP: Empty OTP verification test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Empty OTP verification test failed: {str(e)}")
            self.take_failure_screenshot("empty_otp_verification_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_04_attempt_verification_with_empty_otp_field")
            self.logger.info("==================================================")
    
    def test_05_validate_otp_input_field_functionality(self):
        """Test OTP input field functionality and behavior"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_05_validate_otp_input_field_functionality")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting OTP field functionality test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: OTP page loaded, now testing field functionality")
            
            # Test various OTP field behaviors
            test_codes = ["1", "12", "123", "1234", "12345", "123456"]
            
            for code in test_codes:
                self.logger.info(f"STEP: Testing OTP field with: {code}")
                
                # Clear field first
                self.otp_page.clear_otp_field()
                
                # Enter the test code
                assert self.otp_page.enter_otp_code(code), f"Failed to enter OTP: {code}"
                
                # Wait a moment for any field behavior
                time.sleep(1)
                
                # Check if verify button state changes based on field content
                try:
                    button_enabled = self.otp_page.is_verify_button_enabled()
                    self.logger.info(f"STEP: Verify button enabled with '{code}': {button_enabled}")
                except:
                    self.logger.info(f"STEP: Cannot determine verify button state for '{code}'")
            
            # Final validation with the standard test OTP
            self.otp_page.clear_otp_field()
            assert self.otp_page.enter_otp_code("99999"), "Failed to enter final test OTP"
            
            self.logger.info("STEP: OTP field functionality test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: OTP field functionality test failed: {str(e)}")
            self.take_failure_screenshot("otp_field_functionality_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_05_validate_otp_input_field_functionality")
            self.logger.info("==================================================")
    
    def test_06_complete_end_to_end_login_and_otp_flow(self):
        """Test complete end-to-end flow from login to successful OTP verification"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_06_complete_end_to_end_login_and_otp_flow")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting complete end-to-end login and OTP test")
        
        try:
            # Get test credentials
            test_data = DataManager()
            valid_user = test_data.get_login_credentials('valid_user')
            
            self.logger.info("STEP: Starting complete login flow")
            
            # Navigate to login page
            assert self.login_page.navigate_to_login_page(), "Failed to navigate to login page"
            self.logger.info("STEP: Navigated to login page")
            
            # Perform login
            login_result = self.login_page.validate_successful_login_flow(
                email=valid_user['email'],
                password=valid_user['password'],
                accept_terms=True
            )
            
            assert login_result.get('login_successful'), "Login was not successful"
            assert login_result.get('redirected_to_otp'), "Login did not redirect to OTP page"
            self.logger.info("STEP: Login completed successfully, redirected to OTP")
            
            # Verify OTP page is loaded
            assert self.otp_page.is_otp_page_loaded(), "OTP page is not loaded"
            self.logger.info("STEP: OTP page loaded successfully")
            
            # Enter valid OTP
            valid_otp = "99999"
            assert self.otp_page.enter_otp_code(valid_otp), f"Failed to enter OTP: {valid_otp}"
            self.logger.info(f"STEP: Entered valid OTP: {valid_otp}")
            
            # Click verify button
            assert self.otp_page.click_verify_button(), "Failed to click verify button"
            self.logger.info("STEP: Clicked verify button")
            
            # Wait for redirect to home/dashboard
            redirect_success = self.otp_page.wait_for_redirect_after_verification(timeout=15)
            assert redirect_success, "OTP verification did not redirect successfully"
            
            # Validate final URL
            final_url = self.driver.current_url
            self.logger.info(f"STEP: Final URL after complete flow: {final_url}")
            
            # Should be on home page or dashboard
            assert ('home' in final_url.lower() or 'dashboard' in final_url.lower() or 
                   final_url.endswith('/') or 'JumpFive' in final_url), f"Unexpected final URL: {final_url}"
            
            self.logger.info("STEP: Complete end-to-end flow test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Complete end-to-end flow test failed: {str(e)}")
            self.take_failure_screenshot("end_to_end_flow_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_06_complete_end_to_end_login_and_otp_flow")
            self.logger.info("==================================================")
    
    def test_07_validate_otp_redirect_url_after_verification(self):
        """Test OTP verification redirect URL validation"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_07_validate_otp_redirect_url_after_verification")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting OTP redirect URL validation test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            # Record the starting URL
            otp_url = self.driver.current_url
            self.logger.info(f"STEP: Starting OTP URL: {otp_url}")
            
            # Enter valid OTP
            valid_otp = "99999"
            assert self.otp_page.enter_otp_code(valid_otp), f"Failed to enter OTP: {valid_otp}"
            self.logger.info(f"STEP: Entered valid OTP: {valid_otp}")
            
            # Click verify button
            assert self.otp_page.click_verify_button(), "Failed to click verify button"
            self.logger.info("STEP: Clicked verify button")
            
            # Wait for redirect
            time.sleep(5)
            
            # Check final URL
            final_url = self.driver.current_url
            self.logger.info(f"STEP: Final URL after OTP verification: {final_url}")
            
            # Validate that redirect occurred
            assert final_url != otp_url, f"URL did not change from OTP page: {final_url}"
            
            # Validate that we're not on OTP page anymore
            assert 'otp' not in final_url.lower(), f"Still on OTP page after verification: {final_url}"
            
            # Validate expected redirect URL pattern
            expected_patterns = ['home', 'dashboard', 'JumpFive']
            url_valid = any(pattern in final_url for pattern in expected_patterns) or final_url.endswith('/')
            
            assert url_valid, f"Redirect URL does not match expected patterns. URL: {final_url}"
            
            self.logger.info("STEP: OTP redirect URL validation test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: OTP redirect URL validation test failed: {str(e)}")
            self.take_failure_screenshot("otp_redirect_url_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_07_validate_otp_redirect_url_after_verification")
            self.logger.info("==================================================")
    
    def test_08_test_otp_expiration_and_resend_functionality(self):
        """Test OTP expiration (2 min wait), resend button functionality, and valid OTP entry"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_08_test_otp_expiration_and_resend_functionality")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting OTP expiration and resend functionality test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: Successfully reached OTP verification page")
            
            # Take initial screenshot
            self.take_failure_screenshot("otp_expiration_test_start")
            
            # Wait for OTP to expire (2 minutes)
            self.logger.info("STEP: Waiting 2 minutes for OTP to expire...")
            expiration_success = self.otp_page.wait_for_otp_expiration(wait_minutes=2)
            assert expiration_success, "Failed to complete OTP expiration wait"
            
            self.logger.info("STEP: OTP expiration wait completed")
            
            # Check if resend button is clickable
            self.logger.info("STEP: Checking if resend OTP button is clickable after expiration")
            resend_clickable = self.otp_page.is_resend_button_clickable()
            
            # Take screenshot after expiration
            self.take_failure_screenshot("otp_after_expiration")
            
            assert resend_clickable, "Resend OTP button should be clickable after expiration"
            self.logger.info("STEP: Resend button is clickable - validation passed")
            
            # Click resend button
            self.logger.info("STEP: Clicking resend OTP button")
            resend_success = self.otp_page.click_resend_otp_and_verify()
            assert resend_success, "Failed to click resend OTP button"
            
            self.logger.info("STEP: Resend OTP button clicked successfully")
            
            # Take screenshot after resend
            self.take_failure_screenshot("otp_after_resend")
            
            # Enter valid OTP (99999)
            valid_otp = "99999"
            self.logger.info(f"STEP: Entering valid OTP after resend: {valid_otp}")
            
            otp_verification_success = self.otp_page.verify_otp(valid_otp)
            assert otp_verification_success, "Failed to verify valid OTP after resend"
            
            # Wait for redirect
            self.logger.info("STEP: Waiting for redirect after valid OTP")
            time.sleep(5)
            
            # Validate final redirect
            final_url = self.otp_page.get_current_url()
            expected_redirect_url = "https://valueinsightpro.jumpiq.com/JumpFive/home"
            
            self.logger.info(f"STEP: Final URL after OTP resend flow: {final_url}")
            self.logger.info(f"STEP: Expected redirect URL: {expected_redirect_url}")
            
            # Take final screenshot
            self.take_failure_screenshot("otp_resend_flow_complete")
            
            # Assert successful redirect
            assert final_url == expected_redirect_url, f"OTP resend flow did not redirect to expected URL. Expected: {expected_redirect_url}, Got: {final_url}"
            
            self.logger.info("STEP: OTP expiration and resend functionality test completed successfully")
            self.logger.info("STEP: All validations passed - OTP expired, resend worked, valid OTP accepted, proper redirect achieved")
            
        except Exception as e:
            self.logger.error(f"STEP: OTP expiration and resend functionality test failed: {str(e)}")
            self.take_failure_screenshot("otp_expiration_resend_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_08_test_otp_expiration_and_resend_functionality")
            self.logger.info("==================================================")
    
    def test_09_invalid_otp_attempts_with_session_expiry(self):
        """Test invalid OTP attempts: Enter wrong OTP → Error alert → Backspace clear → Repeat 4 times → Redirect to login"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_09_invalid_otp_attempts_with_session_expiry")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting invalid OTP attempts with backspace clearing sequence test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: Successfully reached OTP verification page")
            
            # Take initial screenshot
            self.take_failure_screenshot("invalid_otp_attempts_start")
            
            # Test invalid OTP attempts with session expiry
            self.logger.info("STEP: Starting invalid OTP attempts sequence")
            
            # Use the corrected test method that follows the actual sequence
            session_expiry_test_result = self.otp_page.test_invalid_otp_with_backspace_clearing_sequence(
                invalid_otp="12345"  # Wrong OTP to use for all attempts
            )
            
            assert session_expiry_test_result, "Invalid OTP attempts with session expiry test failed"
            
            # Validate we're now on login page
            final_url = self.driver.current_url
            expected_login_url = "https://valueinsightpro.jumpiq.com/auth/login"
            
            self.logger.info(f"STEP: Final URL after session expiry: {final_url}")
            self.logger.info(f"STEP: Expected login URL: {expected_login_url}")
            
            # Take final screenshot
            self.take_failure_screenshot("invalid_otp_attempts_complete")
            
            # Assert we're back on login page
            assert final_url == expected_login_url or "login" in final_url.lower(), \
                f"Should be redirected to login page after session expiry. Current URL: {final_url}"
            
            self.logger.info("STEP: Invalid OTP attempts with session expiry test completed successfully")
            self.logger.info("STEP: Validated sequence: Enter wrong OTP → Error alert → Backspace clear → Repeat 4 times → Redirect to login")
            
        except Exception as e:
            self.logger.error(f"STEP: Invalid OTP attempts with session expiry test failed: {str(e)}")
            self.take_failure_screenshot("invalid_otp_attempts_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_09_invalid_otp_attempts_with_session_expiry")
            self.logger.info("==================================================")
    
    def test_09_validate_multiple_invalid_otp_attempts(self):
        """Test multiple invalid OTP attempts to understand actual behavior"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_09_validate_multiple_invalid_otp_attempts")
        self.logger.info("==================================================")
        self.logger.info("STEP: Testing actual behavior of multiple invalid OTP attempts")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: Successfully reached OTP verification page")
            self.take_failure_screenshot("multiple_invalid_attempts_start")
            
            # Test multiple invalid attempts to see what actually happens
            attempts_made = 0
            max_attempts = 6  # Test up to 6 attempts
            
            for attempt in range(1, max_attempts + 1):
                self.logger.info(f"STEP: Invalid OTP attempt {attempt}")
                
                # Clear field and enter different invalid OTP each time
                self.otp_page.clear_otp_field()
                invalid_otp = f"1111{attempt}"
                
                assert self.otp_page.enter_otp(invalid_otp), f"Failed to enter OTP on attempt {attempt}"
                assert self.otp_page.click_verify_button(), f"Failed to click verify on attempt {attempt}"
                
                time.sleep(3)  # Wait for response
                attempts_made = attempt
                
                # Check current URL
                current_url = self.driver.current_url
                self.logger.info(f"STEP: After attempt {attempt}, URL: {current_url}")
                
                # If redirected to login, that's the session expiry behavior
                if "login" in current_url.lower():
                    self.logger.info(f"SUCCESS: Session expiry detected after {attempt} invalid attempts")
                    self.logger.info(f"Redirected to: {current_url}")
                    self.take_failure_screenshot(f"session_expiry_after_{attempt}_attempts")
                    
                    # Validate it's the expected login URL
                    expected_login_url = "https://valueinsightpro.jumpiq.com/auth/login"
                    assert current_url == expected_login_url or "login" in current_url.lower(), \
                        f"Expected login URL, got: {current_url}"
                    
                    self.logger.info(f"VALIDATED: Session expires after {attempt} invalid OTP attempts")
                    return  # Test passed
                
                # Check for error messages
                error_message = self.otp_page.get_otp_error_message(2)
                if error_message:
                    self.logger.info(f"STEP: Error message after attempt {attempt}: {error_message}")
                
                # Ensure we're still on OTP page
                assert "otp" in current_url.lower(), f"Unexpected redirect after {attempt} attempts: {current_url}"
            
            # If we reach here, no session expiry occurred
            self.logger.info(f"RESULT: No session expiry after {attempts_made} invalid attempts")
            self.logger.info("Testing if correct OTP still works...")
            
            # Test if correct OTP works
            self.otp_page.clear_otp_field()
            self.otp_page.enter_otp("99999")
            self.otp_page.click_verify_button()
            time.sleep(5)
            
            final_url = self.driver.current_url
            self.logger.info(f"STEP: Final URL after correct OTP: {final_url}")
            
            if "home" in final_url.lower() or "dashboard" in final_url.lower() or "JumpFive" in final_url:
                self.logger.info("CONCLUSION: No session lockout - correct OTP works after multiple invalid attempts")
            else:
                self.logger.info("CONCLUSION: Some form of lockout may be present")
            
            self.take_failure_screenshot("multiple_invalid_attempts_complete")
            
        except Exception as e:
            self.logger.error(f"STEP: Multiple invalid OTP attempts test failed: {str(e)}")
            self.take_failure_screenshot("multiple_invalid_attempts_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_09_validate_multiple_invalid_otp_attempts")
            self.logger.info("==================================================")
    
    def test_10_validate_session_expired_popup_details(self):
        """Test to validate specific details of session expired popup"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_10_validate_session_expired_popup_details")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting session expired popup validation test")
        
        try:
            # First login to reach OTP page
            assert self.perform_login_to_otp(), "Failed to reach OTP page"
            
            self.logger.info("STEP: Successfully reached OTP verification page")
            
            # Perform 3 invalid attempts first
            self.logger.info("STEP: Performing 3 invalid OTP attempts")
            invalid_attempts = self.otp_page.attempt_invalid_otp_multiple_times("99999", attempts=3)
            
            # Validate all 3 attempts stayed on OTP page
            for attempt in invalid_attempts:
                assert attempt.get('still_on_otp_page', False), f"Attempt {attempt['attempt']} did not stay on OTP page"
            
            self.logger.info("STEP: Completed 3 invalid attempts, still on OTP page")
            
            # Fourth attempt
            self.logger.info("STEP: Performing 4th OTP attempt")
            self.otp_page.clear_otp_field()
            assert self.otp_page.enter_otp("11111"), "Failed to enter OTP for 4th attempt"
            assert self.otp_page.click_verify_button(), "Failed to click verify button for 4th attempt"
            
            # Wait for popup and validate its details
            self.logger.info("STEP: Checking session expired popup details")
            time.sleep(3)  # Wait for popup to appear
            
            popup_details = self.otp_page.check_for_session_expired_popup(timeout=10)
            
            # Validate popup presence
            assert popup_details['popup_found'], "Session expired popup should be displayed after 4th invalid attempt"
            self.logger.info("STEP: Session expired popup found")
            
            # Validate popup message contains "Session Expired"
            message_text = popup_details.get('message_text', '')
            assert message_text and "session expired" in message_text.lower(), \
                f"Popup should contain 'Session Expired' message. Found: {message_text}"
            
            self.logger.info(f"STEP: Validated popup message: {message_text}")
            
            # Take screenshot of popup
            self.take_failure_screenshot("session_expired_popup_validation")
            
            # Dismiss popup
            self.logger.info("STEP: Dismissing session expired popup")
            assert self.otp_page.dismiss_session_expired_popup(), "Failed to dismiss session expired popup"
            
            # Validate redirect to login
            self.logger.info("STEP: Validating redirect to login page")
            assert self.otp_page.validate_redirect_to_login_page(), "Failed to redirect to login page"
            
            final_url = self.driver.current_url
            self.logger.info(f"STEP: Successfully redirected to: {final_url}")
            
            self.logger.info("STEP: Session expired popup validation test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Session expired popup validation test failed: {str(e)}")
            self.take_failure_screenshot("session_expired_popup_validation_error")
            raise
        finally:
            self.logger.info("==================================================")
            self.logger.info("FINISHED TEST: test_10_validate_session_expired_popup_details")
            self.logger.info("==================================================")

if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"]) 