import pytest
import yaml
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime


class BaseTest:
    """Base test class for common test setup and teardown"""
    
    # Class variables to store data across test methods
    stored_financials_data = {}
    
    @classmethod
    def setup_class(cls):
        """Setup class method - runs once per test class"""
        cls.load_config()
    
    @classmethod
    def load_config(cls):
        """Load configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        try:
            with open(config_path, 'r') as file:
                cls.config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file not found at: {config_path}")
            cls.config = cls.get_default_config()
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            cls.config = cls.get_default_config()
    
    @classmethod
    def get_default_config(cls):
        """Return default configuration if config file is not found"""
        return {
            'base_url': 'https://valueinsightpro.jumpiq.com',
            'login_url': 'https://valueinsightpro.jumpiq.com/auth/login',
            'timeouts': {
                'implicit_wait': 10,
                'explicit_wait': 20,
                'page_load_timeout': 30
            },
            'browser': {
                'default': 'chrome',
                'headless': False,
                'window_size': '1920,1080'
            },
            'test_data': {
                'screenshot_on_failure': True,
                'report_path': 'reports/',
                'screenshot_path': 'screenshots/'
            }
        }
    

    
    def teardown_method(self, method):
        """Teardown method - runs after each test method"""
        if hasattr(self, 'driver') and self.driver:
            try:
                # Take screenshot on failure if configured
                if (self.config['test_data']['screenshot_on_failure'] and 
                    hasattr(self, '_test_failed') and self._test_failed):
                    self.take_failure_screenshot(method.__name__)
                
                self.driver.quit()
                print(f"Completed test: {method.__name__}")
            except Exception as e:
                print(f"Error during teardown: {str(e)}")
    
    def create_driver(self):
        """Create and return a WebDriver instance"""
        # Check environment variables for browser and headless mode
        browser = os.environ.get('BROWSER', self.config['browser']['default']).lower()
        headless = os.environ.get('HEADLESS', 'false').lower() == 'true'
        
        # Update config with environment variables
        self.config['browser']['default'] = browser
        self.config['browser']['headless'] = headless
        
        if browser == 'chrome':
            return self.create_chrome_driver()
        elif browser == 'firefox':
            return self.create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def create_chrome_driver(self):
        """Create and return Chrome WebDriver"""
        chrome_options = ChromeOptions()
        
        # Add common Chrome options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set window size
        window_size = self.config['browser']['window_size']
        chrome_options.add_argument(f"--window-size={window_size}")
        
        # Set headless mode if configured
        if self.config['browser']['headless']:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
        
        # Create Chrome driver using WebDriverManager with error handling for macOS ARM
        try:
            driver_path = ChromeDriverManager().install()
            
            # Fix for macOS ARM ChromeDriver issue
            import platform
            if platform.system() == 'Darwin' and platform.machine() == 'arm64':
                # Check if the driver path points to the wrong file
                driver_dir = os.path.dirname(driver_path)
                actual_chromedriver = os.path.join(driver_dir, 'chromedriver')
                if os.path.exists(actual_chromedriver) and not driver_path.endswith('chromedriver'):
                    driver_path = actual_chromedriver
                    print(f"Fixed ChromeDriver path for macOS ARM: {driver_path}")
            
            service = ChromeService(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to hide automation flags
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
            
        except Exception as e:
            print(f"Error creating Chrome driver: {str(e)}")
            print("Attempting to use system ChromeDriver...")
            # Fallback to system ChromeDriver
            service = ChromeService()
            return webdriver.Chrome(service=service, options=chrome_options)
    
    def create_firefox_driver(self):
        """Create and return Firefox WebDriver"""
        firefox_options = FirefoxOptions()
        
        # Set headless mode if configured
        if self.config['browser']['headless']:
            firefox_options.add_argument("--headless")
        
        # Create Firefox driver using WebDriverManager
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        # Set window size
        window_size = self.config['browser']['window_size'].split(',')
        driver.set_window_size(int(window_size[0]), int(window_size[1]))
        
        return driver
    
    def configure_driver(self):
        """Configure driver with timeouts and other settings"""
        # Set timeouts
        self.driver.implicitly_wait(self.config['timeouts']['implicit_wait'])
        self.driver.set_page_load_timeout(self.config['timeouts']['page_load_timeout'])
        
        # Maximize window if not headless
        if not self.config['browser']['headless']:
            self.driver.maximize_window()
    
    def take_failure_screenshot(self, test_name):
        """Take a screenshot when test fails"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = self.config['test_data']['screenshot_path']
        
        # Create directory if it doesn't exist
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        screenshot_path = os.path.join(screenshot_dir, f"FAILED_{test_name}_{timestamp}.png")
        try:
            self.driver.save_screenshot(screenshot_path)
            print(f"Failure screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Error taking failure screenshot: {str(e)}")
    
    def setup_method(self, method):
        """Setup method - runs before each test method"""
        self.driver = self.create_driver()
        self.configure_driver()
        self._test_failed = False
        print(f"Starting test: {method.__name__}")
    
    def get_config(self):
        """Get current configuration"""
        return self.config 