import pytest as pt
from bambu import bambu 
from functools import partial
from bambu.camel import underscore_keys

from bambu.config import read_config
cfg = read_config('.env')

DOMAIN = cfg.get('DOMAIN')
TOKEN = cfg.get('TOKEN')

create_api = partial(bambu.create_api, subdomain=DOMAIN, api_key=TOKEN)

@pt.mark.asyncio
async def test_capacity() -> None:
    api: bambu.APIv1 = create_api()
    async with api:
        # params = {'start': '2023-11-01', 'end': '2023-11-30', 'employeeId': 4133}
        # r = await api.get_time_off_requests(params)

        r = await api.get_time_off_requests(employee_id=4133, start_date='2023-11-01', end_date='2023-11-30')
        assert r is not None
        print(f'api.get_time_off_requests = {r}')

        amount = r[0]['amount']
        match amount['unit']:
            case 'days': days = int(amount['amount'])
            case 'hours': days = int(amount['amount']) / 8
        print(f'{days=}')

        print('...and with underscore keys')
        for x in r:
            print(f'api.get_time_off_requests = {underscore_keys(x)}')