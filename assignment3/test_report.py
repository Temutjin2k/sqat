import unittest
import HtmlTestRunner
import os
import sys

from assignment3.actions_class import ActionChainsTests
from assignment3.select_class import SelectClassTests
from assignment3.waits import WebWaitTests

sys.path.append(os.getcwd())

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    # Load tests from both test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(WebWaitTests))
    suite.addTests(loader.loadTestsFromTestCase(ActionChainsTests))
    suite.addTests(loader.loadTestsFromTestCase(SelectClassTests))
    
    report_dir = os.path.join(os.getcwd(), "reports")
    
    print("Starting tests execution...")
    print("Report will be generated in: " + report_dir)
    
    # Initialize the HTML Test Runner
    runner = HtmlTestRunner.HTMLTestRunner(
        output=report_dir,
        report_name="SQAT_Test_Report",
        report_title="Assignment 3 - Selenium Test Execution Report",
        combine_reports=True,
        add_timestamp=True
    )
    
    # Run the suite
    runner.run(suite)
    print("\nTest Execution Completed!")
