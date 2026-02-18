#!/usr/bin/env python3
"""
Wellfound Search Inspector

Tests the full search flow on Wellfound to identify correct selectors.
"""

from playwright.sync_api import sync_playwright
import time

def inspect_search_flow():
    """Inspect the complete Wellfound search flow."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("=== STEP 1: Navigate to Wellfound ===")
            page.goto("https://wellfound.com/jobs", timeout=30000)
            time.sleep(3)

            print("\n=== STEP 2: Fill Search Form ===")

            # Find and fill job title input
            title_selectors = [
                'input[placeholder*="Job title"]',
                'input[name*="job"]',
                'input[type="text"]',
            ]

            for selector in title_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"✓ Found title input: {selector}")
                        page.fill(selector, "AI Product Engineer", timeout=5000)
                        break
                except:
                    pass

            # Find and fill location input (or skip for remote)
            location_selectors = [
                'input[placeholder*="Location"]',
                'input[name*="location"]',
            ]

            for selector in location_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"✓ Found location input: {selector}")
                        # Leave empty for remote jobs
                        break
                except:
                    pass

            time.sleep(2)

            print("\n=== STEP 3: Submit Search ===")

            # Find and click search button
            search_selectors = [
                'button:has-text("Search")',
                'button[type="submit"]',
                '[data-test*="search"]',
            ]

            for selector in search_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"✓ Found search button: {selector}")
                        page.click(selector)
                        break
                except:
                    pass

            # Wait for results
            time.sleep(5)

            print(f"\n✓ Current URL: {page.url}")

            print("\n=== STEP 4: Analyze Results Page ===")

            # Try different result selectors
            result_selectors = [
                '[data-test*="job"]',
                'article',
                '[role="article"]',
                'div[class*="JobSearchResult"]',
                'a[href*="/role/"]',
                'li',
                'div[class*="Card"]',
            ]

            print("\n--- Testing Result Selectors ---\n")
            for selector in result_selectors:
                try:
                    count = page.locator(selector).count()
                    if count > 0 and count < 200:
                        print(f"✓ '{selector}': {count} elements")

                        # Get first element details
                        first = page.locator(selector).first
                        if first:
                            text = first.inner_text()[:150]
                            classes = first.get_attribute("class") or "no-class"
                            print(f"  Classes: {classes}")
                            print(f"  Text preview: {text}...")
                            print()
                except Exception as e:
                    pass

            # Look for job links
            print("\n--- Looking for Job Links ---\n")
            links = page.locator('a[href*="/role/"]').all()
            print(f"Found {len(links)} job links with '/role/' pattern")

            if len(links) > 0:
                first_link = links[0]
                href = first_link.get_attribute("href")
                text = first_link.inner_text()[:100]
                print(f"  First link: {href}")
                print(f"  Text: {text}")

            # Save results page
            html = page.content()
            with open("wellfound_results.html", "w") as f:
                f.write(html)
            print(f"\n✓ Saved results HTML to wellfound_results.html")

            page.screenshot(path="wellfound_results.png")
            print(f"✓ Saved screenshot to wellfound_results.png")

            input("\nPress Enter to close browser...")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    inspect_search_flow()
