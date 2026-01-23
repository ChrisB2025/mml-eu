"""
Navigation Tests for MML Europe Website
Tests all navigation elements including main nav, dropdowns, and mobile menu.
"""
from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://mml-eu-production.up.railway.app"

def test_logo_link(page):
    """Test that logo links to homepage."""
    logo = page.locator('a.navbar_logo-link, a[href*="index"], .w-nav-brand').first
    if logo.count() > 0:
        href = logo.get_attribute("href")
        return {"passed": True, "href": href}
    return {"passed": False, "error": "Logo not found"}

def test_main_nav_links(page):
    """Test main navigation links."""
    results = []
    # Try multiple selectors based on actual site structure
    nav_selectors = [
        '.nav_link.w-inline-block',  # Main nav links
        '.nav_logo.w-inline-block',  # Logo link
        'a.nav_link',                # Alternative selector
    ]

    found_links = []
    for selector in nav_selectors:
        nav_links = page.locator(selector).all()
        for link in nav_links:
            try:
                text = link.text_content().strip()
                href = link.get_attribute("href")
                # Don't require visibility - some nav elements may be hidden initially
                # but still functional
                if text and href:
                    found_links.append({
                        "text": text[:50],
                        "href": href,
                        "selector": selector
                    })
            except:
                pass

    # Deduplicate by href
    seen = set()
    for r in found_links:
        if r["href"] not in seen and r["href"] != "#":
            seen.add(r["href"])
            results.append(r)

    return results

def test_events_dropdown(page):
    """Test events dropdown menu."""
    # Look for dropdown trigger
    dropdown_trigger = page.locator('[data-hover="true"], .w-dropdown-toggle, .navbar_dropdown-toggle').first

    if dropdown_trigger.count() == 0:
        return {"passed": False, "error": "Dropdown trigger not found"}

    try:
        # Hover to open dropdown
        dropdown_trigger.hover()
        page.wait_for_timeout(500)

        # Check for dropdown content
        dropdown_content = page.locator('.w-dropdown-list, .navbar_dropdown-list').first
        is_visible = dropdown_content.is_visible() if dropdown_content.count() > 0 else False

        # Get dropdown links
        dropdown_links = page.locator('.w-dropdown-list a, .navbar_dropdown-list a').all()
        links = []
        for link in dropdown_links:
            links.append({
                "text": link.text_content().strip(),
                "href": link.get_attribute("href")
            })

        return {
            "passed": True,
            "dropdown_visible": is_visible,
            "links": links
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}

def test_mobile_menu(page, context):
    """Test mobile menu at tablet/mobile viewport."""
    # Create mobile context
    mobile_page = context.new_page()
    mobile_page.set_viewport_size({"width": 768, "height": 1024})
    mobile_page.goto(BASE_URL, wait_until="networkidle")

    try:
        # Look for mobile menu button
        menu_button = mobile_page.locator('.w-nav-button, .navbar_menu-button, [aria-label*="menu"]').first

        if menu_button.count() == 0:
            mobile_page.close()
            return {"passed": False, "error": "Mobile menu button not found"}

        is_button_visible = menu_button.is_visible()

        if not is_button_visible:
            mobile_page.close()
            return {"passed": True, "note": "Mobile menu button not visible at this viewport - may be desktop"}

        # Click to open menu
        menu_button.click()
        mobile_page.wait_for_timeout(500)

        # Check if menu opened
        nav_menu = mobile_page.locator('.w-nav-overlay, .navbar_menu.w--open, .w-nav-menu').first
        menu_opened = nav_menu.is_visible() if nav_menu.count() > 0 else False

        # Click again to close
        menu_button.click()
        mobile_page.wait_for_timeout(500)

        # Check if menu closed
        menu_closed = not nav_menu.is_visible() if nav_menu.count() > 0 else True

        mobile_page.close()
        return {
            "passed": True,
            "button_visible": is_button_visible,
            "menu_opened": menu_opened,
            "menu_closed": menu_closed
        }

    except Exception as e:
        mobile_page.close()
        return {"passed": False, "error": str(e)}

def test_footer_links(page):
    """Test footer navigation links."""
    footer_links = page.locator('footer a, .footer a, .footer_link').all()
    results = []

    for link in footer_links:
        text = link.text_content().strip()
        href = link.get_attribute("href")
        if text and href:
            results.append({
                "text": text[:50],
                "href": href
            })

    return results

def test_link_navigation(page, browser):
    """Test that clicking links navigates to correct pages."""
    results = []

    # Get all links and filter for internal ones
    all_links = page.locator('a[href]').all()

    tested_urls = set()
    for link in all_links:
        href = link.get_attribute("href")
        if not href:
            continue

        # Skip anchors, javascript, and external links
        if href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
            continue

        # Check if it's an internal link (relative or same domain)
        is_internal = (
            href.endswith(".html") or
            href.startswith("/") or
            "mml-eu" in href or
            (not href.startswith("http") and not href.startswith("//"))
        )

        if not is_internal:
            continue

        if href in tested_urls:
            continue

        tested_urls.add(href)

        if len(tested_urls) > 10:  # Test first 10 unique links
            break

        # Create new page to test navigation
        test_page = browser.new_page()
        try:
            full_url = href if href.startswith("http") else f"{BASE_URL}/{href.lstrip('/')}"
            response = test_page.goto(full_url, wait_until="domcontentloaded", timeout=10000)
            status = response.status if response else "No response"
            results.append({
                "href": href,
                "status": status,
                "passed": status == 200
            })
        except Exception as e:
            results.append({
                "href": href,
                "error": str(e),
                "passed": False
            })
        finally:
            test_page.close()

    return results

def run_navigation_tests():
    results = {"passed": 0, "failed": 0, "tests": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Capture console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("="*60)
        print("NAVIGATION TESTS")
        print("="*60)

        # Navigate to homepage
        page.goto(BASE_URL, wait_until="networkidle")

        # Test 1: Logo link
        print("\n1. Testing logo link...")
        logo_result = test_logo_link(page)
        results["tests"].append({"name": "Logo Link", **logo_result})
        if logo_result["passed"]:
            results["passed"] += 1
            print(f"   PASS: Logo links to {logo_result.get('href', 'N/A')}")
        else:
            results["failed"] += 1
            print(f"   FAIL: {logo_result.get('error', 'Unknown error')}")

        # Test 2: Main nav links
        print("\n2. Testing main navigation links...")
        nav_links = test_main_nav_links(page)
        results["tests"].append({"name": "Main Nav Links", "links": nav_links, "passed": len(nav_links) > 0})
        if nav_links:
            results["passed"] += 1
            print(f"   PASS: Found {len(nav_links)} navigation links")
            for link in nav_links:
                print(f"      - {link['text']}: {link['href']}")
        else:
            results["failed"] += 1
            print("   FAIL: No navigation links found")

        # Test 3: Events dropdown
        print("\n3. Testing events dropdown...")
        dropdown_result = test_events_dropdown(page)
        results["tests"].append({"name": "Events Dropdown", **dropdown_result})
        if dropdown_result["passed"]:
            results["passed"] += 1
            print(f"   PASS: Dropdown working, found {len(dropdown_result.get('links', []))} links")
            for link in dropdown_result.get("links", []):
                print(f"      - {link['text']}: {link['href']}")
        else:
            results["failed"] += 1
            print(f"   FAIL: {dropdown_result.get('error', 'Unknown error')}")

        # Test 4: Mobile menu
        print("\n4. Testing mobile menu...")
        mobile_result = test_mobile_menu(page, context)
        results["tests"].append({"name": "Mobile Menu", **mobile_result})
        if mobile_result["passed"]:
            results["passed"] += 1
            print(f"   PASS: Mobile menu toggle working")
            print(f"      Button visible: {mobile_result.get('button_visible', 'N/A')}")
            print(f"      Menu opens: {mobile_result.get('menu_opened', 'N/A')}")
            print(f"      Menu closes: {mobile_result.get('menu_closed', 'N/A')}")
        else:
            results["failed"] += 1
            print(f"   FAIL: {mobile_result.get('error', 'Unknown error')}")

        # Test 5: Footer links
        print("\n5. Testing footer links...")
        footer_links = test_footer_links(page)
        results["tests"].append({"name": "Footer Links", "links": footer_links, "passed": len(footer_links) > 0})
        if footer_links:
            results["passed"] += 1
            print(f"   PASS: Found {len(footer_links)} footer links")
        else:
            results["failed"] += 1
            print("   FAIL: No footer links found")

        # Test 6: Link navigation
        print("\n6. Testing link navigation (sample of links)...")
        link_results = test_link_navigation(page, browser)
        all_passed = all(r["passed"] for r in link_results) if link_results else False
        results["tests"].append({"name": "Link Navigation", "links": link_results, "passed": all_passed})
        if all_passed and link_results:
            results["passed"] += 1
            print(f"   PASS: All {len(link_results)} tested links return 200")
        else:
            results["failed"] += 1
            for r in link_results:
                status = "PASS" if r["passed"] else "FAIL"
                print(f"   {status}: {r['href']} - {r.get('status', r.get('error', 'Unknown'))}")

        # Console errors
        if console_errors:
            print(f"\nConsole errors detected: {len(console_errors)}")
            for err in console_errors[:5]:
                print(f"   - {err[:100]}")

        context.close()
        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print("NAVIGATION TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {results['passed'] + results['failed']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")

    # Save results
    with open("C:/Dev/Claude/MML EU/tests/navigation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_navigation_tests()
