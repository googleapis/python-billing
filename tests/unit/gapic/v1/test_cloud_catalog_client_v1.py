# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests."""

import mock
import pytest

from google.cloud import billing_v1
from google.cloud.billing_v1.proto import cloud_catalog_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestCloudCatalogClient(object):
    def test_list_services(self):
        # Setup Expected Response
        next_page_token = ""
        services_element = {}
        services = [services_element]
        expected_response = {"next_page_token": next_page_token, "services": services}
        expected_response = cloud_catalog_pb2.ListServicesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudCatalogClient()

        paged_list_response = client.list_services()
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.services[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloud_catalog_pb2.ListServicesRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_services_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudCatalogClient()

        paged_list_response = client.list_services()
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_skus(self):
        # Setup Expected Response
        next_page_token = ""
        skus_element = {}
        skus = [skus_element]
        expected_response = {"next_page_token": next_page_token, "skus": skus}
        expected_response = cloud_catalog_pb2.ListSkusResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudCatalogClient()

        # Setup Request
        parent = client.service_path("[SERVICE]")

        paged_list_response = client.list_skus(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.skus[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloud_catalog_pb2.ListSkusRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_skus_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudCatalogClient()

        # Setup request
        parent = client.service_path("[SERVICE]")

        paged_list_response = client.list_skus(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
