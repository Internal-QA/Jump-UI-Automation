import pytest
import sys
import os
import time
from datetime import datetime

# Add the parent directory to the path to import framework modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_test import BaseTest
from pages.login_page import LoginPage
from utils.test_data_manager import DataManager
from utils.logger import get_logger
from utils.report_generator import ReportGenerator
import allure

@allure.epic("UI Automation Test Suite")
@allure.feature("Login Functionality")
@allure.story("User Authentication and Login Page Interactions")
class TestLogin(BaseTest):
    """Test class for login functionality"""
    
    @classmethod
    def setup_class(cls):
        """Setup class - runs once before all tests in this class"""
        super().setup_class()
        cls.test_data_manager = DataManager()
        cls.logger = get_logger()
        cls.report_generator = ReportGenerator()
        cls.report_generator.start_execution()
        
        # Create test data file if it doesn't exist
        cls.test_data_manager.create_test_data_file()
        
        cls.logger.info("Starting Login Test Suite")
    
    @classmethod
    def teardown_class(cls):
        """Teardown class - runs once after all tests in this class"""
        cls.report_generator.end_execution()
        html_report = cls.report_generator.generate_html_report("login_test_report")
        json_report = cls.report_generator.export_json_report("login_test_report")
        
        cls.logger.info("Login Test Suite completed")
        cls.logger.info(f"HTML Report: {html_report}")
        cls.logger.info(f"JSON Report: {json_report}")
    
    def setup_method(self, method):
        """Setup method - runs before each test"""
        super().setup_method(method)
        self.login_page = LoginPage(self.driver, self.config)
        self.test_start_time = time.time()
        self.test_steps = []
        self.logger.log_test_start(method.__name__)
    
    def teardown_method(self, method):
        """Teardown method - runs after each test"""
        test_duration = time.time() - self.test_start_time
        
        # Determine test status
        test_status = "passed"
        error_message = None
        screenshot_path = None
        
        if hasattr(self, '_test_failed') and self._test_failed:
            test_status = "failed"
            error_message = getattr(self, '_test_error', "Test failed")
            screenshot_path = self.login_page.take_login_page_screenshot(f"failed_{method.__name__}")
        
        # Add test result to report
        self.report_generator.add_test_result(
            test_name=method.__name__,
            status=test_status,
            duration=test_duration,
            error_message=error_message,
            screenshot_path=screenshot_path,
            test_steps=self.test_steps
        )
        
        self.logger.log_test_end(method.__name__, test_status.upper())
        super().teardown_method(method)
    
    def add_test_step(self, step_description):
        """Add a test step to the current test"""
        self.test_steps.append(step_description)
        self.logger.log_step(step_description)
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("login", "authentication", "critical")
    def test_01_login_with_valid_credentials(self):
        """Test valid login credentials and successful authentication"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_01_login_with_valid_credentials")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting valid login test")

        try:
            # Get test data
            test_data = DataManager()
            valid_user = test_data.get_login_credentials('valid_user')
            
            # Navigate to login page and validate
            success = self.login_page.validate_successful_login_flow(
                valid_user['email'], 
                valid_user['password']
            )
            
            assert success, "Login was not attempted"
            self.logger.info("STEP: Valid login test completed successfully")
            
        except Exception as e:
            self.logger.error(f"STEP: Valid login test failed: {str(e)}")
            self.take_failure_screenshot("valid_login_error")
            raise

        self.logger.info("==================================================")
        self.logger.info("FINISHED TEST: test_01_login_with_valid_credentials")
        self.logger.info("==================================================")

    def test_02_attempt_login_with_invalid_email(self):
        """Test login with invalid email"""
        try:
            self.add_test_step("Starting invalid email test")
            
            # Get invalid credentials
            credentials = self.test_data_manager.get_login_credentials("invalid_user")
            
            self.add_test_step(f"Using invalid email: {credentials['email']}")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Fill in credentials
            self.login_page.enter_email(credentials['email'])
            self.add_test_step("Entered invalid email")
            
            self.login_page.enter_password(credentials['password'])
            self.add_test_step("Entered password")
            
            # Try to login
            self.login_page.click_sign_in_button()
            self.add_test_step("Clicked login button")
            
            # Wait for error message
            time.sleep(3)
            
            # Check if we're still on login page (indicating error)
            current_url = self.driver.current_url
            self.add_test_step(f"Current URL after login attempt: {current_url}")
            
            # Should still be on login page or see error
            assert 'login' in current_url.lower() or 'error' in current_url.lower(), "Should show error for invalid email"
            
            self.add_test_step("✓ Invalid email test passed - error handling working correctly")
            
        except Exception as e:
            self.add_test_step(f"✗ Invalid email test failed: {str(e)}")
            self.take_failure_screenshot("invalid_email_error")
            raise

    def test_03_attempt_login_with_empty_email(self):
        """Test login form validation with empty email field"""
        try:
            self.add_test_step("Starting empty email validation test")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Only enter password, leave email empty
            password = "TestPassword123!"
            self.login_page.enter_password(password)
            self.add_test_step("Entered password only (email left empty)")
            
            # Try to click login button
            self.login_page.click_sign_in_button()
            self.add_test_step("Attempted to click login button")
            
            # Wait for validation
            time.sleep(2)
            
            # Check if login button is still disabled or form validation prevents submission
            current_url = self.driver.current_url
            self.add_test_step(f"Current URL after login attempt: {current_url}")
            
            # Should still be on login page
            assert 'login' in current_url.lower(), "Should remain on login page due to empty email validation"
            
            self.add_test_step("✓ Empty email validation test passed")
            
        except Exception as e:
            self.add_test_step(f"✗ Empty email validation test failed: {str(e)}")
            self.take_failure_screenshot("empty_email_error")
            raise

    def test_04_attempt_login_with_empty_password(self):
        """Test login form validation with empty password field"""
        try:
            self.add_test_step("Starting empty password validation test")
            
            # Get valid email
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Only enter email, leave password empty
            self.login_page.enter_email(credentials['email'])
            self.add_test_step("Entered email only (password left empty)")
            
            # Try to click login button
            self.login_page.click_sign_in_button()
            self.add_test_step("Attempted to click login button")
            
            # Wait for validation
            time.sleep(2)
            
            # Check if we're still on login page
            current_url = self.driver.current_url
            self.add_test_step(f"Current URL after login attempt: {current_url}")
            
            # Should still be on login page
            assert 'login' in current_url.lower(), "Should remain on login page due to empty password validation"
            
            self.add_test_step("✓ Empty password validation test passed")
            
        except Exception as e:
            self.add_test_step(f"✗ Empty password validation test failed: {str(e)}")
            self.take_failure_screenshot("empty_password_error")
            raise

    def test_05_attempt_login_without_accepting_terms(self):
        """Test login when terms and conditions are not accepted"""
        try:
            self.add_test_step("Starting terms acceptance validation test")
            
            # Get valid credentials
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Fill in credentials but don't accept terms
            self.login_page.enter_email(credentials['email'])
            self.login_page.enter_password(credentials['password'])
            self.add_test_step("Entered valid credentials")
            
            # Ensure terms checkbox is not checked (if it exists)
            try:
                # Look for terms checkbox and ensure it's unchecked
                terms_checkbox = self.driver.find_element("xpath", "//input[@type='checkbox']")
                if terms_checkbox.is_selected():
                    terms_checkbox.click()  # Uncheck it
                self.add_test_step("Ensured terms checkbox is unchecked")
            except:
                self.add_test_step("No terms checkbox found - test may not be applicable")
            
            # Try to click login button
            self.login_page.click_sign_in_button()
            self.add_test_step("Attempted to click login button without accepting terms")
            
            # Wait for validation
            time.sleep(3)
            
            # Check if we're still on login page or see error
            current_url = self.driver.current_url
            self.add_test_step(f"Current URL after login attempt: {current_url}")
            
            # Should either remain on login page or show error
            assert 'login' in current_url.lower() or 'error' in current_url.lower(), "Should prevent login without terms acceptance"
            
            self.add_test_step("✓ Terms acceptance validation test passed")
            
        except Exception as e:
            self.add_test_step(f"✗ Terms acceptance validation test failed: {str(e)}")
            self.take_failure_screenshot("terms_validation_error")
            raise

    def test_06_validate_all_login_page_elements_present(self):
        """Test presence of all login page elements"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_06_validate_all_login_page_elements_present")
        self.logger.info("==================================================")
        self.logger.info("STEP: Starting login page elements test")

        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.logger.info("STEP: Navigating to login page")

            # Check email field presence
            email_locator = self.login_page.locator_manager.get_locator("login_page", "email_field")
            assert self.login_page.is_element_present(email_locator[0], email_locator[1]), "Email field is not present"
            self.logger.info("STEP: Checking email field presence")

            # Check password field presence
            password_locator = self.login_page.locator_manager.get_locator("login_page", "password_field")
            assert self.login_page.is_element_present(password_locator[0], password_locator[1]), "Password field is not present"
            self.logger.info("STEP: Checking password field presence")

            # Check checkbox presence
            checkbox_locator = self.login_page.locator_manager.get_locator("login_page", "terms_checkbox")
            assert self.login_page.is_element_present(checkbox_locator[0], checkbox_locator[1]), "Terms checkbox is not present"
            self.logger.info("STEP: Checking checkbox presence")

            # Check sign in button presence
            button_locator = self.login_page.locator_manager.get_locator("login_page", "sign_in_button")
            assert self.login_page.is_element_present(button_locator[0], button_locator[1]), "Sign In button is not present"
            self.logger.info("STEP: Checking sign in button presence")

            # Check sign in button text
            button_element = self.login_page.find_element(button_locator[0], button_locator[1])
            button_text = button_element.text if button_element else ""
            assert "Sign In" in button_text, f"Expected 'Sign In' but got '{button_text}'"
            self.logger.info("STEP: Verifying sign in button text")

            # Take screenshot for verification
            self.take_failure_screenshot("login_page_elements")
            self.logger.info("STEP: Taking screenshot of login page")

            self.logger.info("STEP: Login page elements test completed successfully")

        except Exception as e:
            self.logger.error(f"STEP: Login page elements test failed: {str(e)}")
            self.take_failure_screenshot("login_elements_error")
            raise

        self.logger.info("==================================================")
        self.logger.info("FINISHED TEST: test_06_validate_all_login_page_elements_present")
        self.logger.info("==================================================")
    
    def test_07_clear_login_form(self):
        """Test clearing the login form"""
        try:
            self.add_test_step("Starting clear login form test")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Fill form with data
            self.login_page.enter_email("test@example.com")
            self.add_test_step("Entered email")
            self.login_page.enter_password("testpassword")
            self.add_test_step("Entered password")
            self.login_page.check_terms_and_conditions()
            self.add_test_step("Checked terms checkbox")
            
            # Verify checkbox is checked
            assert self.login_page.is_checkbox_checked(), "Checkbox should be checked"
            
            # Clear the form
            self.login_page.clear_login_form()
            
            # Verify form is cleared
            assert not self.login_page.is_checkbox_checked(), "Checkbox should be unchecked after clear"
            
            self.add_test_step("Clear login form test completed successfully")
            
        except Exception as e:
            self.add_test_step(f"✗ Clear login form test failed: {str(e)}")
            self.take_failure_screenshot("clear_login_form_error")
            raise
    
    def test_08_successful_login_otp_redirect(self):
        """Test that successful login redirects to OTP verification page"""
        try:
            self.add_test_step("Starting OTP redirect validation test")
            
            # Get valid credentials from test data
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            
            self.add_test_step(f"Testing OTP redirect with credentials: {credentials['email']}")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Perform login
            self.login_page.enter_email(credentials['email'])
            self.add_test_step("Entered email")
            self.login_page.enter_password(credentials['password'])
            self.add_test_step("Entered password")
            self.login_page.check_terms_and_conditions()
            self.add_test_step("Checked terms")
            self.login_page.click_sign_in_button()
            self.add_test_step("Clicked login button")
            
            assert self.login_page.is_redirected_to_otp_page(timeout=15), "User was not redirected to OTP verification page"
            
            # Get final URL for validation
            final_url = self.driver.current_url
            self.add_test_step(f"Final URL after login: {final_url}")
            
            # Validate redirect occurred
            assert 'otp-verify' in final_url.lower(), f"Expected OTP URL not found in final URL: {final_url}"
            
            # Additional validation - ensure we're not on login page anymore
            login_url = self.config.get('login_url', 'https://valueinsightpro.jumpiq.com/auth/login')
            assert login_url not in final_url, f"Still on login page after successful login: {final_url}"
            
            self.add_test_step("✅ OTP redirect validation test completed successfully")
            
        except Exception as e:
            self.add_test_step(f"✗ OTP redirect validation test failed: {str(e)}")
            self.take_failure_screenshot("otp_redirect_error")
            raise
    
    def test_09_sign_in_button_state_validation(self):
        """Test that sign-in button is properly enabled/disabled during form completion"""
        try:
            self.add_test_step("Starting sign-in button state validation test")
            
            # Get valid credentials
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")
            
            # Verify login page is loaded
            assert self.login_page.is_login_page_loaded(), "Login page is not properly loaded"
            
            # Perform form state progression validation
            form_validation = self.login_page.validate_form_state_progression(
                credentials['email'], 
                credentials['password']
            )
            
            # Log detailed validation results
            self.add_test_step(f"Initial state recorded: {form_validation.get('initial_state', False)}")
            self.add_test_step(f"Email field completion handled: {form_validation.get('after_email', False)}")
            self.add_test_step(f"Password field completion handled: {form_validation.get('after_password', False)}")
            self.add_test_step(f"Checkbox completion handled: {form_validation.get('after_checkbox', False)}")
            self.add_test_step(f"Complete form enables button: {form_validation.get('all_stages_correct', False)}")
            
            # Assertions
            assert form_validation.get('initial_state', False), "Failed to record initial button state"
            assert form_validation.get('after_email', False), "Failed to validate button state after email entry"
            assert form_validation.get('after_password', False), "Failed to validate button state after password entry"
            assert form_validation.get('after_checkbox', False), "Button not enabled after checking terms checkbox"
            assert form_validation.get('all_stages_correct', False), "Overall form state progression validation failed"
            
            self.add_test_step("✅ Sign-in button state validation test completed successfully")
            
        except Exception as e:
            self.add_test_step(f"✗ Sign-in button state validation test failed: {str(e)}")
            self.take_failure_screenshot("sign_in_button_state_error")
            raise

    @allure.title("Password Eye Icon Functionality")
    @allure.description("Tests the password visibility toggle functionality using the eye icon")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "password", "interaction")
    def test_010_password_eye_icon_functionality(self):
        """Test password eye icon functionality to toggle password visibility"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_010_password_eye_icon_functionality")
        self.logger.info("==================================================")
        self.logger.info("STEP: Testing password eye icon functionality")

        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")

            # Enter password to test eye icon
            test_password = "testpassword123"
            self.login_page.enter_password(test_password)
            self.add_test_step("Entered password")

            # Validate password eye icon functionality
            assert self.login_page.validate_password_eye_icon_functionality(), "Password eye icon validation failed"
            self.logger.info("STEP: Password eye icon functionality validated successfully")

        except Exception as e:
            self.add_test_step(f"✗ Password eye icon test failed: {str(e)}")
            self.take_failure_screenshot("password_eye_icon_error")
            raise

        self.logger.info("==================================================")
        self.logger.info("FINISHED TEST: test_010_password_eye_icon_functionality")
        self.logger.info("==================================================")

    @allure.title("Need Help Button Functionality")
    @allure.description("Tests the 'Need help?' button functionality including modal opening and closing")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("ui", "help", "modal")
    def test_011_need_help_button_functionality(self):
        """Test 'Need help?' button functionality"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_011_need_help_button_functionality")
        self.logger.info("==================================================")
        self.logger.info("STEP: Testing 'Need help?' button functionality")

        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")

            # Take screenshot before testing
            self.take_failure_screenshot("before_help_button_test")

            # Validate 'Need help?' button functionality
            assert self.login_page.validate_need_help_functionality(), "Need help button validation failed"
            self.logger.info("STEP: 'Need help?' button functionality validated successfully")

            # Take screenshot after testing
            self.take_failure_screenshot("after_help_button_test")

        except Exception as e:
            self.add_test_step(f"✗ 'Need help?' button test failed: {str(e)}")
            self.take_failure_screenshot("need_help_button_error")
            raise

        self.logger.info("==================================================")
        self.logger.info("FINISHED TEST: test_011_need_help_button_functionality")
        self.logger.info("==================================================")

    @allure.title("Privacy Policy Button Functionality")
    @allure.description("Tests the 'Privacy Policy' button functionality including modal opening and closing")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("ui", "privacy", "modal")
    def test_012_privacy_policy_button_functionality(self):
        """Test 'Privacy Policy' button functionality"""
        self.logger.info("==================================================")
        self.logger.info("STARTING TEST: test_012_privacy_policy_button_functionality")
        self.logger.info("==================================================")
        self.logger.info("STEP: Testing 'Privacy Policy' button functionality")

        try:
            # Navigate to login page
            self.login_page.navigate_to_login_page()
            self.add_test_step("Navigated to login page")

            # Take screenshot before testing
            self.take_failure_screenshot("before_privacy_policy_test")

            # Validate 'Privacy Policy' button functionality
            assert self.login_page.validate_privacy_policy_functionality(), "Privacy Policy button validation failed"
            self.logger.info("STEP: 'Privacy Policy' button functionality validated successfully")

            # Take screenshot after testing
            self.take_failure_screenshot("after_privacy_policy_test")

        except Exception as e:
            self.add_test_step(f"✗ 'Privacy Policy' button test failed: {str(e)}")
            self.take_failure_screenshot("privacy_policy_button_error")
            raise

        self.logger.info("==================================================")
        self.logger.info("FINISHED TEST: test_012_privacy_policy_button_functionality")
        self.logger.info("==================================================")



if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"]) 