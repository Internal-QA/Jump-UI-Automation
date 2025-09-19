"""
Optimized Configuration for Fast Test Execution
Target: Complete 81 tests in under 1 hour (< 45 seconds per test average)
"""

# Performance Optimizations
FAST_MODE = True
HEADLESS_MODE = True  # Run browsers in headless mode for speed
PARALLEL_WORKERS = 4  # Run tests in parallel

# Timeout Optimizations (reduced from 15+ seconds)
DEFAULT_WAIT_TIMEOUT = 3  # Reduced from 15 seconds
ELEMENT_WAIT_TIMEOUT = 2  # Quick element waits
PAGE_LOAD_TIMEOUT = 5    # Page load timeout
IMPLICIT_WAIT = 1        # Implicit wait

# Session Management
REUSE_BROWSER_SESSION = True  # Reuse browser across tests
LOGIN_ONCE_PER_SESSION = True # Login once and reuse session

# Screenshot Optimization
SCREENSHOTS_ON_FAILURE_ONLY = True
COMPRESS_SCREENSHOTS = True

# Test Optimizations
SKIP_REDUNDANT_VALIDATIONS = True
FAST_ELEMENT_LOCATORS = True
MINIMAL_LOGGING = True

# Chrome Options for Performance
CHROME_OPTIONS = [
    '--headless',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-extensions',
    '--disable-images',
    '--disable-javascript',  # For tests that don't need JS
    '--disable-plugins',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-features=TranslateUI',
    '--disable-web-security',
    '--no-first-run',
    '--fast-start',
    '--disable-default-apps'
]

# Test Categories for Parallel Execution
TEST_GROUPS = {
    'login': ['test_login.py'],
    'otp': ['test_otp.py'], 
    'navigation': ['test_home.py'],
    'portfolio': ['test_portfolio.py'],
    'valuations': ['test_valuations.py']
}
