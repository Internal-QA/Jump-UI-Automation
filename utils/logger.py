import logging
import os
from datetime import datetime
import json


class TestLogger:
    """Custom logger for UI automation tests"""
    
    def __init__(self, log_file_path=None, log_level=logging.INFO):
        """Initialize TestLogger with optional log file path and level"""
        self.log_level = log_level
        
        if log_file_path is None:
            # Create logs directory if it doesn't exist
            logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)
            
            # Create log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file_path = os.path.join(logs_dir, f"test_execution_{timestamp}.log")
        else:
            self.log_file_path = log_file_path
        
        self.setup_logger()
    
    def setup_logger(self):
        """Set up the logger with file and console handlers"""
        # Create logger
        self.logger = logging.getLogger('UIAutomationLogger')
        self.logger.setLevel(self.log_level)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Log initial setup message
        self.logger.info(f"Logger initialized. Log file: {self.log_file_path}")
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_test_start(self, test_name):
        """Log test start"""
        self.logger.info(f"{'='*50}")
        self.logger.info(f"STARTING TEST: {test_name}")
        self.logger.info(f"{'='*50}")
    
    def log_test_end(self, test_name, status):
        """Log test end with status"""
        self.logger.info(f"{'='*50}")
        self.logger.info(f"FINISHED TEST: {test_name} - STATUS: {status}")
        self.logger.info(f"{'='*50}")
    
    def log_step(self, step_description):
        """Log test step"""
        self.logger.info(f"STEP: {step_description}")
    
    def log_assertion(self, assertion_description, result):
        """Log assertion with result"""
        status = "PASSED" if result else "FAILED"
        self.logger.info(f"ASSERTION: {assertion_description} - {status}")
    
    def log_screenshot(self, screenshot_path):
        """Log screenshot capture"""
        self.logger.info(f"SCREENSHOT: {screenshot_path}")
    
    def log_page_navigation(self, url):
        """Log page navigation"""
        self.logger.info(f"NAVIGATING TO: {url}")
    
    def log_element_interaction(self, action, element_locator):
        """Log element interaction"""
        self.logger.info(f"ACTION: {action} on element: {element_locator}")
    
    def log_test_data(self, data_description, data):
        """Log test data"""
        self.logger.debug(f"TEST DATA ({data_description}): {json.dumps(data, indent=2)}")
    
    def log_exception(self, exception, context=""):
        """Log exception with context"""
        if context:
            self.logger.error(f"EXCEPTION in {context}: {str(exception)}")
        else:
            self.logger.error(f"EXCEPTION: {str(exception)}")
    
    def close(self):
        """Close all handlers"""
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)


# Global logger instance
test_logger = None

def get_logger(log_file_path=None, log_level=logging.INFO):
    """Get global logger instance"""
    global test_logger
    if test_logger is None:
        test_logger = TestLogger(log_file_path, log_level)
    return test_logger 