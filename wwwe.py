import asyncio
import json
from inspect import isfunction, getmembers

import services
from services.firefox import firefox
from services.inoitsu import inoitsu
from services.leakedsource import leakedsource
from utils import parse_args, driver


async def main():
    args = parse_args()

    with driver() as d:
        results = [
            firefox(d=d, email=args.email),
            leakedsource(d=d, email=args.email),
            inoitsu(d=d, email=args.email)
        ]

    tasks = [asyncio.ensure_future(func(args.email)) for _, func in getmembers(services, isfunction)]
    results.extend(filter(None, await asyncio.gather(*tasks)))

    with open('output.json', 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == '__main__':
    asyncio.run(main())
