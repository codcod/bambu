import asyncio
import enum
from abc import ABC
from urllib.parse import urlencode

import aiohttp

from .config import read_config

Params = dict[str, str]


class Methods(enum.StrEnum):
    GET_EMPLOYEE = 'employees/{id}'
    GET_TIME_OFF_REQUESTS = 'time_off/requests'


class APIBase(ABC):
    def __init__(self, *, subdomain: str, api_key: str):
        self.subdomain = subdomain
        self.api_key = api_key

    @property
    def base_url(self) -> str:
        base_url = read_config('.env').get('BASE_URL')
        return f'{base_url}{self.subdomain}'

    def url_for(self, method: Methods, *, api_version: str = 'v1', **kwargs) -> str:
        base_url = read_config('.env').get('BASE_URL')
        m = method.format(**kwargs)
        return f'{base_url}{self.subdomain}/{api_version}/{m}'

    async def _get(self, method: str, params: Params, api_version: str = 'v1') -> dict:
        assert method is not None
        url = '{}/{}/{}?{}'.format(
            self.base_url, api_version, method, urlencode(params)
        )
        async with self._session.get(url, timeout=35) as response:
            if response.status == 200:
                r = await response.json()
                return r

    async def __aenter__(self):
        auth = aiohttp.BasicAuth(login=self.api_key)
        self._session = aiohttp.ClientSession(
            auth=auth, headers=self.headers, loop=asyncio.get_event_loop()
        )

    async def __aexit__(self, *args):
        await self._session.close()


class API(APIBase):
    def __init__(self, *, subdomain: str, api_key: str):
        self.headers = {'Accept': 'application/json'}
        super().__init__(subdomain=subdomain, api_key=api_key)

    async def get_employee(
        self,
        *,
        id: int,
        fields: str = 'firstName,lastName',
        only_current: bool = True,
        **kwargs,
    ) -> dict:
        assert id
        assert fields

        method = Methods.GET_EMPLOYEE.format(id=id)

        params = kwargs | {
            'id': id,
            'fields': fields,
            'onlyCurrent': only_current,
        }
        r = await self._get(method, params)
        return r

    async def get_time_off_requests(
        self,
        *,
        employee_id: int,
        start_date: str,
        end_date: str,
        id: int = None,
        action: str = None,
        **kwargs,
    ) -> dict:
        assert start_date
        assert end_date
        assert action in ('view', 'approve', None)

        method = Methods.GET_TIME_OFF_REQUESTS

        params = kwargs | {
            'employeeId': employee_id,
            'start': start_date,
            'end': end_date,
        }
        r = await self._get(method, params)
        return r


def create_api(subdomain: str, api_key: str) -> APIBase:
    return API(subdomain=subdomain, api_key=api_key)
