import pytest as pt
from bambu import bambu 
from functools import partial
from bambu.camel import camelcase_keys, underscore_keys

from bambu.config import read_config
cfg = read_config('.env')

DOMAIN = cfg.get('DOMAIN')
TOKEN = cfg.get('TOKEN')

create_api = partial(bambu.create_api, subdomain=DOMAIN, api_key=TOKEN)

@pt.mark.asyncio
async def test_get_employee_existing() -> None:
    api: bambu.APIv1 = create_api()
    async with api:
        fields = 'firstName,lastName,employeeNumber,ssn,departament'
        emp = await api.get_employee(id=4529, fields=fields)
        assert emp is not None
        print(f'{emp=}')
        print(f'with underscore keys = {underscore_keys(emp)}')

@pt.mark.asyncio
async def test_get_employee_nonexisting() -> None:
    api: bambu.APIv1 = create_api()
    async with api:
        emp = await api.get_employee(id=100_000)
        assert emp is None

@pt.mark.asyncio
async def _test_get_time_off_requests() -> None:
    api: bambu.APIv1 = create_api()
    async with api:
        r = await api.get_time_off_requests(employee_id=4133)
        assert r is not None
        print(f'api.get_time_off_requests for employee_id=4133 = {r}')
        print(f'...amount part only = {r[0]['amount']}')
