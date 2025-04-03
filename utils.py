import logging
import os
import json
import time
from typing import Optional
from selenium import webdriver
from undetected_chromedriver import Chrome
from undetected_geckodriver import Firefox

def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize the input text.

    Args:
        text: The string to clean.

    Returns:
        A cleaned and normalized string.
    """
    if not text:
        return ""
    replacements = {
        '$': '',
        '\\le': '<=',
        '^{\\dagger}': '',
        '\\ge': '>=',
        '\\neq': '!=',
        '\\cdot': '*',
        '\\ldots': '...',
        '\xa0': ' ',
        '\u2009': ' ',
        '\u2192': '->'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove multiple spaces and trim
    return " ".join(text.split()).strip()

def get_driver(browser: str) -> Chrome | Firefox:
    """
    Get a Selenium WebDriver instance for the specified browser.
    This function uses undetected_chromedriver for Chrome and undetected_geckodriver for Firefox.

    Args:
        browser: The browser to use ('chrome' or 'firefox').

    Returns:
        A WebDriver instance for the specified browser.
    """
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        return Chrome(options=options)

    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('useAutomationExtension', False)
        return Firefox(options=options)

    else:
        raise ValueError("Unsupported browser. Choose either 'chrome' or 'firefox'.")

def fetch_page(url: str, browser: str) -> str:
    """
    Fetch the HTML content of a page and try to bypass Cloudflare if needed.

    Args:
        url: The URL to fetch.
        browser: The browser to use for fetching the page ('chrome' or 'firefox').

    Returns:
        The page source HTML as a string.

    Raises:
        Exception: If the page could not be fetched after retries.
    """
    driver = None
    try:
        driver = get_driver(browser)
        driver.get(url)
        time.sleep(5)

        retries = 3
        for attempt in range(retries):
            html_content = driver.page_source
            if "Just a moment" not in html_content:
                return html_content

            logging.info("Cloudflare challenge detected, retrying... (%d/%d)", attempt + 1, retries)
            time.sleep(10 + attempt * 5)

        raise Exception("Failed to bypass Cloudflare challenge after multiple attempts.")
    finally:
        if driver:
            driver.close()
            time.sleep(0.1)

def save_data(title: str, data: dict, console) -> None:
    """
    Save scraped data to a JSON file in the Examples directory.
    """
    output_dir = "Examples"
    os.makedirs(output_dir, exist_ok=True)
    # Sanitize filename: allow only alphanumerics, space, and underscore.
    filename = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join(output_dir, f"{filename}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    console.print(f"[bold green]✓[/bold green] Successfully saved data to [cyan]{filepath}[/cyan]")