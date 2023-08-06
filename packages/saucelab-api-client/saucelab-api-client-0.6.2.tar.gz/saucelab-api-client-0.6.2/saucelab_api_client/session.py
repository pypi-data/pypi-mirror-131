import configparser
import json
import os

import requests

from saucelab_api_client.models.service import Auth, Host


class Session:
    def __init__(self, host: str = None, username: str = None, token: str = None, env_policy: str = 'clear'):
        """
        https://docs.saucelabs.com/dev/api/

        Insert your api server
        :param host:
        :param username: your username
        :param token: tour API token
        :param env_policy: str
        """
        self.__host: str
        self._device_cache = os.path.join(os.path.dirname(__file__), 'devices.json')
        self._session = requests.Session()
        self.__get_auth(host, username, token, env_policy)
        del host, username, token
        if self.__host[-1] == '/':
            self.__host = self.__host[:-1]
        self.driver = Host(self._session, self.__host)

    def request(self, method: str, url: str, data: dict = None, params: dict = None,
                return_type: str = False, **kwargs):
        data = json.dumps(data) if data else ''
        if 'download' in url or 'upload' in url:
            self._session.headers.pop('Content-Type', None)
        else:
            self._session.headers.update({'Content-Type': 'application/json'})
        response = self._session.request(method=method, url=f'{self.__host}{url}', data=data, params=params, **kwargs)
        if response.status_code in (200, 201):
            if return_type == 'text':
                return response.text
            elif return_type == 'content':
                return response.content
            else:
                return response.json()
        else:
            return f'Error: {response.status_code}: {response.reason} ({response.text})'

    def __get_auth(self, host: str = None, username: str = None, token: str = None, env_policy: str = None):

        if all((host, username, token)):
            self._session.auth, self.__host = Auth(username, token), host
            return
        else:

            path, config = os.path.dirname(__file__), configparser.ConfigParser()
            for _ in range(7):
                for file in ('pytest', 'saucelab'):
                    file_name = os.path.join(path, f'{file}.ini')
                    if os.path.isfile(file_name):
                        config.read(file_name)
                        if config.has_section('saucelab'):
                            options = config.options('saucelab')
                            if all((option in options for option in
                                    ('saucelab_username', 'saucelab_token', 'saucelab_host'))):
                                sauce = config['saucelab']
                                self._session.auth = Auth(sauce['saucelab_username'], sauce['saucelab_token'])
                                self.__host = sauce['saucelab_host']
                                return
                path = os.path.dirname(path)

            env_username, env_token = os.environ.get('SAUCELAB_USERNAME', None), os.environ.get('SAUCELAB_TOKEN', None)
            env_host = os.environ.get('SAUCELAB_HOST', None)
            if all((env_username, env_token, env_host)):
                self._session.auth = Auth(env_username, env_token)
                self.__host = env_host
                if env_policy == 'clear':
                    tuple(map(os.environ.pop, ('SAUCELAB_USERNAME', 'SAUCELAB_TOKEN', 'SAUCELAB_HOST')))
                return
        self.__host = '/'
        self._session.auth = Auth('', '')
