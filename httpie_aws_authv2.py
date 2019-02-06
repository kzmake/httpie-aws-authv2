"""
AWS auth v2 plugin for HTTPie.
"""
import os
import time
from urllib.parse import parse_qsl, urlencode
from urllib.parse import urlparse, urlunparse

import requests
from botocore.auth import SigV2Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from httpie.plugins import AuthPlugin

__version__ = '0.0.1'
__author__ = 'kzmake'
__licence__ = 'MIT'

ACCESS_KEY = 'ACCESS_KEY_ID'
SECRET_KEY = 'SECRET_ACCESS_KEY'

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class AWSv2Auth(SigV2Auth):
    def __init__(self, credentials: Credentials):
        super().__init__(credentials)

    def add_auth(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        rr = r.copy()
        url = urlparse(r.url)

        if 'Host' in r.headers:
            netloc = r.headers['Host'].decode('utf-8')
        else:
            netloc = url.netloc

        rr.url = urlunparse((url.scheme, netloc, url.path, url.params, url.query, url.fragment))

        if r.method == 'POST':
            if r.body:
                body = dict(parse_qsl(r.body.decode("utf-8").strip()))
                r.body = urlencode(self.update_params(rr, body))
                new_headers = r.headers
                new_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
                r.headers = new_headers

        elif r.method == 'GET':
            url = urlparse(r.url)
            if url.query:
                new_query = urlencode(self.update_params(rr, dict(parse_qsl(url.query))))
                r.url = urlunparse((url.scheme, url.netloc, url.path, url.params, new_query, url.fragment))

        return r

    def update_params(self, r: requests.PreparedRequest, params: dict) -> dict:
        params['AccessKeyId'] = self.credentials.access_key
        params['SignatureVersion'] = '2'
        params['SignatureMethod'] = 'HmacSHA256'
        params['Timestamp'] = time.strftime(ISO8601, time.gmtime()) if 'Timestamp' not in params else params['Timestamp']
        request = AWSRequest(method=r.method, url=r.url, data=urlencode(params), headers=r.headers)
        _, signature = self.calc_signature(request, params)
        params['Signature'] = signature

        return params


class AWSAuth(object):
    def __init__(self, access_key=None, secret_key=None):
        self.aws_access_key = os.environ.get(ACCESS_KEY) if access_key is None else access_key
        self.aws_secret_key = os.environ.get(SECRET_KEY) if secret_key is None else secret_key

        if self.aws_access_key is None:
            raise RuntimeError('ERROR: ACCESS_KEY_ID is None')
        if self.aws_secret_key is None:
            raise RuntimeError('ERROR: SECRET_ACCESS_KEY is None')

        self.credentials = Credentials(self.aws_access_key, self.aws_secret_key)

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        AWSv2Auth(self.credentials).add_auth(r)

        return r


class AWSv2AuthPlugin(AuthPlugin):
    name = 'AWS auth-v2'
    auth_type = 'aws2'
    description = 'Sign requests using the AWS Signature Version 2 Signing Process'
    auth_require = False
    prompt_password = False

    def get_auth(self, username=None, password=None):
        access_key = username
        secret_key = password

        return AWSAuth(access_key=access_key, secret_key=secret_key)
