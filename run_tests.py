#!/usr/bin/env python3
"""
Test runner script for UI automation framework.
Provides options to run tests with different configurations.
"""

import argparse
import os
import sys
import subprocess
from datetime import datetime


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['reports', 'logs', 'screenshots', 'test_data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")


def run_login_tests(browser="chrome", headless=False, verbose=False):
    """Run login tests with specified configuration"""
    print(f"Running login tests with browser: {browser}, headless: {headless}")
    
    # Create directories
    create_directories()
    
    # Build pytest command
    cmd = ["python3", "-m", "pytest", "tests/test_login.py"]
    
    if verbose:
        cmd.extend(["-v", "-s"])
    
    # Add HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"reports/login_test_report_{timestamp}.html"
    cmd.extend(["--html", html_report, "--self-contained-html"])


def run_otp_tests(browser="chrome", headless=False, verbose=False):
    """Run OTP verification tests with specified configuration"""
    print(f"Running OTP tests with browser: {browser}, headless: {headless}")
    
    # Create directories
    create_directories()
    
    # Build pytest command
    cmd = ["python3", "-m", "pytest", "tests/test_otp.py"]
    
    if verbose:
        cmd.extend(["-v", "-s"])
    
    # Add HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"reports/otp_test_report_{timestamp}.html"
    cmd.extend(["--html", html_report, "--self-contained-html"])
    
    # Set environment variables for browser configuration
    env = os.environ.copy()
    if browser.lower() == "firefox":
        env["BROWSER"] = "firefox"
    else:
        env["BROWSER"] = "chrome"
    
    if headless:
        env["HEADLESS"] = "true"
    else:
        env["HEADLESS"] = "false"
    
    # Run tests
    try:
        result = subprocess.run(cmd, env=env, check=False)
        print(f"\nTest execution completed. Exit code: {result.returncode}")
        print(f"HTML Report generated: {html_report}")
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1


def run_all_tests(browser="chrome", headless=False, verbose=False):
    env = os.environ.copy()
    if browser.lower() == "firefox":
        env["BROWSER"] = "firefox"
    else:
        env["BROWSER"] = "chrome"
    
    if headless:
        env["HEADLESS"] = "true"
    else:
        env["HEADLESS"] = "false"
    
    # Run tests
    try:
        result = subprocess.run(cmd, env=env, check=False)
        print(f"\nTest execution completed. Exit code: {result.returncode}")
        print(f"HTML Report generated: {html_report}")
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1


def run_all_tests(browser="chrome", headless=False, verbose=False):
    """Run all tests in the tests directory"""
    print(f"Running all tests with browser: {browser}, headless: {headless}")
    
    # Create directories
    create_directories()
    
    # Build pytest command
    cmd = ["python3", "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.extend(["-v", "-s"])
    
    # Add HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"reports/all_tests_report_{timestamp}.html"
    cmd.extend(["--html", html_report, "--self-contained-html"])
    
    # Set environment variables
    env = os.environ.copy()
    if browser.lower() == "firefox":
        env["BROWSER"] = "firefox"
    else:
        env["BROWSER"] = "chrome"
    
    if headless:
        env["HEADLESS"] = "true"
    else:
        env["HEADLESS"] = "false"
    
    # Run tests
    try:
        result = subprocess.run(cmd, env=env, check=False)
        print(f"\nTest execution completed. Exit code: {result.returncode}")
        print(f"HTML Report generated: {html_report}")
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1


def setup_framework():
    """Setup the framework by installing dependencies and creating directories"""
    print("Setting up UI automation framework...")
    
    # Install dependencies
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    
    # Create directories
    create_directories()
    
    print("Framework setup completed!")
    return True


def main():
    """Main function to parse arguments and run tests"""
    parser = argparse.ArgumentParser(description="UI Automation Test Runner")
    
    parser.add_argument(
        "--setup", 
        action="store_true", 
        help="Setup the framework by installing dependencies and creating directories"
    )
    
    parser.add_argument(
        "--test", 
        choices=["login", "otp", "all"], 
        default="login",
        help="Which tests to run (default: login)"
    )
    
    parser.add_argument(
        "--browser", 
        choices=["chrome", "firefox"], 
        default="chrome",
        help="Browser to use for testing (default: chrome)"
    )
    
    parser.add_argument(
        "--headless", 
        action="store_true", 
        help="Run tests in headless mode"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Run tests with verbose output"
    )
    
    args = parser.parse_args()
    
    if args.setup:
        setup_framework()
        return
    
    print("=" * 60)
    print("UI AUTOMATION TEST FRAMEWORK")
    print("=" * 60)
    print(f"Test Type: {args.test}")
    print(f"Browser: {args.browser}")
    print(f"Headless: {args.headless}")
    print(f"Verbose: {args.verbose}")
    print("=" * 60)
    
    if args.test == "login":
        exit_code = run_login_tests(args.browser, args.headless, args.verbose)
    elif args.test == "otp":
        exit_code = run_otp_tests(args.browser, args.headless, args.verbose)
    elif args.test == "all":
        exit_code = run_all_tests(args.browser, args.headless, args.verbose)
    else:
        print(f"Unknown test type: {args.test}")
        exit_code = 1
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 