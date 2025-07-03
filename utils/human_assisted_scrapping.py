"""
A tool used to perform human-assisted scrapping. It takes what the user copies
and writes it down into a folder as an individual file.
"""

import csv
import pyperclip
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_driver(webdriver_path: str):
    service = Service(executable_path=webdriver_path)
    performance_prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 2,
    }
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs",
        {
            **performance_prefs,
        },
    )
    # some more performance-related options
    options.add_argument("--no-proxy-server")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--window-sized=1024,1324")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-dev-shm-usage")

    # avoid detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    return driver


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--webdriver-path", type=str, required=True)
    args = parser.parse_args()

    driver = get_driver(args.webdriver_path)

    out_dir = "article-text/kokac"
    Path(out_dir).mkdir(exist_ok=True)
    with open("data/kokac/inter-rater.csv", encoding="latin-1") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            title = row[-1]
            url = row[-3]
            out_path = Path(out_dir) / f"{title.replace('/', '_')}.txt"
            print(title)
            if out_path.exists():
                continue
            driver.get("http://" + url)
            i = input()
            if i == "skip":
                print("skipped", title)
                continue
            with open(str(out_path), "w") as f:
                f.write(pyperclip.paste())
