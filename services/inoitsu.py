from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils import print_error, result

inoitsu_url = 'https://www.hotsheet.com/inoitsu/'


def process_search(d: WebDriver, email: str) -> int:
    d.get(url=inoitsu_url)
    submit = d.find_element_by_xpath('/html/body/center/div[2]/center/div/blockquote/form/input[3]')
    email_field = d.find_element_by_xpath('//*[@id="act"]')
    email_field.send_keys(email)
    submit.click()
    WebDriverWait(d, 10).until(
        ec.presence_of_element_located((By.XPATH, '/html/body/center/div[2]/center/div/blockquote/h3'))
    )
    return 'no breaches found!' not in d.page_source.lower()


def inoitsu(d: WebDriver, email: str) -> dict:
    try:
        if process_search(d=d, email=email):
            return result(email=email, service=__name__, is_leak=True)
        return result(email=email, service=__name__, is_leak=False)
    except Exception as e:
        print_error(e, service=__name__)
