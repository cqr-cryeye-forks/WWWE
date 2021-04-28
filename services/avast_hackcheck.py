import json
from typing import Union

import aiohttp

from utils import print_error, unexpected_status, get_headers

avast_url = 'https://identityprotection.avast.com/v1/web/query/site-breaches/unauthorized-data'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Vaar-Header-App-Product': 'hackcheck-web-avast',
    'Vaar-Header-App-Product-Name': 'hackcheck-web-avast',
    'Vaar-Header-App-Build-Version': '1.0.0',
    'Vaar-Version': '0',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://www.avast.com',
    'Referer': 'https://www.avast.com/',
}


def parse_resp(content: dict, email: str) -> Union[dict, None]:
    try:
        if content['breaches']:
            return {'result': f'The mailing address: {email} was found in a Avast Hackcheck service.'}
        return {'result': f'The mailing address: {email} was not found in a Avast Hackcheck search service.'}
    except TypeError:
        return None


async def avast_hackcheck(email: str) -> dict:
    data = json.dumps({
        'emailAddresses': [email]
    })
    try:
        async with aiohttp.request(method='POST', url=avast_url, data=data, headers=get_headers(headers)) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.json(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
