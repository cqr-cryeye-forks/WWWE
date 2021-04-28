import base64

import aiohttp

from utils import print_error, unexpected_status, get_headers, result

lifelock_url = 'https://www.lifelock.com/bin/norton/lifelock/detectbreach'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'CSRF-Token': 'undefined',
    'Origin': 'https://www.lifelock.com',
    'Referer': 'https://www.lifelock.com/breach-detection/',
    'TE': 'Trailers',
}


def parse_resp(content: dict, email: str) -> dict:
    if content['data']['results']:
        return result(email=email, service=__name__, is_leak=True)
    return result(email=email, service=__name__, is_leak=False)


async def lifelock(email: str) -> dict:
    bemail = base64.b64encode(email.encode('UTF-8'))
    data = {
        'email': bemail.decode('UTF-8'),
        'language': 'en',
        'country': 'us'
    }
    try:
        async with aiohttp.request(method='POST', url=lifelock_url, data=data, headers=get_headers(headers)) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.json(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
