from playwright.sync_api import sync_playwright


def scrape_xml():
    url = "https://clerk.house.gov/evs/2024/roll455.xml"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        def handle_response(response):
            if response.url == url:
                print(response.text())

        page.on("response", handle_response)
        page.goto(url)
        browser.close()


if __name__ == "__main__":
    scrape_xml()
