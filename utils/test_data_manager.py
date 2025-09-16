import json
import os
import yaml
from typing import Dict, List, Any


class DataManager:
    """Class to manage test data for UI automation tests"""
    
    def __init__(self, data_file_path=None):
        """Initialize TestDataManager with optional data file path"""
        if data_file_path is None:
            # Default to test_data.json in the same directory
            self.data_file_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'test_data.json')
        else:
            self.data_file_path = data_file_path
        
        # Path to main config file for credentials
        self.config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        
        self.test_data = self.load_test_data()
        self.config_credentials = self.load_config_credentials()
    
    def load_test_data(self) -> Dict[str, Any]:
        """Load test data from JSON file"""
        try:
            if os.path.exists(self.data_file_path):
                with open(self.data_file_path, 'r') as file:
                    data = json.load(file)
                    print(f"Test data loaded from: {self.data_file_path}")
                    return data
            else:
                print(f"Test data file not found at: {self.data_file_path}")
                return self.get_default_test_data()
        except Exception as e:
            print(f"Error loading test data: {str(e)}")
            return self.get_default_test_data()
    
    def get_default_test_data(self) -> Dict[str, Any]:
        """Return default test data structure"""
        return {
            "login_credentials": {
                "valid_user": {
                    "email": "test3",
                    "password": "value@123"
                },
                "invalid_user": {
                    "email": "invalid@example.com",
                    "password": "WrongPassword"
                },
                "empty_credentials": {
                    "email": "",
                    "password": ""
                }
            },
            "test_scenarios": {
                "positive_tests": [
                    {
                        "test_name": "valid_login",
                        "description": "Login with valid credentials",
                        "email": "test3",
                        "password": "value@123",
                        "accept_terms": True,
                        "expected_result": "success"
                    }
                ],
                "negative_tests": [
                    {
                        "test_name": "invalid_email",
                        "description": "Login with invalid email",
                        "email": "invalid@example.com",
                        "password": "value@123",
                        "accept_terms": True,
                        "expected_result": "failure"
                    },
                    {
                        "test_name": "invalid_password",
                        "description": "Login with invalid password",
                        "email": "test3",
                        "password": "WrongPassword",
                        "accept_terms": True,
                        "expected_result": "failure"
                    },
                    {
                        "test_name": "empty_email",
                        "description": "Login with empty email",
                        "email": "",
                        "password": "value@123",
                        "accept_terms": True,
                        "expected_result": "failure"
                    },
                    {
                        "test_name": "empty_password",
                        "description": "Login with empty password",
                        "email": "test3",
                        "password": "",
                        "accept_terms": True,
                        "expected_result": "failure"
                    },
                    {
                        "test_name": "terms_not_accepted",
                        "description": "Login without accepting terms",
                        "email": "test3",
                        "password": "value@123",
                        "accept_terms": False,
                        "expected_result": "failure"
                    }
                ]
            },
            "expected_messages": {
                "login_success": "Login successful",
                "invalid_credentials": "Invalid credentials",
                "empty_email": "Email is required",
                "empty_password": "Password is required",
                "terms_required": "Please accept terms and conditions"
            }
        }
    
    def load_config_credentials(self) -> Dict[str, Any]:
        """Load credentials from main config file"""
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r') as file:
                    config_data = yaml.safe_load(file)
                    credentials = config_data.get('credentials', {})
                    if credentials:
                        print(f"Credentials loaded from config file: {self.config_file_path}")
                        return credentials
            print("No credentials found in config file, using test data defaults")
            return {}
        except Exception as e:
            print(f"Error loading credentials from config: {str(e)}")
            return {}
    
    def get_login_credentials(self, user_type: str) -> Dict[str, str]:
        """Get login credentials for specific user type - check config file first, then test data"""
        try:
            # First, try to get credentials from config file
            if self.config_credentials and user_type in self.config_credentials:
                print(f"Using credentials from config file for: {user_type}")
                return self.config_credentials[user_type]
            
            # Fallback to test data file
            print(f"Using credentials from test data for: {user_type}")
            return self.test_data["login_credentials"][user_type]
        except KeyError:
            print(f"User type '{user_type}' not found in either config or test data")
            # Return valid_user as ultimate fallback
            if self.config_credentials and "valid_user" in self.config_credentials:
                return self.config_credentials["valid_user"]
            return self.test_data["login_credentials"]["valid_user"]
    
    def get_test_scenarios(self, scenario_type: str) -> List[Dict[str, Any]]:
        """Get test scenarios by type (positive_tests, negative_tests)"""
        try:
            return self.test_data["test_scenarios"][scenario_type]
        except KeyError:
            print(f"Scenario type '{scenario_type}' not found in test data")
            return []
    
    def get_expected_message(self, message_type: str) -> str:
        """Get expected message for specific type"""
        try:
            return self.test_data["expected_messages"][message_type]
        except KeyError:
            print(f"Message type '{message_type}' not found in test data")
            return ""
    
    def add_test_scenario(self, scenario_type: str, scenario: Dict[str, Any]):
        """Add a new test scenario"""
        if scenario_type not in self.test_data["test_scenarios"]:
            self.test_data["test_scenarios"][scenario_type] = []
        
        self.test_data["test_scenarios"][scenario_type].append(scenario)
        print(f"Added new scenario '{scenario.get('test_name', 'unknown')}' to {scenario_type}")
    
    def save_test_data(self):
        """Save current test data to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
            
            with open(self.data_file_path, 'w') as file:
                json.dump(self.test_data, file, indent=4)
            print(f"Test data saved to: {self.data_file_path}")
            return True
        except Exception as e:
            print(f"Error saving test data: {str(e)}")
            return False
    
    def get_all_test_data(self) -> Dict[str, Any]:
        """Get all test data"""
        return self.test_data
    
    def update_credentials(self, user_type: str, email: str, password: str):
        """Update credentials for a specific user type"""
        if "login_credentials" not in self.test_data:
            self.test_data["login_credentials"] = {}
        
        self.test_data["login_credentials"][user_type] = {
            "email": email,
            "password": password
        }
        print(f"Updated credentials for user type: {user_type}")
    
    def create_test_data_file(self):
        """Create test data file with default data"""
        self.test_data = self.get_default_test_data()
        return self.save_test_data() 