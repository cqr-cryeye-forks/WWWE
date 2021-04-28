from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils import print_error, result

firefox_url = 'https://monitor.firefox.com/'


def process_search(d: WebDriver, email: str) -> int:
    d.get(url=firefox_url)
    form = d.find_element_by_xpath('//*[@id="scan-user-email"]')
    email_field = d.find_element_by_xpath('//*[@id="scan-email"]')
    email_field.send_keys(email)
    form.submit()
    results_count = WebDriverWait(d, 10).until(
        ec.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div/h2/span'))
    )
    return int(results_count.text)


def firefox(d: WebDriver, email: str) -> dict:
    try:
        if process_search(d=d, email=email):
            return result(email=email, service=__name__, is_leak=True)
        return result(email=email, service=__name__, is_leak=False)
    except Exception as e:
        print_error(e, service=__name__)
