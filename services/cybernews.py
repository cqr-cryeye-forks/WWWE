import aiohttp
from aiohttp import ClientSession

from utils import print_error, unexpected_status, get_headers

cybernews_url = 'https://check.cybernews.com/chk/'


def parse_resp(content: dict, email: str) -> dict:
    if content['e']:
        return {'result': f'The mailing address: {email} was found in a Cybernews Leak Check service.'}
    return {'result': f'The mailing address: {email} was not found in a Cybernews Leak Check service.'}


async def cybernews(email: str) -> dict:
    data = {
        'lang': 'en_US',
        'e': email
    }
    try:
        async with aiohttp.request(method='POST', url=cybernews_url, data=data, headers=get_headers()) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.json(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
