from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False = ves el navegador
    page = browser.new_page()
    page.goto("https://playwright.dev")
    print(f"Título: {page.title()}")
    browser.close()