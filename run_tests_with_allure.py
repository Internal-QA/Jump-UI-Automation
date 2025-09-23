#!/usr/bin/env python3
"""
Test Runner with Allure Report Generation
Runs all tests and generates comprehensive Allure reports
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def run_tests_with_allure():
    """Run tests and generate Allure reports"""
    
    print("SUCCESS: RUNNING TESTS WITH ALLURE REPORTING")
    print("=" * 50)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Clean previous results
    if os.path.exists('allure-results'):
        subprocess.run(['rm', '-rf', 'allure-results'])
    if os.path.exists('allure-report'):
        subprocess.run(['rm', '-rf', 'allure-report'])
    
    start_time = time.time()
    
    # Run tests with Allure
    print("\nEXPERIMENT: Running tests with Allure reporting...")
    
    cmd = [
        'python3', '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short',
        '--alluredir=allure-results',
        '--clean-alluredir'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        execution_time = time.time() - start_time
        
        print(f"⏱️  Test execution completed in {execution_time:.1f}s")
        
        # Parse results
        passed = result.stdout.count('PASSED')
        failed = result.stdout.count('FAILED')
        total = passed + failed
        
        print(f"DATA: Test Results: {passed} passed, {failed} failed ({total} total)")
        
        if result.returncode == 0:
            print("PASS: All tests PASSED")
        else:
            print("FAIL: Some tests FAILED")
            print("Last few lines of output:")
            print(result.stdout[-500:])
        
        # Generate Allure report
        print("\nDATA: Generating Allure report...")
        
        report_cmd = ['allure', 'generate', 'allure-results', '-o', 'allure-report', '--clean']
        
        try:
            subprocess.run(report_cmd, check=True, capture_output=True)
            print("PASS: Allure report generated successfully")
            print("📁 Report location: allure-report/index.html")
            
            # Try to open report
            try:
                subprocess.run(['allure', 'open', 'allure-report'], timeout=2)
            except:
                print("INFO: To view report: allure open allure-report")
                
        except subprocess.CalledProcessError:
            print("FAIL: Allure report generation failed")
            print("INFO: Make sure Allure is installed: npm install -g allure-commandline")
        except FileNotFoundError:
            print("FAIL: Allure command not found")
            print("INFO: Install Allure: npm install -g allure-commandline")
        
        print(f"\n🏁 Total execution time: {execution_time:.1f}s ({execution_time/60:.1f} minutes)")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"💥 Error running tests: {e}")
        return False

if __name__ == "__main__":
    try:
        success = run_tests_with_allure()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test execution interrupted")
        sys.exit(1)
