from aiohttp import ClientSession

from utils import print_error, set_headers, unexpected_status

haveibeenpwned_url = 'https://haveibeenpwned.com/unifiedsearch/'


async def haveibeenpwned(email: str, session: ClientSession) -> dict:
    try:
        set_headers(s=session)
        async with session.get(f'{haveibeenpwned_url}{email}', verify_ssl=False) as resp:
            if resp.status == 200:
                return {'result': f'The mailing address: {email} was found in a Haveibeenpwned service.'}
            elif resp.status == 404:
                return {'result': f'The mailing address: {email} was not found in a Haveibeenpwned service.'}
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
