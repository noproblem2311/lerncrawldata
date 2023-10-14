from playwright.sync_api import sync_playwright

def playwright_config():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        return page