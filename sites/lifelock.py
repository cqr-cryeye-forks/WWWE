import base64

from aiohttp import ClientSession

from utils import print_error, set_headers, unexpected_status

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
        return {'result': f'The mailing address: {email} was found in a Lifelock search service.'}
    return {'result': f'The mailing address: {email} was not found in a Lifelock search service.'}


async def lifelock(email: str, session: ClientSession) -> dict:
    bemail = base64.b64encode(email.encode('UTF-8'))
    data = {
        'email': bemail.decode('UTF-8'),
        'language': 'en',
        'country': 'us'
    }
    try:
        set_headers(s=session, headers=headers)
        async with session.post(lifelock_url, data=data, verify_ssl=False) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.json(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
