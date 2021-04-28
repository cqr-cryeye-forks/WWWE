import asyncio
import json
from inspect import isfunction, getmembers

import aiohttp

import sites
from sites.firefox import firefox
from sites.leakedsource import leakedsource
from utils import parse_args, driver


async def main():
    args = parse_args()

    with driver() as d:
        results = [firefox(d=d, email=args.email), leakedsource(d=d, email=args.email)]

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(func(args.email, session)) for _, func in getmembers(sites, isfunction)]
        results.extend(filter(None, await asyncio.gather(*tasks)))

    with open('output.json', 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == '__main__':
    asyncio.run(main())
