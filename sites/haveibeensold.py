import aiohttp

from utils import print_error, unexpected_status, get_headers

haveibeensold_url = 'https://haveibeensold.app/api/api.php'


def parse_resp(content: dict, email: str) -> dict:
    if content['data'] and content['data'] != 'E_NOT_VALID':
        return {'result': f'The mailing address: {email} was found in a Haveibeensold service.'}
    return {'result': f'The mailing address: {email} was not found in a Haveibeensold service.'}


async def haveibeensold(email: str) -> dict:
    data = {
        'email': email,
        'action': 'check'
    }
    try:
        async with aiohttp.request(method='POST', url=haveibeensold_url, data=data, headers=get_headers()) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.json(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
