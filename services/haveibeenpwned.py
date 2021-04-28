import aiohttp

from utils import print_error, unexpected_status, get_headers, result

haveibeenpwned_url = 'https://haveibeenpwned.com/unifiedsearch/'


async def haveibeenpwned(email: str) -> dict:
    try:
        async with aiohttp.request(method='GET', url=f'{haveibeenpwned_url}{email}', headers=get_headers()) as resp:
            if resp.status == 200:
                return result(email=email, service=__name__, is_leak=True)
            elif resp.status == 404:
                return result(email=email, service=__name__, is_leak=False)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
