import argparse
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def capture_screenshot(url, output_file=None):
    """Capture website screenshot and save to file.
    
    Args:
        url (str): Valid URL to capture
        output_file (str, optional): Output path. Defaults to timestamped filename.
    
    Returns:
        str: Path to saved screenshot
    """
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL format. Must include http:// or https://")

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"screenshot_{timestamp}.png"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.screenshot(path=output_file)
            browser.close()
    except Exception as e:
        if os.path.exists(output_file):
            os.remove(output_file)
        raise RuntimeError(f"Screenshot failed: {str(e)}") from e

    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture website screenshot")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    try:
        saved_path = capture_screenshot(args.url, args.output)
        print(f"Screenshot saved to: {saved_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
