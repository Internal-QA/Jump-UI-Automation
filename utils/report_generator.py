import json
import os
from datetime import datetime
from typing import List, Dict, Any


class ReportGenerator:
    """Generate HTML test reports for UI automation"""
    
    def __init__(self, report_dir=None):
        """Initialize report generator with optional report directory"""
        if report_dir is None:
            self.report_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        else:
            self.report_dir = report_dir
        
        # Create reports directory if it doesn't exist
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
        
        self.test_results = []
        self.execution_summary = {
            'start_time': None,
            'end_time': None,
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def start_execution(self):
        """Mark the start of test execution"""
        self.execution_summary['start_time'] = datetime.now()
    
    def end_execution(self):
        """Mark the end of test execution"""
        self.execution_summary['end_time'] = datetime.now()
    
    def add_test_result(self, test_name: str, status: str, duration: float = 0.0, 
                       error_message: str = None, screenshot_path: str = None, 
                       test_steps: List[str] = None):
        """Add a test result to the report"""
        test_result = {
            'test_name': test_name,
            'status': status.lower(),
            'duration': duration,
            'error_message': error_message,
            'screenshot_path': screenshot_path,
            'test_steps': test_steps or [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.test_results.append(test_result)
        
        # Update summary
        self.execution_summary['total_tests'] += 1
        if status.lower() == 'passed':
            self.execution_summary['passed'] += 1
        elif status.lower() == 'failed':
            self.execution_summary['failed'] += 1
        elif status.lower() == 'skipped':
            self.execution_summary['skipped'] += 1
    
    def generate_html_report(self, report_name="test_report"):
        """Generate HTML test report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{report_name}_{timestamp}.html"
        report_path = os.path.join(self.report_dir, report_filename)
        
        html_content = self._create_html_content()
        
        try:
            with open(report_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            print(f"HTML report generated: {report_path}")
            return report_path
        except Exception as e:
            print(f"Error generating HTML report: {str(e)}")
            return None
    
    def _create_html_content(self):
        """Create HTML content for the report"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Automation Test Report</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>UI Automation Test Report</h1>
            <div class="report-info">
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Execution Time:</strong> {self._get_execution_duration()}</p>
            </div>
        </div>
        
        <div class="summary">
            <h2>Execution Summary</h2>
            <div class="summary-cards">
                <div class="card total">
                    <h3>Total Tests</h3>
                    <span class="count">{self.execution_summary['total_tests']}</span>
                </div>
                <div class="card passed">
                    <h3>Passed</h3>
                    <span class="count">{self.execution_summary['passed']}</span>
                </div>
                <div class="card failed">
                    <h3>Failed</h3>
                    <span class="count">{self.execution_summary['failed']}</span>
                </div>
                <div class="card skipped">
                    <h3>Skipped</h3>
                    <span class="count">{self.execution_summary['skipped']}</span>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {self._get_success_percentage()}%"></div>
            </div>
            <p class="success-rate">Success Rate: {self._get_success_percentage():.1f}%</p>
        </div>
        
        <div class="test-results">
            <h2>Test Results</h2>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Timestamp</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_test_rows()}
                </tbody>
            </table>
        </div>
        
        {self._generate_test_details()}
    </div>
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
"""
        return html
    
    def _get_css_styles(self):
        """Get CSS styles for the HTML report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .header h1 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .report-info p {
            margin: 5px 0;
            color: #666;
        }
        
        .summary {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .summary h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            color: white;
        }
        
        .card.total { background: #3498db; }
        .card.passed { background: #27ae60; }
        .card.failed { background: #e74c3c; }
        .card.skipped { background: #f39c12; }
        
        .card h3 {
            font-size: 14px;
            margin-bottom: 10px;
            opacity: 0.9;
        }
        
        .card .count {
            font-size: 32px;
            font-weight: bold;
        }
        
        .progress-bar {
            background: #ecf0f1;
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        
        .progress-fill {
            background: #27ae60;
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .success-rate {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .test-results {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .test-results h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .results-table th,
        .results-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .results-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .status {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .status.passed { background: #d4edda; color: #155724; }
        .status.failed { background: #f8d7da; color: #721c24; }
        .status.skipped { background: #fff3cd; color: #856404; }
        
        .btn {
            padding: 6px 12px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .btn:hover {
            background: #0056b3;
        }
        
        .test-detail {
            background: white;
            padding: 20px;
            margin: 10px 0;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: none;
        }
        
        .test-detail.show {
            display: block;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
            font-family: monospace;
        }
        
        .screenshot {
            margin: 15px 0;
        }
        
        .screenshot img {
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 4px;
        }
        
        .test-steps {
            margin: 15px 0;
        }
        
        .test-steps ol {
            padding-left: 20px;
        }
        
        .test-steps li {
            margin: 5px 0;
            padding: 5px;
            background: #f8f9fa;
            border-radius: 3px;
        }
        """
    
    def _generate_test_rows(self):
        """Generate table rows for test results"""
        rows = ""
        for i, test in enumerate(self.test_results):
            status_class = test['status']
            rows += f"""
                <tr>
                    <td>{test['test_name']}</td>
                    <td><span class="status {status_class}">{test['status']}</span></td>
                    <td>{test['duration']:.2f}s</td>
                    <td>{test['timestamp']}</td>
                    <td>
                        <button class="btn" onclick="toggleDetails({i})">View Details</button>
                    </td>
                </tr>
            """
        return rows
    
    def _generate_test_details(self):
        """Generate detailed test result sections"""
        details = ""
        for i, test in enumerate(self.test_results):
            details += f"""
                <div id="detail-{i}" class="test-detail">
                    <h3>Test Details: {test['test_name']}</h3>
                    <p><strong>Status:</strong> <span class="status {test['status']}">{test['status']}</span></p>
                    <p><strong>Duration:</strong> {test['duration']:.2f} seconds</p>
                    <p><strong>Timestamp:</strong> {test['timestamp']}</p>
                    
                    {self._format_error_message(test['error_message'])}
                    {self._format_screenshot(test['screenshot_path'])}
                    {self._format_test_steps(test['test_steps'])}
                </div>
            """
        return details
    
    def _format_error_message(self, error_message):
        """Format error message for display"""
        if error_message:
            return f'<div class="error-message"><strong>Error:</strong><br>{error_message}</div>'
        return ""
    
    def _format_screenshot(self, screenshot_path):
        """Format screenshot for display"""
        if screenshot_path and os.path.exists(screenshot_path):
            return f'<div class="screenshot"><strong>Screenshot:</strong><br><img src="{screenshot_path}" alt="Test Screenshot"></div>'
        return ""
    
    def _format_test_steps(self, test_steps):
        """Format test steps for display"""
        if test_steps:
            steps_html = "<ol>"
            for step in test_steps:
                steps_html += f"<li>{step}</li>"
            steps_html += "</ol>"
            return f'<div class="test-steps"><strong>Test Steps:</strong>{steps_html}</div>'
        return ""
    
    def _get_execution_duration(self):
        """Get execution duration as formatted string"""
        if self.execution_summary['start_time'] and self.execution_summary['end_time']:
            duration = self.execution_summary['end_time'] - self.execution_summary['start_time']
            return str(duration).split('.')[0]  # Remove microseconds
        return "N/A"
    
    def _get_success_percentage(self):
        """Calculate success percentage"""
        if self.execution_summary['total_tests'] == 0:
            return 0
        return (self.execution_summary['passed'] / self.execution_summary['total_tests']) * 100
    
    def _get_javascript(self):
        """Get JavaScript for interactive features"""
        return """
        function toggleDetails(index) {
            const detail = document.getElementById('detail-' + index);
            if (detail.classList.contains('show')) {
                detail.classList.remove('show');
            } else {
                // Hide all other details
                const allDetails = document.querySelectorAll('.test-detail');
                allDetails.forEach(d => d.classList.remove('show'));
                // Show current detail
                detail.classList.add('show');
                detail.scrollIntoView({behavior: 'smooth'});
            }
        }
        """
    
    def export_json_report(self, report_name="test_report"):
        """Export test results as JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"{report_name}_{timestamp}.json"
        json_path = os.path.join(self.report_dir, json_filename)
        
        report_data = {
            'execution_summary': self.execution_summary,
            'test_results': self.test_results,
            'generated_at': datetime.now().isoformat()
        }
        
        try:
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(report_data, file, indent=4, default=str)
            print(f"JSON report exported: {json_path}")
            return json_path
        except Exception as e:
            print(f"Error exporting JSON report: {str(e)}")
            return None 