from aiohttp import ClientSession

from utils import print_error, unexpected_status, set_headers

inoitsu_url = 'https://www.hotsheet.com/inoitsu/'


def parse_resp(content: str, email: str) -> dict:
    if not ('no breaches found' in content.lower()):
        return {'result': f'The mailing address: {email} was found in a Inoitsu service.'}
    return {'result': f'The mailing address: {email} was not found in a Inoitsu search service.'}


async def inoitsu(email: str, session: ClientSession) -> dict:
    data = {
        'act': email,
        'accounthide': 'test',
        'submit': 'Submit'
    }
    try:
        set_headers(s=session)
        async with session.post(inoitsu_url, data=data, verify_ssl=False) as resp:
            if resp.status == 200:
                return parse_resp(content=await resp.text(), email=email)
            else:
                await unexpected_status(resp=resp, service=__name__)
    except Exception as e:
        print_error(e, service=__name__)
