"""Interfaces for calling PyCloud services"""
#
# Copyright (C) 2020 PyCloud - All Rights Reserved
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from base64 import b64encode
from abc import ABC, abstractmethod
from typing import Dict
import pickle
import logging

import grpc
import json_tricks
import requests

from pycloud_client.proto.pycloud_pb2 import Request
from pycloud_client.proto.pycloud_pb2_grpc import EndpointStub
from pycloud_client.utils import serialize, utc_timestamp_ms

LOGGER = logging.getLogger("PyCloudClient")


class PyCloudClient(ABC):  # pylint: disable=too-few-public-methods
    """Base class for http and grpc clients"""

    def __init__(self, host, port=None, client_id=""):
        self.client_id = client_id
        self.port = port
        self.host = host
        self.addr = host
        if self.port is not None:
            self.addr += ":{}".format(port)

    @abstractmethod
    def request(self, endpoint_id, *args, **kwargs):
        """ Send request to the endpoint"""


class GRPCClient(PyCloudClient):  # pylint: disable=too-few-public-methods
    """Fast GRPC client - use it for best performance"""

    def request(self, endpoint_id: str, *args, **kwargs):
        return grpc_request(self.client_id, endpoint_id, args, kwargs, self.addr)


class HTTPClient(PyCloudClient):  # pylint: disable=too-few-public-methods
    """HTTP client - slow"""

    def __init__(self, host, port=None, client_id="", auth=None):
        super().__init__(host, port, client_id)
        self.auth = auth

    def request(self, endpoint_id, *args, **kwargs):
        return http_request(self.client_id, endpoint_id, args, kwargs,
                            self.addr, self.auth)


def grpc_request(source_id, endpoint_id, args, kwargs, service_addr):
    """Call GRPC endpoint"""
    channel = grpc.insecure_channel(service_addr)
    stub = EndpointStub(channel)
    request = _create_grpc_message(endpoint_id, args, kwargs, source_id)
    response = stub.ProcessRequest(request)
    # unsafe, make sure to call only trusted endpoints
    return pickle.loads(response.response)


def _create_grpc_message(endpoint_id, args, kwargs, source_id):
    serialized_args = serialize(args)
    serialized_kwargs = serialize(kwargs)
    request = Request(
        timestamp=str(utc_timestamp_ms()),
        source_id=source_id,
        endpoint_id=endpoint_id,
        args=serialized_args,
        kwargs=serialized_kwargs,
    )
    return request


def http_request(source_id, endpoint_id, args, kwargs,  # pylint: disable=too-many-arguments
                 service_addr, auth=None):
    """Call http endpoint"""
    headers = {"content-type": "application/json"}
    if auth is not None:
        headers["Authorization"] = basic_auth_header(auth)
    payload = _create_http_message(args, endpoint_id, kwargs, source_id)
    url = service_addr
    if not url.startswith("http"):
        url = "http://" + url
    LOGGER.debug("Url: %s", url)
    response = requests.post(url, data=payload, headers=headers)
    return_value = None
    if response.status_code < 300:
        return_value = json_tricks.loads(response.content.decode("utf-8"))
    return return_value, response.status_code


def basic_auth_header(auth: Dict[str, str]):
    """Create basic auth header from dict"""
    return "Basic " + b64encode(bytes(auth["username"] + ":" + auth["password"],
                                      encoding="utf-8")).decode("utf-8")


def _create_http_message(args, endpoint_id, kwargs, source_id):
    payload = {
        "timestamp": str(utc_timestamp_ms()),
        "source_id": source_id,
        "endpoint_id": endpoint_id,
        "args": args,
        "kwargs": kwargs,
    }
    payload = json_tricks.dumps(payload)
    return payload

