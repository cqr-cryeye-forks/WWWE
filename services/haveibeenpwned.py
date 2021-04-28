import aiohttp

from utils import print_error, unexpected_status, get_headers

haveibeenpwned_url = 'https://haveibeenpwned.com/unifiedsearch/'


async def haveibeenpwned(email: str) -> dict:
    try:
        async with aiohttp.request(method='GET', url=f'{haveibeenpwned_url}{email}', headers=get_headers()) as resp:
            if resp.status == 200:
                return {'result': f'The mailing address: {email} was found in a Haveibeenpwned service.'}
            elif resp.status == 404:
                return {'result': f'The mailing address: {email} was not found in a Haveibeenpwned service.'}
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
