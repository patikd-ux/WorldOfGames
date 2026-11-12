import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_URL = "http://localhost:8777"
WAIT_SECONDS = 10


def test_scores_service(application_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(application_url)
        element = WebDriverWait(driver, WAIT_SECONDS).until(
            EC.presence_of_element_located((By.ID, "score")))
        text = element.text.strip()
        if not text.isdecimal():
            print(f"FAIL: the score is not a whole number: {text!r}")
            return False
        score = int(text)
        if not 1 <= score <= 1000:
            print(f"FAIL: the score {score} is outside the range 1-1000")
            return False
        print(f"PASS: the score is {score} at {application_url}")
        return True
    except WebDriverException as error:
        print(f"FAIL: {type(error).__name__}: {error.msg}")
        return False
    finally:
        if driver is not None:
            driver.quit()


def main_function(application_url=DEFAULT_URL):
    if test_scores_service(application_url):
        sys.exit(0)
    sys.exit(-1)


if __name__ == "__main__":
    main_function(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL)
