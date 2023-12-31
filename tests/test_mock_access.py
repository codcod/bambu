# flake8: noqa
import json
from functools import partial

import pytest as pt
import pook

from bambu import api 
from bambu.camel import camelcase_keys, underscore_keys
from bambu.config import read_config

ACCESS_MODE = 'DIRECT'

cfg = read_config('.env')

DOMAIN =  'testdomain'
TOKEN = 'testtoken'
BASE_URL = 'https://api.bamboohr.com/api/gateway.php/' + DOMAIN

create_api = partial(api.create_api, subdomain=DOMAIN, api_key=TOKEN)


@pt.fixture
def resp_employee():
    return {
        'id': '4529',
        'firstName': 'Tester',
        'lastName': 'Tester',
        'employeeNumber': '4526',
        'ssn': None
    }

@pt.fixture
def resp_time_off():
    return json.loads(
        '''
        [
            {
                "id": "1",
                "employeeId": "1",
                "name": "Jon Doe",
                "status": {
                    "lastChanged": "2011-08-14",
                    "lastChangedByUserId": "1",
                    "status": "approved"
                },
                "start": "2001-01-01",
                "end": "2001-01-06",
                "created": "2011-08-13",
                "type": {
                    "id": "1",
                    "name": "Vacation",
                    "icon": "time-off-calendar"
                },
                "amount": {
                    "unit": "days",
                    "amount": "5"
                },
                "actions": {
                    "view": true,
                    "edit": true,
                    "cancel": true,
                    "approve": true,
                    "deny": true,
                    "bypass": true
                },
                "dates": {
                    "2001-01-01": "1",
                    "2001-01-02": "1",
                    "2001-01-03": "1",
                    "2001-01-04": "0",
                    "2001-01-05": "1",
                    "2001-01-06": "1"
                },
                "notes": {
                    "employee": "Relaxing in the country for a few days.",
                    "manager": "Have fun!"
                }
            }
        ]
        '''
    )


@pt.mark.asyncio
@pook.on
async def test_get_employee_existing(resp_employee) -> None:
    bamboo: api.API = create_api()

    pook.get(
        bamboo.url_for(api.Methods.GET_EMPLOYEE, id=4529),
        reply=200,
        response_type='json',
        response_json=resp_employee
    )
    
    async with bamboo:
        fields = 'firstName,lastName,employeeNumber,ssn'
        empl = await bamboo.get_employee(id=4529, fields=fields)
        
        assert empl is not None
        for field in fields.split(','):
            assert field in empl
        assert empl == resp_employee


@pt.mark.asyncio
@pook.on
async def test_get_time_off_requests(resp_time_off) -> None:
    bamboo: api.API = create_api()

    pook.get(
        bamboo.url_for(api.Methods.GET_TIME_OFF_REQUESTS),
        reply=200,
        response_type='json',
        response_json=resp_time_off
    )

    async with bamboo:
        r = await bamboo.get_time_off_requests(
            employee_id=1,
            start_date='2023-11-01',
            end_date='2023-11-30'        
        )
        assert r is not None
        assert r == resp_time_off
