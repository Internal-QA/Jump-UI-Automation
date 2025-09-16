#!/usr/bin/env python3
"""
Test to validate actual OTP behavior instead of expected behavior
Run this to understand what the application actually does with invalid OTP attempts
"""

import pytest
import sys
import os

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_test import BaseTest
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from utils.test_data_manager import DataManager
from utils.logger import get_logger
import time


class TestActualOTPBehavior(BaseTest):
    """Test class to understand actual OTP behavior"""
    
    def setup_method(self, method):
        """Setup method called before each test"""
        super().setup_method(method)
        self.login_page = LoginPage(self.driver, self.config)
        self.otp_page = OTPPage(self.driver, self.config)
        self.test_data_manager = DataManager()
        self.logger = get_logger()
    
    def perform_login_to_otp(self):
        """Helper method to login and reach OTP page"""
        try:
            if not self.login_page.navigate_to_login_page():
                return False
            
            credentials = self.test_data_manager.get_login_credentials("valid_user")
            login_success = self.login_page.validate_successful_login_flow(
                credentials["email"], credentials["password"]
            )
            
            if login_success:
                time.sleep(3)
                return self.otp_page.is_otp_page_loaded()
            return False
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def test_actual_invalid_otp_behavior(self):
        """Test what actually happens with multiple invalid OTP attempts"""
        print("=" * 80)
        print("TESTING ACTUAL OTP BEHAVIOR")
        print("=" * 80)
        
        # Login to reach OTP page
        assert self.perform_login_to_otp(), "Failed to reach OTP page"
        print("✓ Successfully reached OTP page")
        
        # Test multiple invalid attempts
        max_attempts = 10
        for attempt in range(1, max_attempts + 1):
            print(f"\n--- Attempt {attempt} ---")
            
            # Clear and enter invalid OTP
            self.otp_page.clear_otp_field()
            invalid_otp = f"1111{attempt}"
            
            print(f"Entering invalid OTP: {invalid_otp}")
            assert self.otp_page.enter_otp(invalid_otp), f"Failed to enter OTP on attempt {attempt}"
            
            # Click verify
            assert self.otp_page.click_verify_button(), f"Failed to click verify on attempt {attempt}"
            
            # Wait and check result
            time.sleep(3)
            
            current_url = self.driver.current_url
            print(f"URL after attempt {attempt}: {current_url}")
            
            # Check if redirected to login
            if "login" in current_url.lower():
                print(f"🎉 FOUND IT! Redirected to login after {attempt} invalid attempts")
                print(f"Final URL: {current_url}")
                return  # Test completed successfully
            
            # Check for error messages
            error_msg = self.otp_page.get_otp_error_message(2)
            if error_msg:
                print(f"Error message: {error_msg}")
            else:
                print("No error message displayed")
            
            # Continue if still on OTP page
            if "otp" in current_url.lower():
                print(f"Still on OTP page after {attempt} attempts")
            else:
                print(f"Unexpected redirect to: {current_url}")
                break
        
        print(f"\n❌ No redirect occurred after {max_attempts} invalid attempts")
        print("Conclusion: Session expiry behavior may not be implemented as described")
        
        # Test if correct OTP still works
        print("\n--- Testing Correct OTP ---")
        self.otp_page.clear_otp_field()
        self.otp_page.enter_otp("99999")
        self.otp_page.click_verify_button()
        time.sleep(5)
        
        final_url = self.driver.current_url
        if "home" in final_url.lower() or "dashboard" in final_url.lower():
            print("✓ Correct OTP still works after multiple invalid attempts")
        else:
            print(f"❓ Unexpected result with correct OTP: {final_url}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

