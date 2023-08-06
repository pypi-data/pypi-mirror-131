import json
import logging
import os

import requests
from werkzeug.exceptions import default_exceptions

LOG = logging.getLogger(__name__)


class ServiceClient:
    """[summary]
    TODO: make this sphinx format for auto-developer-docs generation
    version: If not provided, latest api version will be used
    Returns:
        [type]: [description]
    """

    # Change this as new headers and api versions are supported
    HEADER_MAP = {
        1: os.environ['CXR_V1_HEADER'],
        None: os.environ['CXR_LATEST_HEADER'],
    }

    def __init__(self, service_name, version=None, raise_errors=True):
        self.version = version
        self.service_name = service_name
        self.raise_errors = raise_errors
        self.config = ServiceConfig(service_name)
        if not self.config:
            raise ValueError(f"Service with name '{service_name}' does not exist in system config.")

    @property
    def uri(self):
        return f'/api{self.config.base_uri}'

    def get_version_header(self, version):
        if version not in self.HEADER_MAP:
            raise KeyError(f'Version "{version}" is not a valid API version.')
        return self.HEADER_MAP[version]

    def _request(self, version: str = None, url: str = '/', method: str = 'GET', headers: dict = {}, **kwargs):
        """[summary]
        Args:
            version (str, optional): The API Version for this request. Defaults to using class-level api version
            url (str, optional): The URL for this request. Defaults to '/'.
            method (str, optional): The method for this request. Defaults to 'GET'.
        Raises:
            default_exceptions: [description]
        Returns:
            [type]: [description]
        """
        LOG.info(f'Request method={method}, service={self.service_name}, url={self.uri + url}')
        result = requests.request(
            method=method,
            url=self.config.base_url + self.uri + url,
            headers={
                **headers,
                'Accept': self.get_version_header(version or self.version)
            },
            **kwargs
        )
        LOG.info(f'Response code={result.status_code}, service={self.service_name}')

        if not result.ok:
            LOG.info(result)
            LOG.info(result.__dict__)
            try:
                decoded = result.json()
            except json.decoder.JSONDecodeError:
                decoded = {}

            if self.raise_errors and 'message' in decoded and result.status_code in default_exceptions:
                raise default_exceptions[result.status_code](decoded['message'])
            elif self.raise_errors and result.status_code in default_exceptions:
                raise default_exceptions[result.status_code]()
            elif self.raise_errors:
                result.raise_for_status()
            else:
                return result, decoded
        else:
            # All services must return data key. Each service needs to be consistent in this way
            return result, result.json()['data']

    def post(self, **kwargs):
        return self._request(method='POST', **kwargs)

    def patch(self, **kwargs):
        return self._request(method='PATCH', **kwargs)

    def put(self, **kwargs):
        return self._request(method='PUT', **kwargs)

    def delete(self, **kwargs):
        return self._request(method='DELETE', **kwargs)

    def get(self, **kwargs):
        return self._request(method='GET', **kwargs)

    def options(self, **kwargs):
        return self._request(method='OPTIONS', **kwargs)


class ServiceConfig:
    ENVS = {
        'host': 'CXR_{service_name_upper}_HOST',
        'port': 'CXR_{service_name_upper}_PORT',
        'api_version': 'CXR_{service_name_upper}_API_VERSION',
        'base_uri': 'CXR_{service_name_upper}_BASE_URI',
        'protocol': 'CXR_{service_name_upper}_PROTOCOL',
    }

    def __init__(self, service_name):
        self.service_name = service_name.upper()
        for attr, name in ServiceConfig.ENVS.items():
            setattr(self, attr, os.environ[name.format(service_name_upper=self.service_name)])

    @property
    def base_url(self):
        return f'{self.protocol}://{self.host}:{self.port}'
