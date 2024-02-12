# pylint: disable=C0114,C0115,C0116
from functools import partial

import pytest as pt
from bambu import api
from bambu.config import read_config

cfg = read_config('.env')

DOMAIN = cfg.get('DOMAIN')
TOKEN = cfg.get('TOKEN')

create_api = partial(api.create_api, subdomain=DOMAIN, api_key=TOKEN)


@pt.mark.asyncio
async def test_get_employee_existing() -> None:
    bamboo: api.API = create_api()
    async with bamboo:
        fields = 'firstName,lastName,employeeNumber,ssn'  # ',departament'
        empl = await bamboo.get_employee(id=4529, fields=fields)
        assert empl is not None
        for field in fields.split(','):
            assert field in empl
        assert empl.get('id') == '4529'
        assert empl.get('employeeNumber') == '4526'


@pt.mark.asyncio
async def test_get_employee_nonexisting() -> None:
    bamboo: api.API = create_api()
    async with bamboo:
        empl = await bamboo.get_employee(id=100_000)
        assert empl is None


@pt.mark.asyncio
async def test_get_time_off_requests() -> None:
    bamboo: api.API = create_api()
    async with bamboo:
        r = await bamboo.get_time_off_requests(
            employee_id=4133, start_date='2023-11-01', end_date='2023-11-30'
        )
        assert r is not None
        print(f'api.get_time_off_requests for employee_id=4133 = {r}')
        print(f'...amount part only = {r[0]["amount"]}')
