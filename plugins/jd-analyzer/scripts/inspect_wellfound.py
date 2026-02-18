#!/usr/bin/env python3
"""
Wellfound Page Inspector

Inspects the Wellfound jobs page to identify correct selectors.
"""

from playwright.sync_api import sync_playwright
import time

def inspect_wellfound():
    """Inspect Wellfound page structure."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("Navigating to Wellfound...")
            page.goto("https://wellfound.com/jobs", timeout=30000)

            # Wait for page to load
            time.sleep(5)

            print("\n=== PAGE STRUCTURE ===\n")

            # Get page title
            print(f"Page Title: {page.title()}")

            # Try to find job listings with various selectors
            selectors_to_try = [
                ".job-listings",
                ".jobs-list",
                "[class*='job']",
                "[data-test*='job']",
                "ul[role='list']",
                ".styles_results",
                "[class*='SearchResult']",
                "[class*='JobListing']",
                "div[class*='job']",
            ]

            print("\n--- Testing Selectors ---\n")
            for selector in selectors_to_try:
                try:
                    count = page.locator(selector).count()
                    if count > 0:
                        print(f"✓ '{selector}' found {count} elements")

                        # Get the first element's classes
                        first = page.locator(selector).first
                        classes = first.get_attribute("class")
                        print(f"  Classes: {classes}")
                except Exception as e:
                    print(f"✗ '{selector}' failed: {str(e)[:50]}")

            # Try to find job cards
            print("\n--- Looking for Job Cards ---\n")
            job_selectors = [
                "article",
                "[role='article']",
                "li[data-test]",
                "div[class*='Card']",
                "a[class*='job']",
            ]

            for selector in job_selectors:
                try:
                    count = page.locator(selector).count()
                    if count > 0 and count < 100:  # Likely job cards
                        print(f"✓ '{selector}' found {count} elements (likely job cards)")

                        # Get first card details
                        first = page.locator(selector).first
                        text = first.inner_text()[:100]
                        print(f"  First card text: {text}...")
                except Exception as e:
                    pass

            # Save page HTML for manual inspection
            html = page.content()
            with open("wellfound_page.html", "w") as f:
                f.write(html)
            print(f"\n✓ Saved HTML to wellfound_page.html")

            # Take screenshot
            page.screenshot(path="wellfound_page.png")
            print(f"✓ Saved screenshot to wellfound_page.png")

            input("\nPress Enter to close browser...")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    inspect_wellfound()
