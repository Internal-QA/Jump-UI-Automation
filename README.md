# Jump UI Automation Framework

A comprehensive, reusable, and dynamic UI automation framework built with Python, Selenium, and pytest. This framework provides a solid foundation for automated testing of web applications with a focus on maintainability, scalability, and ease of use.

## Features

- **Page Object Model**: Clean separation of page elements and actions
- **Dynamic Element Handling**: Robust element location and interaction
- **Comprehensive Reporting**: HTML and JSON reports with screenshots
- **Detailed Logging**: Structured logging for debugging and analysis
- **Configuration Management**: YAML-based configuration for easy customization
- **Test Data Management**: JSON-based test data with easy manipulation
- **Cross-Browser Support**: Chrome and Firefox browser support
- **Headless Execution**: Support for headless browser execution
- **Screenshot Capture**: Automatic screenshots on test failures
- **Parallel Execution Ready**: Framework designed for parallel test execution

## Project Structure

```
Jump-UI-Automation/
├── base/
│   ├── base_page.py          # Base page class with common methods
│   └── base_test.py          # Base test class with setup/teardown
├── config/
│   └── config.yaml           # Configuration settings
├── pages/
│   └── login_page.py         # Login page object
├── tests/
│   └── test_login.py         # Login test cases
├── utils/
│   ├── logger.py             # Logging utilities
│   ├── report_generator.py   # HTML report generation
│   └── test_data_manager.py  # Test data management
├── test_data/
│   └── test_data.json        # Test data and scenarios
├── logs/                     # Test execution logs
├── reports/                  # Test reports (HTML/JSON)
├── screenshots/              # Test screenshots
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── run_tests.py              # Test runner script
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Chrome or Firefox browser

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Jump-UI-Automation
   ```

2. **Set up the framework:**
   ```bash
   python run_tests.py --setup
   ```
   
   This will:
   - Install all required Python dependencies
   - Create necessary directories (logs, reports, screenshots)

3. **Verify installation:**
   ```bash
   python run_tests.py --test login --verbose
   ```

### Quick Start

**Run login tests with Chrome (default):**
```bash
python run_tests.py --test login
```

**Run tests with Firefox in headless mode:**
```bash
python run_tests.py --test login --browser firefox --headless
```

**Run all tests with verbose output:**
```bash
python run_tests.py --test all --verbose
```

## Configuration

### Browser Configuration (`config/config.yaml`)

```yaml
base_url: "https://valueinsightpro.jumpiq.com"
login_url: "https://valueinsightpro.jumpiq.com/auth/login"
otp_url: "https://valueinsightpro.jumpiq.com/auth/otp-verify"

timeouts:
  implicit_wait: 10
  explicit_wait: 20
  page_load_timeout: 30

browser:
  default: "chrome"        # chrome or firefox
  headless: false          # true for headless execution
  window_size: "1920,1080"

test_data:
  screenshot_on_failure: true
  report_path: "reports/"
  screenshot_path: "screenshots/"
```

### Test Data (`test_data/test_data.json`)

```json
{
    "login_credentials": {
        "valid_user": {
            "email": "test@example.com",
            "password": "TestPassword123"
        },
        "invalid_user": {
            "email": "invalid@example.com",
            "password": "WrongPassword"
        }
    }
}
```

## Login Page Test Implementation

### Page Elements

The login page contains the following elements tested by the framework:

- **Email Field**: `//input[@id='company-email']`
- **Password Field**: `//span[@class='ant-input-affix-wrapper css-bixahu ant-input-outlined ant-input-password input']//input[@type='password']`
- **Terms Checkbox**: `//input[@type='checkbox']`
- **Sign In Button**: `//button[normalize-space()='Sign In']`

### Test Scenarios

The framework includes comprehensive test coverage:

1. **Valid Login Test** - Tests successful login with valid credentials and validates redirect to OTP verification page
2. **Invalid Email Test** - Tests login rejection with invalid email
3. **Empty Email Test** - Tests validation for empty email field
4. **Empty Password Test** - Tests validation for empty password field
5. **Terms Not Accepted Test** - Tests login rejection without accepting terms
6. **Login Page Elements Test** - Verifies all required elements are present
7. **Clear Login Form Test** - Tests form clearing functionality
8. **OTP Redirect Test** - Specifically validates successful login redirects to OTP verification page

### Error Message Validation

The framework validates specific error messages from the application:
- **Invalid Credentials**: "Invalid username or password"
- **Missing Fields**: "Both username and password are required"

### Usage Example

```python
from pages.login_page import LoginPage
from base.base_test import BaseTest

class TestLogin(BaseTest):
    def test_valid_login(self):
        login_page = LoginPage(self.driver, self.config)
        
        # Navigate to login page
        assert login_page.navigate_to_login_page()
        
        # Perform login
        success = login_page.perform_login(
            email="test@example.com",
            password="TestPassword123",
            accept_terms=True
        )
        assert success
```

## Framework Components

### Base Classes

**BasePage** (`base/base_page.py`)
- Common web element interactions
- Wait strategies and timeouts
- Screenshot capture
- Navigation utilities

**BaseTest** (`base/base_test.py`)
- Browser setup and teardown
- Configuration loading
- WebDriver management
- Test failure handling

### Page Objects

**LoginPage** (`pages/login_page.py`)
- Login-specific element locators
- Login flow methods
- Form validation checks
- Page state verification

### Utilities

**TestLogger** (`utils/logger.py`)
- Structured logging
- Test step tracking
- Error logging
- Console and file output

**TestReportGenerator** (`utils/report_generator.py`)
- HTML report generation
- Test execution summaries
- Screenshot integration
- Interactive report features

**TestDataManager** (`utils/test_data_manager.py`)
- JSON test data loading
- Credential management
- Test scenario handling
- Data file creation

## Running Tests

### Command Line Options

```bash
python run_tests.py [OPTIONS]

Options:
  --setup              Setup framework (install dependencies)
  --test {login,all}   Which tests to run (default: login)
  --browser {chrome,firefox}  Browser to use (default: chrome)
  --headless           Run in headless mode
  --verbose            Verbose output
```

### Using pytest directly

```bash
# Run login tests
pytest tests/test_login.py -v

# Run specific test
pytest tests/test_login.py::TestLogin::test_valid_login -v

# Run with custom markers
pytest -m "login" -v

# Generate HTML report
pytest tests/test_login.py --html=reports/custom_report.html --self-contained-html
```

## Reports and Logging

### HTML Reports

The framework generates comprehensive HTML reports with:
- Test execution summary
- Individual test results
- Screenshots for failed tests
- Test step details
- Interactive features

Reports are saved in the `reports/` directory.

### Logging

Detailed logs are generated for each test run:
- Test execution flow
- Element interactions
- Assertions and validations
- Error messages and stack traces

Logs are saved in the `logs/` directory.

### Screenshots

Screenshots are automatically captured:
- On test failures
- When explicitly requested
- For specific test steps

Screenshots are saved in the `screenshots/` directory.

## Extending the Framework

### Adding New Pages

1. Create a new page class inheriting from `BasePage`
2. Define element locators and page-specific methods
3. Add the page to your test classes

```python
from base.base_page import BasePage

class NewPage(BasePage):
    # Element locators
    ELEMENT_LOCATOR = ("xpath", "//element[@id='example']")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
    
    def perform_action(self):
        return self.click_element(
            self.ELEMENT_LOCATOR[0], 
            self.ELEMENT_LOCATOR[1]
        )
```

### Adding New Tests

1. Create test methods in the appropriate test class
2. Use the test data manager for test data
3. Implement proper assertions and logging

```python
def test_new_functionality(self):
    self.add_test_step("Starting new functionality test")
    
    # Test implementation
    result = self.page.perform_action()
    assert result, "Action failed"
    
    self.add_test_step("New functionality test completed")
```

### Customizing Configuration

Modify `config/config.yaml` to adjust:
- Browser settings
- Timeout values
- URL configurations
- Reporting preferences

## Best Practices

1. **Use Page Object Model** - Keep page elements and actions in page classes
2. **Implement Proper Waits** - Use explicit waits for element interactions
3. **Add Meaningful Assertions** - Verify expected behavior at each step
4. **Use Test Data Files** - Externalize test data for maintainability
5. **Implement Proper Logging** - Log test steps and important actions
6. **Take Screenshots** - Capture screenshots for debugging failures
7. **Keep Tests Independent** - Each test should be able to run independently

## Troubleshooting

### Common Issues

1. **WebDriver Issues**
   - Ensure Chrome/Firefox is installed
   - Check WebDriver compatibility with browser version

2. **Element Not Found**
   - Verify element locators are correct
   - Check if page has loaded completely
   - Increase wait timeouts if needed

3. **Test Failures**
   - Check logs for detailed error messages
   - Review screenshots for visual debugging
   - Verify test data and configuration

### Debug Mode

Run tests with maximum verbosity:
```bash
python run_tests.py --test login --verbose
```

Enable debug logging in your test:
```python
import logging
logger = get_logger(log_level=logging.DEBUG)
```

## Contributing

1. Follow the existing code structure and patterns
2. Add proper documentation and comments
3. Include test cases for new features
4. Update this README when adding new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review logs and reports for detailed information
3. Create an issue in the project repository

---

**Happy Testing! 🚀**
