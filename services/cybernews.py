import aiohttp

from utils import print_error, unexpected_status, get_headers, result

cybernews_url = 'https://check.cybernews.com/chk/'


def parse_resp(content: dict, email: str) -> dict:
    if content['e']:
        return result(email=email, service=__name__, is_leak=True)
    return result(email=email, service=__name__, is_leak=False)


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
