"""
Responsive Design Tests for MML Europe Website
Tests typography and layout at each breakpoint.
"""
from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://mml-eu-production.up.railway.app"

PAGES = [
    "/index.html",
    "/about.html",
    "/blog.html",
    "/stockholm-event.html",
    "/brussels-event.html",
]

BREAKPOINTS = [
    {"name": "Desktop", "width": 1440, "height": 900},
    {"name": "Tablet", "width": 991, "height": 1024},
    {"name": "Mobile Landscape", "width": 767, "height": 480},
    {"name": "Mobile Portrait", "width": 479, "height": 800},
    {"name": "Small Mobile", "width": 375, "height": 667},
]

def check_horizontal_overflow(page):
    """Check if page has horizontal scrollbar (indicates overflow)."""
    result = page.evaluate("""
        () => {
            return {
                documentWidth: document.documentElement.scrollWidth,
                viewportWidth: document.documentElement.clientWidth,
                hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
            }
        }
    """)
    return result

def get_heading_styles(page):
    """Get computed font sizes for headings."""
    styles = page.evaluate("""
        () => {
            const h1 = document.querySelector('h1');
            const h2 = document.querySelector('h2');
            return {
                h1_size: h1 ? window.getComputedStyle(h1).fontSize : null,
                h2_size: h2 ? window.getComputedStyle(h2).fontSize : null,
            }
        }
    """)
    return styles

def check_button_overflow(page):
    """Check if any buttons overflow their containers."""
    result = page.evaluate("""
        () => {
            const buttons = document.querySelectorAll('a.button, button, .w-button');
            const issues = [];
            buttons.forEach((btn, i) => {
                const rect = btn.getBoundingClientRect();
                const parent = btn.parentElement;
                if (parent) {
                    const parentRect = parent.getBoundingClientRect();
                    if (rect.right > parentRect.right + 5 || rect.left < parentRect.left - 5) {
                        issues.push({
                            index: i,
                            text: btn.textContent.trim().substring(0, 30),
                            buttonRight: rect.right,
                            parentRight: parentRect.right
                        });
                    }
                }
            });
            return { buttonCount: buttons.length, overflowIssues: issues };
        }
    """)
    return result

def run_responsive_tests():
    results = {"passed": 0, "failed": 0, "tests": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for breakpoint in BREAKPOINTS:
            context = browser.new_context(
                viewport={"width": breakpoint["width"], "height": breakpoint["height"]}
            )
            page = context.new_page()

            # Capture console errors
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            print(f"\n{'='*60}")
            print(f"Testing at {breakpoint['name']} ({breakpoint['width']}px)")
            print('='*60)

            for page_path in PAGES:
                url = f"{BASE_URL}{page_path}"
                page_name = page_path.split('/')[-1]

                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    page.wait_for_load_state("networkidle")

                    # Test 1: Check horizontal overflow
                    overflow = check_horizontal_overflow(page)
                    overflow_pass = not overflow["hasOverflow"]

                    # Test 2: Get heading styles
                    headings = get_heading_styles(page)

                    # Test 3: Check button overflow
                    buttons = check_button_overflow(page)
                    buttons_pass = len(buttons["overflowIssues"]) == 0

                    test_passed = overflow_pass and buttons_pass

                    test_result = {
                        "breakpoint": breakpoint["name"],
                        "page": page_name,
                        "width": breakpoint["width"],
                        "passed": test_passed,
                        "overflow": overflow,
                        "headings": headings,
                        "buttons": buttons,
                        "console_errors": console_errors.copy()
                    }
                    results["tests"].append(test_result)

                    if test_passed:
                        results["passed"] += 1
                        status = "PASS"
                    else:
                        results["failed"] += 1
                        status = "FAIL"

                    print(f"\n{status}: {page_name}")
                    print(f"  Horizontal overflow: {'No' if overflow_pass else 'YES - ' + str(overflow)}")
                    print(f"  H1 size: {headings['h1_size']}")
                    print(f"  Buttons checked: {buttons['buttonCount']}, overflow issues: {len(buttons['overflowIssues'])}")

                    if buttons["overflowIssues"]:
                        for issue in buttons["overflowIssues"]:
                            print(f"    - Button '{issue['text']}' overflows")

                    if console_errors:
                        print(f"  Console errors: {len(console_errors)}")

                    console_errors.clear()

                except Exception as e:
                    print(f"\nERROR: {page_name} - {str(e)}")
                    results["failed"] += 1
                    results["tests"].append({
                        "breakpoint": breakpoint["name"],
                        "page": page_name,
                        "passed": False,
                        "error": str(e)
                    })

            context.close()

        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print("RESPONSIVE TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {results['passed'] + results['failed']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")

    # Save results
    with open("C:/Dev/Claude/MML EU/tests/responsive_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_responsive_tests()
