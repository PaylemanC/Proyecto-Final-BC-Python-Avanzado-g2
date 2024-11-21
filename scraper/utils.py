"""
Utils module with helper functions
necessary for the scraper process
"""
from playwright.sync_api import sync_playwright


def get_hr_page(url: str) -> str:
    """
    Get the HTML content of the HR page
    """    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page().goto(url)
        page_content = page.text()
    return page_content


def get_roll_call_data(url: str) -> str:
    """
    Get the roll call data from the XML file
    """
    pass


if __name__ == "__main__":
    print("Greetings from the utils module")
