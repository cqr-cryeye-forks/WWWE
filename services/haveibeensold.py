import aiohttp

from utils import print_error, unexpected_status, get_headers, result

haveibeensold_url = 'https://haveibeensold.app/api/api.php'


def parse_resp(content: dict, email: str) -> dict:
    if content['data'] and content['data'] != 'E_NOT_VALID':
        return result(email=email, service=__name__, is_leak=True)
    return result(email=email, service=__name__, is_leak=False)


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
