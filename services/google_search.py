import aiohttp

from utils import print_error, unexpected_status, get_headers, result

google_url = 'https://google.com/search?q='


def parse_resp(content: str, email: str) -> dict:
    if '<div class="g">' in content:
        return result(email=email, service=__name__, is_leak=True)
    return result(email=email, service=__name__, is_leak=False)


async def google_search(email: str) -> dict:
    try:
        async with aiohttp.request(method='GET', url=f'{google_url}{email}', headers=get_headers()) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.text(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
