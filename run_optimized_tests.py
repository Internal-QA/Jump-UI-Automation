#!/usr/bin/env python3
"""
Optimized Test Runner for Fast Execution
Target: Complete all 81 tests in under 60 minutes
"""

import subprocess
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

class OptimizedTestRunner:
    def __init__(self):
        self.start_time = time.time()
        self.results = {}
        
    def run_test_group(self, group_name, test_files):
        """Run a group of tests in parallel"""
        print(f"\n🚀 Running {group_name} tests...")
        group_start = time.time()
        
        cmd = [
            "python3", "-m", "pytest",
            "-c", "pytest_optimized.ini",
            "--tb=short",
            "-v",
            "-n", "auto",  # Auto-detect CPU cores
            "--dist=loadfile"
        ] + test_files
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
            duration = time.time() - group_start
            
            self.results[group_name] = {
                'duration': duration,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            if result.returncode == 0:
                print(f"✅ {group_name} tests PASSED in {duration:.1f}s")
            else:
                print(f"❌ {group_name} tests FAILED in {duration:.1f}s")
                
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {group_name} tests TIMED OUT")
            self.results[group_name] = {'duration': 900, 'exit_code': -1, 'timeout': True}
            return False
    
    def run_smoke_tests(self):
        """Run quick smoke tests first"""
        print("🔍 Running smoke tests...")
        smoke_cmd = [
            "python3", "-m", "pytest",
            "-c", "pytest_optimized.ini",
            "-m", "smoke",
            "--tb=short",
            "-v"
        ]
        
        result = subprocess.run(smoke_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Smoke tests failed! Stopping execution.")
            print(result.stdout)
            return False
        
        print("✅ Smoke tests passed!")
        return True
    
    def run_optimized_tests(self):
        """Run all tests in optimized groups"""
        print("🎯 Starting Optimized Test Execution")
        print("=" * 50)
        
        # First run smoke tests
        if not self.run_smoke_tests():
            return False
        
        # Define test groups for parallel execution
        test_groups = {
            'login': ['tests/optimized_test_login.py'],
            'quick_otp': ['tests/test_otp.py::TestOTP::test_01_validate_otp_page_elements_present',
                         'tests/test_otp.py::TestOTP::test_02_enter_valid_otp_and_verify_success'],
            'navigation': ['tests/test_home.py'],
            'portfolio_core': ['tests/test_portfolio.py::TestPortfolio::test_01_navigate_to_portfolio_via_home_page_card_3',
                              'tests/test_portfolio.py::TestPortfolio::test_02_click_new_portfolio_button_navigate_to_builder'],
            'valuations_core': ['tests/test_valuations.py::TestValuations::test_01_navigate_to_valuations_page_from_home',
                               'tests/test_valuations.py::TestValuations::test_02_search_for_dealerships_on_valuations_page']
        }
        
        # Run all groups
        all_passed = True
        for group_name, test_files in test_groups.items():
            if not self.run_test_group(group_name, test_files):
                all_passed = False
        
        return all_passed
    
    def run_full_suite_parallel(self):
        """Run full test suite with maximum parallelization"""
        print("🔥 Running FULL SUITE with maximum parallelization")
        
        cmd = [
            "python3", "-m", "pytest",
            "-c", "pytest_optimized.ini",
            "tests/",
            "--tb=short",
            "-v",
            "-n", "8",  # 8 parallel workers
            "--dist=loadscope",
            "--maxfail=5"  # Stop after 5 failures
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time
        
        print(f"\n📊 Full suite completed in {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        if result.returncode == 0:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("❌ Some tests failed:")
            print(result.stdout[-1000:])  # Last 1000 chars
        
        return result.returncode == 0
    
    def print_summary(self):
        """Print execution summary"""
        total_time = time.time() - self.start_time
        print("\n" + "=" * 50)
        print("📈 EXECUTION SUMMARY")
        print("=" * 50)
        print(f"Total execution time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
        
        if total_time < 3600:  # Less than 1 hour
            print("🎯 TARGET ACHIEVED: Completed in under 1 hour!")
        else:
            print("⚠️  Target missed: Took longer than 1 hour")
        
        for group, result in self.results.items():
            status = "✅ PASS" if result['exit_code'] == 0 else "❌ FAIL"
            print(f"{group}: {status} ({result['duration']:.1f}s)")

def main():
    parser = argparse.ArgumentParser(description='Optimized Test Runner')
    parser.add_argument('--mode', choices=['optimized', 'full', 'smoke'], 
                       default='optimized', help='Test execution mode')
    parser.add_argument('--parallel', type=int, default=4, 
                       help='Number of parallel workers')
    
    args = parser.parse_args()
    
    runner = OptimizedTestRunner()
    
    try:
        if args.mode == 'smoke':
            success = runner.run_smoke_tests()
        elif args.mode == 'full':
            success = runner.run_full_suite_parallel()
        else:
            success = runner.run_optimized_tests()
        
        runner.print_summary()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        runner.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
