"""
Visual Regression Screenshots for MML Europe Website
Captures screenshots at key breakpoints for visual verification.
"""
from playwright.sync_api import sync_playwright
import os
import json
from datetime import datetime

BASE_URL = "https://mml-eu-production.up.railway.app"
SCREENSHOT_DIR = "C:/Dev/Claude/MML EU/screenshots"

# Screenshot matrix from the plan
PAGES_TO_SCREENSHOT = [
    "/index.html",
    "/about.html",
    "/stockholm-event.html",
]

BREAKPOINTS = [
    {"name": "desktop", "width": 1440, "height": 900},
    {"name": "tablet", "width": 991, "height": 1024},
    {"name": "mobile", "width": 479, "height": 800},
]

def ensure_screenshot_dir():
    """Ensure screenshot directory exists."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(SCREENSHOT_DIR, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    return run_dir

def capture_screenshot(page, page_url, breakpoint, output_dir):
    """Capture a screenshot at the specified breakpoint."""
    page_name = page_url.split('/')[-1].replace('.html', '')
    filename = f"{page_name}_{breakpoint['name']}_{breakpoint['width']}px.png"
    filepath = os.path.join(output_dir, filename)

    try:
        # Set viewport
        page.set_viewport_size({"width": breakpoint["width"], "height": breakpoint["height"]})

        # Navigate
        page.goto(f"{BASE_URL}{page_url}", wait_until="networkidle", timeout=30000)
        page.wait_for_load_state("networkidle")

        # Wait a bit for any animations to settle
        page.wait_for_timeout(1000)

        # Take full-page screenshot
        page.screenshot(path=filepath, full_page=True)

        return {
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "page": page_url,
            "breakpoint": breakpoint["name"],
            "width": breakpoint["width"]
        }

    except Exception as e:
        return {
            "success": False,
            "filename": filename,
            "page": page_url,
            "breakpoint": breakpoint["name"],
            "error": str(e)
        }

def capture_element_screenshot(page, selector, name, output_dir):
    """Capture a screenshot of a specific element."""
    filename = f"element_{name}.png"
    filepath = os.path.join(output_dir, filename)

    try:
        element = page.locator(selector).first
        if element.count() > 0 and element.is_visible():
            element.screenshot(path=filepath)
            return {"success": True, "filename": filename}
        else:
            return {"success": False, "error": "Element not found or not visible"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_screenshot_capture():
    """Run the screenshot capture process."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "screenshots": [],
        "total": 0,
        "successful": 0,
        "failed": 0
    }

    output_dir = ensure_screenshot_dir()
    results["output_directory"] = output_dir

    print("="*60)
    print("VISUAL REGRESSION SCREENSHOTS")
    print("="*60)
    print(f"Output directory: {output_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Capture page screenshots at each breakpoint
        print("\n1. Capturing page screenshots...")

        for page_url in PAGES_TO_SCREENSHOT:
            page_name = page_url.split('/')[-1]
            print(f"\n   {page_name}:")

            for breakpoint in BREAKPOINTS:
                result = capture_screenshot(page, page_url, breakpoint, output_dir)
                results["screenshots"].append(result)
                results["total"] += 1

                if result["success"]:
                    results["successful"] += 1
                    print(f"      [{breakpoint['name']:>8}] {breakpoint['width']}px - OK")
                else:
                    results["failed"] += 1
                    print(f"      [{breakpoint['name']:>8}] {breakpoint['width']}px - FAILED: {result.get('error', 'Unknown')}")

        # Capture specific element screenshots
        print("\n2. Capturing element screenshots...")

        # Reset to desktop viewport
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(BASE_URL, wait_until="networkidle")

        elements_to_capture = [
            ("nav, .navbar", "navbar"),
            ("footer, .footer", "footer"),
            (".hero, .hero-section, header", "hero"),
        ]

        for selector, name in elements_to_capture:
            result = capture_element_screenshot(page, selector, name, output_dir)
            if result["success"]:
                print(f"      {name}: OK")
            else:
                print(f"      {name}: SKIPPED - {result.get('error', 'Not found')}")

        # Capture mobile menu state
        print("\n3. Capturing mobile menu state...")
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(BASE_URL, wait_until="networkidle")

        # Try to open mobile menu
        menu_button = page.locator('.w-nav-button, .navbar_menu-button').first
        if menu_button.count() > 0 and menu_button.is_visible():
            menu_button.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(output_dir, "mobile_menu_open.png"), full_page=True)
            print("      mobile_menu_open: OK")
        else:
            print("      mobile_menu_open: SKIPPED - Menu button not visible")

        context.close()
        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print("SCREENSHOT CAPTURE SUMMARY")
    print('='*60)
    print(f"Output directory: {output_dir}")
    print(f"Total screenshots: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")

    # Save results manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nManifest saved to: {manifest_path}")

    # List all screenshots
    print(f"\nScreenshots captured:")
    for screenshot in results["screenshots"]:
        if screenshot["success"]:
            print(f"   - {screenshot['filename']}")

    return results

if __name__ == "__main__":
    run_screenshot_capture()
