from aiohttp import ClientSession
from bs4 import BeautifulSoup

from utils import print_error, unexpected_status, set_headers

google_url = 'https://google.com/search?q='


def parse_resp(content: str, email: str) -> dict:
    soup = BeautifulSoup(content, 'lxml')
    results = soup.find('div', {'id': 'search'}).find_all('div', class_='g')
    if results:
        return {'result': f'The mailing address: {email} was found in a Google search service.'}
    return {'result': f'The mailing address: {email} was not found in a Google search service.'}


async def google_search(email: str, session: ClientSession) -> dict:
    try:
        set_headers(s=session)
        async with session.get(f'{google_url}{email}', verify_ssl=False) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.text(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
