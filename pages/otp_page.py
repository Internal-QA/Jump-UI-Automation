"""
OTP Verification Page Object Model for UI Automation Framework
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from base.base_page import BasePage
from utils.locator_manager import get_locator_manager
import time

class OTPPage(BasePage):
    """Page Object for OTP Verification page functionality"""
    
    def __init__(self, driver, config):
        """Initialize OTP page with driver and configuration"""
        super().__init__(driver, config)
        self.page_name = "otp_page"
        self.locator_manager = get_locator_manager()
        self.otp_url = 'https://valueinsightpro.jumpiq.com/auth/otp-verify'
    
    def navigate_to_otp_page(self, timeout=10):
        """Navigate to OTP verification page"""
        try:
            self.driver.get(self.otp_url)
            self.wait_for_page_load(timeout)
            return self.is_otp_page_loaded()
        except Exception as e:
            print(f"Failed to navigate to OTP page: {str(e)}")
            return False
    
    def is_otp_page_loaded(self, timeout=10):
        """Check if OTP verification page has loaded properly"""
        try:
            # Check URL first
            current_url = self.driver.current_url
            if self.otp_url not in current_url:
                print(f"URL mismatch. Expected: {self.otp_url}, Current: {current_url}")
                return False
            
            # Check for OTP input field presence
            otp_input_locator = self.locator_manager.get_locator(self.page_name, "otp_input")
            self.wait.until(EC.presence_of_element_located(otp_input_locator))
            
            # Check for verify button presence
            verify_button_locator = self.locator_manager.get_locator(self.page_name, "verify_button")
            self.wait.until(EC.presence_of_element_located(verify_button_locator))
            
            print("OTP page loaded successfully")
            return True
            
        except TimeoutException:
            print("OTP page elements not found - page may not have loaded")
            return False
        except Exception as e:
            print(f"Error checking OTP page load: {str(e)}")
            return False
    
    def enter_otp(self, otp_code, timeout=10):
        """Enter OTP code in the input field"""
        try:
            print(f"Entering OTP code: {otp_code}")
            
            # Get OTP input field and enter text
            otp_input_locator = self.locator_manager.get_locator(self.page_name, "otp_input")
            success = self.enter_text(otp_input_locator[0], otp_input_locator[1], otp_code)
            
            if success:
                print(f"OTP entered successfully: {otp_code}")
                return True
            else:
                print(f"Failed to enter OTP: {otp_code}")
                return False
                
        except Exception as e:
            print(f"Failed to enter OTP: {str(e)}")
            return False
    
    def click_verify_button(self, timeout=15):
        """Click the verify button"""
        try:
            print("Clicking verify button")
            
            verify_button_locator = self.locator_manager.get_locator(self.page_name, "verify_button")
            success = self.click_element(verify_button_locator[0], verify_button_locator[1])
            
            if success:
                print("Verify button clicked successfully")
                # Wait a moment for any processing
                time.sleep(2)
                return True
            else:
                print("Failed to click verify button")
                return False
            

        except Exception as e:
            print(f"Failed to click verify button: {str(e)}")
            return False
    
    def verify_otp(self, otp_code="99999", timeout=15):
        """Complete OTP verification process"""
        try:
            print(f"Starting OTP verification with code: {otp_code}")
            
            # Ensure we're on the OTP page
            if not self.is_otp_page_loaded():
                print("Not on OTP page - cannot verify OTP")
                return False
            
            # Enter OTP code
            if not self.enter_otp(otp_code):
                return False
            
            # Click verify button
            if not self.click_verify_button():
                return False
            
            print("OTP verification process completed")
            return True
            
        except Exception as e:
            print(f"OTP verification failed: {str(e)}")
            return False
    
    def get_otp_error_message(self, timeout=5):
        """Get any error message displayed after OTP verification"""
        try:
            # Try multiple error message selectors
            error_selectors = [
                self.locator_manager.get_locator(self.page_name, "invalid_otp_alert"),
                self.locator_manager.get_locator(self.page_name, "invalid_otp_error"),
                self.locator_manager.get_locator(self.page_name, "alert_message"),
                self.locator_manager.get_locator(self.page_name, "error_notification"),
                self.locator_manager.get_locator(self.page_name, "otp_expired_error"),
                self.locator_manager.get_locator(self.page_name, "otp_required_error"),
                self.locator_manager.get_locator("common", "any_error")
            ]
            
            for locator in error_selectors:
                try:
                    error_element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located(locator)
                    )
                    error_text = error_element.text.strip()
                    if error_text:
                        print(f"Error message found: {error_text}")
                        return error_text
                except TimeoutException:
                    continue
            
            print("No error message found")
            return None
            
        except Exception as e:
            print(f"Error getting OTP error message: {str(e)}")
            return None
    
    def is_otp_verification_successful(self, timeout=10):
        """Check if OTP verification was successful (URL change or success message)"""
        try:
            # Wait for potential URL change or success indicator
            time.sleep(3)
            
            current_url = self.driver.current_url
            
            # If URL changed from OTP page, verification was likely successful
            if self.otp_url not in current_url:
                print(f"OTP verification successful - redirected to: {current_url}")
                return True
            
            # Check for success message
            try:
                success_locator = self.locator_manager.get_locator(self.page_name, "otp_success")
                success_element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(success_locator)
                )
                success_text = success_element.text.strip()
                if success_text:
                    print(f"OTP verification success message: {success_text}")
                    return True
            except TimeoutException:
                pass
            
            # Check if still on OTP page with no errors
            error_message = self.get_otp_error_message(2)
            if not error_message:
                print("No error message found - OTP verification may have been successful")
                return True
            else:
                print(f"OTP verification failed with error: {error_message}")
                return False
                
        except Exception as e:
            print(f"Error checking OTP verification status: {str(e)}")
            return False
    
    def resend_otp(self, timeout=10):
        """Click resend OTP button if available"""
        try:
            print("Attempting to resend OTP")
            
            resend_locator = self.locator_manager.get_locator(self.page_name, "resend_otp_button")
            success = self.click_element(resend_locator[0], resend_locator[1])
            
            if success:
                print("Resend OTP button clicked")
                return True
            else:
                print("Resend OTP button not found or not clickable")
                return False
                
        except Exception as e:
            print(f"Failed to resend OTP: {str(e)}")
            return False
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def validate_redirect_to_home(self, expected_home_url="https://valueinsightpro.jumpiq.com/JumpFive/home", timeout=10):
        """Validate that OTP verification redirected to the expected home page URL"""
        try:
            print(f"Validating redirect to home page: {expected_home_url}")
            
            # Wait for redirect to complete
            time.sleep(3)
            
            current_url = self.get_current_url()
            
            if current_url == expected_home_url:
                print(f"Redirect validation successful - arrived at: {current_url}")
                return True
            else:
                print(f"Redirect validation failed - Expected: {expected_home_url}, Got: {current_url}")
                return False
                
        except Exception as e:
            print(f"Error validating redirect to home: {str(e)}")
            return False
    
    def wait_for_redirect(self, timeout=10):
        """Wait for redirect away from OTP page"""
        try:
            # Wait for URL to change
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.otp_url not in driver.current_url
            )
            
            new_url = self.driver.current_url
            print(f"Redirected to: {new_url}")
            return new_url
            
        except TimeoutException:
            print("No redirect detected within timeout")
            return None
        except Exception as e:
            print(f"Error waiting for redirect: {str(e)}")
            return None 
    
    def wait_for_otp_expiration(self, wait_minutes=2):
        """Wait for OTP to expire (default 2 minutes)"""
        try:
            wait_seconds = wait_minutes * 60
            print(f"Waiting {wait_minutes} minutes ({wait_seconds} seconds) for OTP to expire...")
            
            # Wait in smaller increments to show progress
            for minute in range(wait_minutes):
                print(f"Waiting... {minute + 1}/{wait_minutes} minutes elapsed")
                time.sleep(60)  # Wait 1 minute at a time
            
            print(f"OTP expiration wait completed - waited {wait_minutes} minutes")
            return True
            
        except Exception as e:
            print(f"Error waiting for OTP expiration: {str(e)}")
            return False
    
    def is_resend_button_clickable(self, timeout=10):
        """Check if the resend OTP button is clickable"""
        try:
            print("Checking if resend OTP button is clickable")
            resend_locator = self.locator_manager.get_locator(self.page_name, "resend_otp_button")
            
            # Check if button exists and is clickable using WebDriverWait
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(self.driver, timeout)
            
            if resend_locator[0].lower() == "xpath":
                element = wait.until(EC.element_to_be_clickable((By.XPATH, resend_locator[1])))
            elif resend_locator[0].lower() == "id":
                element = wait.until(EC.element_to_be_clickable((By.ID, resend_locator[1])))
            elif resend_locator[0].lower() == "css":
                element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, resend_locator[1])))
            elif resend_locator[0].lower() == "class":
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, resend_locator[1])))
            
            if element:
                print("Resend OTP button is clickable")
                return True
            else:
                print("Resend OTP button is not clickable")
                return False
                
        except Exception as e:
            print(f"Error checking resend button clickability: {str(e)}")
            return False
    
    def click_resend_otp_and_verify(self):
        """Click resend OTP button and verify the action was successful"""
        try:
            print("Attempting to click resend OTP button")
            
            # First check if button is clickable
            if not self.is_resend_button_clickable():
                print("Resend button is not clickable")
                return False
            
            # Click the resend button
            if self.resend_otp():
                print("Successfully clicked resend OTP button")
                
                # Wait a moment for any UI updates
                time.sleep(2)
                
                # Verify we're still on OTP page
                current_url = self.get_current_url()
                if "otp-verify" in current_url:
                    print("Resend OTP successful - remained on OTP verification page")
                    return True
                else:
                    print(f"Unexpected redirect after resend OTP: {current_url}")
                    return False
            else:
                print("Failed to click resend OTP button")
                return False
                
        except Exception as e:
            print(f"Error in resend OTP verification: {str(e)}")
            return False
    
    def test_otp_expiration_and_resend_flow(self, valid_otp="99999", wait_minutes=2):
        """Complete test flow: wait for expiration, resend OTP, enter valid OTP"""
        try:
            print(f"Starting OTP expiration and resend flow test")
            
            # Step 1: Wait for OTP to expire
            print("STEP 1: Waiting for OTP to expire...")
            if not self.wait_for_otp_expiration(wait_minutes):
                print("Failed to complete OTP expiration wait")
                return False
            
            # Step 2: Check if resend button is clickable
            print("STEP 2: Checking resend button clickability...")
            if not self.is_resend_button_clickable():
                print("Resend button is not clickable after expiration")
                return False
            
            # Step 3: Click resend button
            print("STEP 3: Clicking resend OTP button...")
            if not self.click_resend_otp_and_verify():
                print("Failed to resend OTP")
                return False
            
            # Step 4: Enter valid OTP
            print(f"STEP 4: Entering valid OTP after resend: {valid_otp}")
            if not self.verify_otp(valid_otp):
                print("Failed to verify OTP after resend")
                return False
            
            print("OTP expiration and resend flow completed successfully")
            return True
            
        except Exception as e:
            print(f"Error in OTP expiration and resend flow: {str(e)}")
            return False
    
    def clear_otp_field(self, timeout=10):
        """Clear the OTP input field"""
        try:
            print("Clearing OTP input field")
            otp_input_locator = self.locator_manager.get_locator(self.page_name, "otp_input")
            otp_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(otp_input_locator)
            )
            otp_element.clear()
            print("OTP field cleared successfully")
            return True
        except Exception as e:
            print(f"Failed to clear OTP field: {str(e)}")
            return False
    
    def clear_otp_field_with_backspace(self, timeout=10):
        """Clear the OTP input field using backspace key"""
        try:
            print("Clearing OTP input field using backspace")
            otp_input_locator = self.locator_manager.get_locator(self.page_name, "otp_input")
            otp_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(otp_input_locator)
            )
            
            # Click to focus on the field
            otp_element.click()
            time.sleep(0.5)
            
            # Use backspace to clear the field (send multiple backspace keys)
            from selenium.webdriver.common.keys import Keys
            for _ in range(10):  # Send enough backspace keys to clear the field
                otp_element.send_keys(Keys.BACK_SPACE)
                time.sleep(0.1)
            
            print("OTP field cleared using backspace")
            return True
        except Exception as e:
            print(f"Failed to clear OTP field with backspace: {str(e)}")
            return False
    
    def enter_otp_code(self, otp_code):
        """Enter OTP code in the input field (alias for enter_otp)"""
        return self.enter_otp(otp_code)
    
    def wait_for_redirect_after_verification(self, timeout=15):
        """Wait for redirect after OTP verification"""
        try:
            print("Waiting for redirect after OTP verification")
            # Wait for URL to change from OTP page
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.otp_url not in driver.current_url
            )
            
            new_url = self.driver.current_url
            print(f"Successfully redirected to: {new_url}")
            return True
            
        except TimeoutException:
            print("No redirect occurred within timeout")
            return False
        except Exception as e:
            print(f"Error waiting for redirect: {str(e)}")
            return False
    
    def is_verify_button_enabled(self, timeout=5):
        """Check if verify button is enabled"""
        try:
            verify_button_locator = self.locator_manager.get_locator(self.page_name, "verify_button")
            button_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(verify_button_locator)
            )
            return button_element.is_enabled()
        except Exception as e:
            print(f"Error checking verify button state: {str(e)}")
            return False
    
    def is_error_message_displayed(self, timeout=5):
        """Check if any error message is displayed"""
        try:
            error_message = self.get_otp_error_message(timeout)
            return error_message is not None and error_message.strip() != ""
        except Exception as e:
            print(f"Error checking error message display: {str(e)}")
            return False
    
    def attempt_invalid_otp_multiple_times(self, invalid_otp="12345", attempts=3):
        """Attempt invalid OTP multiple times and return results for each attempt"""
        results = []
        
        for attempt in range(1, attempts + 1):
            try:
                print(f"Attempt {attempt}/{attempts}: Entering invalid OTP: {invalid_otp}")
                
                # Clear field first
                self.clear_otp_field()
                
                # Enter invalid OTP
                if not self.enter_otp(invalid_otp):
                    results.append({
                        'attempt': attempt,
                        'otp_entered': False,
                        'verify_clicked': False,
                        'error_message': None,
                        'still_on_otp_page': True
                    })
                    continue
                
                # Click verify button
                verify_clicked = self.click_verify_button()
                
                # Wait for response
                time.sleep(3)
                
                # Check for error message
                error_message = self.get_otp_error_message(2)
                
                # Check if still on OTP page
                current_url = self.driver.current_url
                still_on_otp_page = self.otp_url in current_url
                
                attempt_result = {
                    'attempt': attempt,
                    'otp_entered': True,
                    'verify_clicked': verify_clicked,
                    'error_message': error_message,
                    'still_on_otp_page': still_on_otp_page,
                    'current_url': current_url
                }
                
                results.append(attempt_result)
                print(f"Attempt {attempt} result: {attempt_result}")
                
            except Exception as e:
                print(f"Error in attempt {attempt}: {str(e)}")
                results.append({
                    'attempt': attempt,
                    'error': str(e),
                    'otp_entered': False,
                    'verify_clicked': False,
                    'error_message': None,
                    'still_on_otp_page': True
                })
        
        return results
    
    def check_for_session_expired_popup(self, timeout=10):
        """Check for session expired popup and return details"""
        try:
            print("Checking for session expired popup")
            
            # First, check for any popup at all
            any_popup_locator = self.locator_manager.get_locator(self.page_name, "any_popup")
            any_error_locator = self.locator_manager.get_locator(self.page_name, "any_error_text")
            
            popup_found = False
            message_text = None
            all_text = None
            
            # Check for any popup first
            try:
                print("Checking for any popup...")
                popup_element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(any_popup_locator)
                )
                popup_found = True
                print("Some popup found")
                
                # Get all text from the popup
                all_text = popup_element.text.strip()
                print(f"Popup text: {all_text}")
                
            except TimeoutException:
                print("No popup found at all")
            
            # Check for any error text on the page
            try:
                print("Checking for any error text...")
                error_elements = self.driver.find_elements(*any_error_locator)
                if error_elements:
                    for element in error_elements:
                        element_text = element.text.strip()
                        if element_text:
                            print(f"Found error text: {element_text}")
                            if not message_text:
                                message_text = element_text
            except Exception as e:
                print(f"Error checking for error text: {e}")
            
            # Check specific session expired locators
            session_popup_locator = self.locator_manager.get_locator(self.page_name, "session_expired_popup")
            session_message_locator = self.locator_manager.get_locator(self.page_name, "session_expired_message")
            
            try:
                # Check for session expired popup specifically
                popup_element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(session_popup_locator)
                )
                popup_found = True
                print("Session expired popup found")
                
                # Get message text
                try:
                    message_element = self.driver.find_element(*session_message_locator)
                    message_text = message_element.text.strip()
                    print(f"Session expired message: {message_text}")
                except:
                    print("Could not extract specific session expired message text")
                
            except TimeoutException:
                print("No specific session expired popup found")
            
            # Check current URL to see if we were redirected
            current_url = self.driver.current_url
            print(f"Current URL during popup check: {current_url}")
            
            # If we were redirected to login, that might indicate session expiry
            if "login" in current_url.lower():
                print("Detected redirect to login page - this might indicate session expiry")
                popup_found = True
                if not message_text:
                    message_text = "Redirected to login (possible session expiry)"
            
            return {
                'popup_found': popup_found,
                'message_text': message_text,
                'all_popup_text': all_text,
                'current_url': current_url
            }
            
        except Exception as e:
            print(f"Error checking for session expired popup: {str(e)}")
            return {
                'popup_found': False,
                'message_text': None,
                'error': str(e)
            }
    
    def dismiss_session_expired_popup(self, timeout=10):
        """Dismiss session expired popup by clicking OK or close button"""
        try:
            print("Attempting to dismiss session expired popup")
            
            # Try OK button first
            ok_button_locator = self.locator_manager.get_locator(self.page_name, "popup_ok_button")
            close_button_locator = self.locator_manager.get_locator(self.page_name, "popup_close_button")
            
            try:
                ok_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(ok_button_locator)
                )
                ok_button.click()
                print("Clicked OK button on session expired popup")
                return True
            except TimeoutException:
                pass
            
            try:
                close_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(close_button_locator)
                )
                close_button.click()
                print("Clicked close button on session expired popup")
                return True
            except TimeoutException:
                pass
            
            print("Could not find OK or close button to dismiss popup")
            return False
            
        except Exception as e:
            print(f"Error dismissing session expired popup: {str(e)}")
            return False
    
    def validate_redirect_to_login_page(self, expected_login_url="https://valueinsightpro.jumpiq.com/auth/login", timeout=10):
        """Validate redirect to login page after session expiry"""
        try:
            print(f"Validating redirect to login page: {expected_login_url}")
            
            # Wait for redirect
            time.sleep(3)
            
            current_url = self.driver.current_url
            print(f"Current URL after redirect: {current_url}")
            
            if current_url == expected_login_url:
                print("Successfully redirected to login page")
                return True
            elif "login" in current_url.lower():
                print(f"Redirected to login page (URL may have additional parameters): {current_url}")
                return True
            else:
                print(f"Redirect validation failed - Expected: {expected_login_url}, Got: {current_url}")
                return False
                
        except Exception as e:
            print(f"Error validating redirect to login page: {str(e)}")
            return False
    
    def test_invalid_otp_with_backspace_clearing_sequence(self, invalid_otp="12345"):
        """Test the specific sequence: enter wrong OTP -> error alert -> backspace clear -> repeat 4 times -> redirect"""
        try:
            print("Starting invalid OTP with backspace clearing sequence test")
            print("Expected behavior: Enter wrong OTP → Error alert → Backspace clear → Repeat 4 times → Redirect to login")
            
            for attempt in range(1, 5):  # 4 attempts
                print(f"\n--- Attempt {attempt}/4 ---")
                
                # Step 1: Enter wrong OTP
                print(f"STEP 1: Entering wrong OTP: {invalid_otp}")
                if not self.enter_otp(invalid_otp):
                    print(f"Failed to enter OTP on attempt {attempt}")
                    return False
                
                # Step 2: Click verify button
                print("STEP 2: Clicking verify button")
                if not self.click_verify_button():
                    print(f"Failed to click verify button on attempt {attempt}")
                    return False
                
                # Step 3: Wait for error alert to appear
                print("STEP 3: Waiting for error alert...")
                time.sleep(2)  # Wait for error alert
                
                # Check for error message
                error_message = self.get_otp_error_message(3)
                if error_message:
                    print(f"✓ Error alert appeared: {error_message}")
                else:
                    print("⚠ No error alert detected, but continuing...")
                
                # Step 4: Check if we were redirected immediately after this attempt
                current_url = self.driver.current_url
                print(f"Current URL after attempt {attempt}: {current_url}")
                
                if "login" in current_url.lower():
                    print(f"✓ SUCCESS: Redirected to login after {attempt} attempts!")
                    print(f"Login URL: {current_url}")
                    return True
                
                # Step 5: Use backspace to clear the OTP field (if still on OTP page)
                if "otp" in current_url.lower():
                    print("STEP 5: Using backspace to clear OTP field")
                    clear_success = self.clear_otp_field_with_backspace()
                    if not clear_success:
                        print(f"Failed to clear OTP field with backspace on attempt {attempt}")
                        # If we can't clear the field, it might indicate session expiry
                        # Wait a bit and check for redirect
                        print("Waiting for potential delayed redirect due to clearing failure...")
                        time.sleep(5)
                        current_url = self.driver.current_url
                        if "login" in current_url.lower():
                            print(f"✓ SUCCESS: Delayed redirect to login detected!")
                            print(f"Login URL: {current_url}")
                            return True
                        # Try alternative clearing method
                        print("Trying alternative clearing method...")
                        self.clear_otp_field()  # Use regular clear method as fallback
                
                # Step 6: Wait a moment before next attempt
                time.sleep(2)
            
            # After all 4 attempts, wait a bit more for potential delayed redirect
            print("\nAll 4 attempts completed. Waiting for potential redirect...")
            for wait_time in [3, 5, 10]:
                time.sleep(wait_time)
                current_url = self.driver.current_url
                print(f"URL after {wait_time}s additional wait: {current_url}")
                
                if "login" in current_url.lower():
                    print(f"✓ DELAYED SUCCESS: Redirected to login after waiting!")
                    print(f"Login URL: {current_url}")
                    return True
            
            # If no redirect occurred
            final_url = self.driver.current_url
            print(f"FAIL: FAILURE: No redirect occurred after 4 attempts with backspace clearing")
            print(f"Expected: Redirect to https://valueinsightpro.jumpiq.com/auth/login")
            print(f"Actual: Remained on {final_url}")
            
            return False
            
        except Exception as e:
            print(f"Error in invalid OTP with backspace clearing sequence test: {str(e)}")
            return False
    
    def test_invalid_otp_attempts_with_session_expiry(self, invalid_otp="12345", fourth_attempt_otp="54321"):
        """Complete test for invalid OTP attempts leading to session expiry redirect"""
        try:
            print("Starting invalid OTP attempts with session expiry test")
            print("Expected behavior: 3 wrong attempts stay on OTP page, 4th attempt redirects to login")
            
            # Step 1: Attempt invalid OTP 3 times
            print("STEP 1: Attempting invalid OTP 3 times")
            invalid_attempts = self.attempt_invalid_otp_multiple_times(invalid_otp, attempts=3)
            
            # Validate first 3 attempts stay on OTP page
            for attempt_result in invalid_attempts:
                if not attempt_result.get('still_on_otp_page', False):
                    print(f"Unexpected behavior: Not on OTP page after attempt {attempt_result['attempt']}")
                    return False
            
            print("✓ First 3 invalid attempts completed - remained on OTP page as expected")
            
            # Step 2: Fourth attempt (should trigger session expiry and redirect)
            print(f"STEP 2: Fourth attempt with OTP: {fourth_attempt_otp}")
            
            # Record current URL before 4th attempt
            url_before_4th = self.driver.current_url
            print(f"URL before 4th attempt: {url_before_4th}")
            
            self.clear_otp_field()
            if not self.enter_otp(fourth_attempt_otp):
                print("Failed to enter OTP for fourth attempt")
                return False
            
            if not self.click_verify_button():
                print("Failed to click verify button for fourth attempt")
                return False
            
            # Step 3: Wait for and validate redirect to login page
            print("STEP 3: Waiting for redirect to login page after 4th attempt")
            
            # Wait progressively and check URL
            for wait_seconds in [2, 3, 5]:
                time.sleep(wait_seconds)
                current_url = self.driver.current_url
                print(f"URL after {wait_seconds}s wait: {current_url}")
                
                if current_url != url_before_4th and "login" in current_url.lower():
                    expected_login_url = "https://valueinsightpro.jumpiq.com/auth/login"
                    
                    if current_url == expected_login_url:
                        print(f"✓ SUCCESS: Redirected to exact expected login URL: {current_url}")
                        print("✓ Session expiry behavior validated successfully")
                        return True
                    elif "login" in current_url:
                        print(f"✓ SUCCESS: Redirected to login page: {current_url}")
                        print("✓ Session expiry behavior validated (URL may have parameters)")
                        return True
                
                if wait_seconds < 5:  # Don't print this on the last iteration
                    print(f"Still on same page after {wait_seconds}s, waiting more...")
            
            # Final check after all waits
            final_url = self.driver.current_url
            print(f"Final URL after all waits: {final_url}")
            
            if final_url != url_before_4th:
                if "login" in final_url.lower():
                    print(f"✓ DELAYED SUCCESS: Eventually redirected to login: {final_url}")
                    return True
                else:
                    print(f"⚠ Redirected but not to login page: {final_url}")
                    return False
            else:
                print("FAIL: FAILURE: No redirect occurred after 4th invalid OTP attempt")
                print("Expected: Redirect to https://valueinsightpro.jumpiq.com/auth/login")
                print(f"Actual: Remained on {final_url}")
                
                # Take debug screenshot
                try:
                    self.driver.save_screenshot("debug_no_redirect_after_4th_attempt.png")
                    print("Debug screenshot saved: debug_no_redirect_after_4th_attempt.png")
                except:
                    pass
                
                return False
            
        except Exception as e:
            print(f"Error in invalid OTP attempts with session expiry test: {str(e)}")
            return False 
    
 