from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils import print_error

leakedsource_url = 'https://leakedsource.ru/'


def process_search(d: WebDriver, email: str) -> int:
    d.get(url=leakedsource_url)
    submit = d.find_element_by_xpath('/html/body/center[2]/div/form/div/div[2]/center/input')
    email_field = d.find_element_by_xpath('/html/body/center[2]/div[1]/form/div/div[2]/div[1]/div/input')
    email_field.send_keys(email)
    submit.click()
    result = WebDriverWait(d, 10).until(
        ec.presence_of_element_located((By.XPATH, '/html/body/center[2]/div[2]'))
    )
    return 'no results found.' in result.text.lower()


def leakedsource(d: WebDriver, email: str) -> dict:
    try:
        if process_search(d=d, email=email):
            return {'result': f'The mailing address: {email} was found in a Leakedsource service.'}
        return {'result': f'The mailing address: {email} was not found in a Leakedsource service.'}
    except Exception as e:
        print_error(e, service=__name__)
