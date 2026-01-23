"""
Form Functionality Tests for MML Europe Website
Tests Tally form integration for newsletter and event registration.
"""
from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://mml-eu-production.up.railway.app"

PAGES_WITH_NEWSLETTER = [
    "/index.html",
    "/about.html",
    "/blog.html",
    "/stockholm-event.html",
    "/brussels-event.html",
]

EVENT_PAGES = [
    "/stockholm-event.html",
    "/brussels-event.html",
]

def find_newsletter_form(page):
    """Find newsletter form elements on the page."""
    # Look for Tally form or custom newsletter form
    form_selectors = [
        'iframe[src*="tally"]',
        'form[data-tally-form]',
        '.newsletter-form',
        'form[action*="newsletter"]',
        'input[type="email"]',
        '.w-form',
    ]

    for selector in form_selectors:
        element = page.locator(selector).first
        if element.count() > 0 and element.is_visible():
            return {"found": True, "selector": selector}

    return {"found": False}

def test_newsletter_form(page, page_url):
    """Test newsletter form functionality."""
    result = {
        "page": page_url,
        "form_found": False,
        "email_input_found": False,
        "submit_button_found": False,
        "can_submit": False,
        "errors": []
    }

    try:
        # Check for Tally iframe
        tally_iframe = page.locator('iframe[src*="tally"]').first
        if tally_iframe.count() > 0 and tally_iframe.is_visible():
            result["form_found"] = True
            result["form_type"] = "tally_iframe"
            result["note"] = "Tally iframe found - form is embedded"
            return result

        # Look for standard form
        email_input = page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]').first
        if email_input.count() > 0:
            result["email_input_found"] = True
            result["form_found"] = True

            # Check if visible
            if email_input.is_visible():
                # Find submit button
                submit_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    '.w-button',
                    'button:has-text("Subscribe")',
                    'button:has-text("Sign up")',
                    'button:has-text("Submit")',
                ]

                for selector in submit_selectors:
                    submit_btn = page.locator(selector).first
                    if submit_btn.count() > 0 and submit_btn.is_visible():
                        result["submit_button_found"] = True
                        result["submit_selector"] = selector
                        break

                # Try filling the form (but don't actually submit to avoid spam)
                try:
                    email_input.fill("test@example.com")
                    filled_value = email_input.input_value()
                    result["can_fill"] = filled_value == "test@example.com"
                    # Clear the field
                    email_input.fill("")
                except Exception as e:
                    result["errors"].append(f"Fill error: {str(e)}")

        # Check for w-form (Webflow form)
        w_form = page.locator('.w-form').first
        if w_form.count() > 0:
            result["form_found"] = True
            result["form_type"] = "webflow"

    except Exception as e:
        result["errors"].append(str(e))

    result["passed"] = result["form_found"]
    return result

def test_event_registration_form(page, page_url):
    """Test event registration form on event pages."""
    result = {
        "page": page_url,
        "form_found": False,
        "name_input_found": False,
        "email_input_found": False,
        "submit_button_found": False,
        "errors": []
    }

    try:
        # Check for Tally iframe (common for registration)
        tally_iframe = page.locator('iframe[src*="tally"]').first
        if tally_iframe.count() > 0:
            result["form_found"] = True
            result["form_type"] = "tally_iframe"
            result["passed"] = True
            return result

        # Look for registration form
        registration_form = page.locator('form, .registration-form, .w-form').first

        if registration_form.count() > 0:
            result["form_found"] = True

            # Check for name input
            name_input = page.locator('input[name="name"], input[placeholder*="name" i], input[type="text"]').first
            if name_input.count() > 0:
                result["name_input_found"] = True

            # Check for email input
            email_input = page.locator('input[type="email"], input[name="email"]').first
            if email_input.count() > 0:
                result["email_input_found"] = True

            # Check for submit button
            submit_btn = page.locator('button[type="submit"], input[type="submit"], .w-button').first
            if submit_btn.count() > 0:
                result["submit_button_found"] = True

    except Exception as e:
        result["errors"].append(str(e))

    result["passed"] = result["form_found"]
    return result

def check_form_validation(page):
    """Check if form has proper validation."""
    result = {
        "has_required_fields": False,
        "has_email_validation": False,
        "errors": []
    }

    try:
        # Check for required attributes
        required_inputs = page.locator('input[required], select[required], textarea[required]').all()
        result["has_required_fields"] = len(required_inputs) > 0
        result["required_count"] = len(required_inputs)

        # Check email input type
        email_inputs = page.locator('input[type="email"]').all()
        result["has_email_validation"] = len(email_inputs) > 0

    except Exception as e:
        result["errors"].append(str(e))

    return result

def run_form_tests():
    results = {"passed": 0, "failed": 0, "tests": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Capture console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("="*60)
        print("FORM FUNCTIONALITY TESTS")
        print("="*60)

        # Test 1: Newsletter forms on all pages
        print("\n1. Testing newsletter forms on all pages...")
        for page_path in PAGES_WITH_NEWSLETTER:
            url = f"{BASE_URL}{page_path}"
            page_name = page_path.split('/')[-1]

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_load_state("networkidle")

                newsletter_result = test_newsletter_form(page, page_name)
                results["tests"].append({"type": "newsletter", **newsletter_result})

                if newsletter_result["passed"]:
                    results["passed"] += 1
                    form_type = newsletter_result.get("form_type", "standard")
                    print(f"   PASS: {page_name} - Newsletter form found ({form_type})")
                else:
                    results["failed"] += 1
                    print(f"   FAIL: {page_name} - Newsletter form not found")

            except Exception as e:
                results["failed"] += 1
                print(f"   ERROR: {page_name} - {str(e)}")
                results["tests"].append({
                    "type": "newsletter",
                    "page": page_name,
                    "passed": False,
                    "error": str(e)
                })

        # Test 2: Event registration forms
        print("\n2. Testing event registration forms...")
        for page_path in EVENT_PAGES:
            url = f"{BASE_URL}{page_path}"
            page_name = page_path.split('/')[-1]

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_load_state("networkidle")

                registration_result = test_event_registration_form(page, page_name)
                results["tests"].append({"type": "registration", **registration_result})

                if registration_result["passed"]:
                    results["passed"] += 1
                    form_type = registration_result.get("form_type", "standard")
                    print(f"   PASS: {page_name} - Registration form found ({form_type})")
                else:
                    results["failed"] += 1
                    print(f"   FAIL: {page_name} - Registration form not found")

            except Exception as e:
                results["failed"] += 1
                print(f"   ERROR: {page_name} - {str(e)}")

        # Test 3: Form validation check
        print("\n3. Checking form validation attributes...")
        page.goto(BASE_URL, wait_until="networkidle")
        validation_result = check_form_validation(page)
        results["tests"].append({"type": "validation", **validation_result})
        print(f"   Required fields: {validation_result.get('required_count', 0)}")
        print(f"   Email validation: {validation_result.get('has_email_validation', False)}")

        # Console errors
        if console_errors:
            print(f"\nConsole errors detected: {len(console_errors)}")
            for err in console_errors[:5]:
                print(f"   - {err[:100]}")

        context.close()
        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print("FORM TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {results['passed'] + results['failed']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")

    # Save results
    with open("C:/Dev/Claude/MML EU/tests/form_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_form_tests()
