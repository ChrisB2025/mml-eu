"""
MML Europe Website - Complete Test Suite Runner
Runs all test suites: responsive, navigation, forms, interactive, screenshots
"""
import sys
import json
from datetime import datetime

# Add the tests directory to the path
sys.path.insert(0, "C:/Dev/Claude/MML EU/tests")

from test_responsive import run_responsive_tests
from test_navigation import run_navigation_tests
from test_forms import run_form_tests
from test_interactive import run_interactive_tests
from test_screenshots import run_screenshot_capture

def run_all_tests():
    """Run all test suites and generate a summary report."""

    print("\n" + "="*70)
    print("MML EUROPE WEBSITE - COMPLETE TEST SUITE")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: https://mml-eu-production.up.railway.app")
    print("="*70)

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "target_url": "https://mml-eu-production.up.railway.app",
        "suites": {}
    }

    total_passed = 0
    total_failed = 0

    # 1. Responsive Design Tests
    print("\n\n" + "#"*70)
    print("# SUITE 1: RESPONSIVE DESIGN TESTS")
    print("#"*70)
    try:
        responsive_results = run_responsive_tests()
        all_results["suites"]["responsive"] = responsive_results
        total_passed += responsive_results["passed"]
        total_failed += responsive_results["failed"]
    except Exception as e:
        print(f"ERROR running responsive tests: {e}")
        all_results["suites"]["responsive"] = {"error": str(e)}

    # 2. Navigation Tests
    print("\n\n" + "#"*70)
    print("# SUITE 2: NAVIGATION TESTS")
    print("#"*70)
    try:
        navigation_results = run_navigation_tests()
        all_results["suites"]["navigation"] = navigation_results
        total_passed += navigation_results["passed"]
        total_failed += navigation_results["failed"]
    except Exception as e:
        print(f"ERROR running navigation tests: {e}")
        all_results["suites"]["navigation"] = {"error": str(e)}

    # 3. Form Functionality Tests
    print("\n\n" + "#"*70)
    print("# SUITE 3: FORM FUNCTIONALITY TESTS")
    print("#"*70)
    try:
        form_results = run_form_tests()
        all_results["suites"]["forms"] = form_results
        total_passed += form_results["passed"]
        total_failed += form_results["failed"]
    except Exception as e:
        print(f"ERROR running form tests: {e}")
        all_results["suites"]["forms"] = {"error": str(e)}

    # 4. Interactive Elements Tests
    print("\n\n" + "#"*70)
    print("# SUITE 4: INTERACTIVE ELEMENTS TESTS")
    print("#"*70)
    try:
        interactive_results = run_interactive_tests()
        all_results["suites"]["interactive"] = interactive_results
        total_passed += interactive_results["passed"]
        total_failed += interactive_results["failed"]
    except Exception as e:
        print(f"ERROR running interactive tests: {e}")
        all_results["suites"]["interactive"] = {"error": str(e)}

    # 5. Visual Regression Screenshots
    print("\n\n" + "#"*70)
    print("# SUITE 5: VISUAL REGRESSION SCREENSHOTS")
    print("#"*70)
    try:
        screenshot_results = run_screenshot_capture()
        all_results["suites"]["screenshots"] = screenshot_results
    except Exception as e:
        print(f"ERROR capturing screenshots: {e}")
        all_results["suites"]["screenshots"] = {"error": str(e)}

    # Final Summary
    print("\n\n" + "="*70)
    print("FINAL TEST SUMMARY")
    print("="*70)
    print(f"\nTest Target: https://mml-eu-production.up.railway.app")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "-"*40)

    suite_summaries = [
        ("Responsive Design", all_results["suites"].get("responsive", {})),
        ("Navigation", all_results["suites"].get("navigation", {})),
        ("Forms", all_results["suites"].get("forms", {})),
        ("Interactive", all_results["suites"].get("interactive", {})),
    ]

    for name, results in suite_summaries:
        if "error" in results:
            print(f"{name:25} ERROR: {results['error'][:40]}")
        else:
            passed = results.get("passed", 0)
            failed = results.get("failed", 0)
            status = "PASS" if failed == 0 else "FAIL"
            print(f"{name:25} {status:6} (Passed: {passed}, Failed: {failed})")

    # Screenshots summary
    screenshot_data = all_results["suites"].get("screenshots", {})
    if "error" not in screenshot_data:
        successful = screenshot_data.get("successful", 0)
        total = screenshot_data.get("total", 0)
        print(f"{'Visual Screenshots':25} {'OK':6} ({successful}/{total} captured)")
        if screenshot_data.get("output_directory"):
            print(f"\n  Screenshots saved to: {screenshot_data['output_directory']}")

    print("\n" + "-"*40)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")

    if total_failed == 0:
        print("\nALL TESTS PASSED!")
    else:
        print(f"\n{total_failed} TEST(S) NEED ATTENTION")

    # Save complete results
    results_path = "C:/Dev/Claude/MML EU/tests/complete_results.json"
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nComplete results saved to: {results_path}")

    return all_results

if __name__ == "__main__":
    run_all_tests()
