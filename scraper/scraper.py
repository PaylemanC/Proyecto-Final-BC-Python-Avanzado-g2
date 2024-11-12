from playwright.sync_api import sync_playwright


def scrape():
    url = "https://clerk.house.gov/evs/2024/roll455.xml"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        print(content)
        browser.close()


if __name__ == "__main__":
    scrape()
