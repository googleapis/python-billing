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
from google.cloud.billing_v1.proto import cloud_billing_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2


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


class TestCloudBillingClient(object):
    def test_get_billing_account(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        open_ = True
        display_name = "displayName1615086568"
        master_billing_account = "masterBillingAccount1503143052"
        expected_response = {
            "name": name_2,
            "open": open_,
            "display_name": display_name,
            "master_billing_account": master_billing_account,
        }
        expected_response = cloud_billing_pb2.BillingAccount(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        name = client.billing_account_path("[BILLING_ACCOUNT]")

        response = client.get_billing_account(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.GetBillingAccountRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_billing_account_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        name = client.billing_account_path("[BILLING_ACCOUNT]")

        with pytest.raises(CustomException):
            client.get_billing_account(name)

    def test_list_billing_accounts(self):
        # Setup Expected Response
        next_page_token = ""
        billing_accounts_element = {}
        billing_accounts = [billing_accounts_element]
        expected_response = {
            "next_page_token": next_page_token,
            "billing_accounts": billing_accounts,
        }
        expected_response = cloud_billing_pb2.ListBillingAccountsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        paged_list_response = client.list_billing_accounts()
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.billing_accounts[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.ListBillingAccountsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_billing_accounts_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        paged_list_response = client.list_billing_accounts()
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_billing_account(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        open_ = True
        display_name = "displayName1615086568"
        master_billing_account = "masterBillingAccount1503143052"
        expected_response = {
            "name": name_2,
            "open": open_,
            "display_name": display_name,
            "master_billing_account": master_billing_account,
        }
        expected_response = cloud_billing_pb2.BillingAccount(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        name = client.billing_account_path("[BILLING_ACCOUNT]")
        account = {}

        response = client.update_billing_account(name, account)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.UpdateBillingAccountRequest(
            name=name, account=account
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_billing_account_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        name = client.billing_account_path("[BILLING_ACCOUNT]")
        account = {}

        with pytest.raises(CustomException):
            client.update_billing_account(name, account)

    def test_create_billing_account(self):
        # Setup Expected Response
        name = "name3373707"
        open_ = True
        display_name = "displayName1615086568"
        master_billing_account = "masterBillingAccount1503143052"
        expected_response = {
            "name": name,
            "open": open_,
            "display_name": display_name,
            "master_billing_account": master_billing_account,
        }
        expected_response = cloud_billing_pb2.BillingAccount(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        billing_account = {}

        response = client.create_billing_account(billing_account)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.CreateBillingAccountRequest(
            billing_account=billing_account
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_billing_account_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        billing_account = {}

        with pytest.raises(CustomException):
            client.create_billing_account(billing_account)

    def test_list_project_billing_info(self):
        # Setup Expected Response
        next_page_token = ""
        project_billing_info_element = {}
        project_billing_info = [project_billing_info_element]
        expected_response = {
            "next_page_token": next_page_token,
            "project_billing_info": project_billing_info,
        }
        expected_response = cloud_billing_pb2.ListProjectBillingInfoResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        name = client.billing_account_path("[BILLING_ACCOUNT]")

        paged_list_response = client.list_project_billing_info(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.project_billing_info[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.ListProjectBillingInfoRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_project_billing_info_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        name = client.billing_account_path("[BILLING_ACCOUNT]")

        paged_list_response = client.list_project_billing_info(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_project_billing_info(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        project_id = "projectId-1969970175"
        billing_account_name = "billingAccountName-1056086879"
        billing_enabled = False
        expected_response = {
            "name": name_2,
            "project_id": project_id,
            "billing_account_name": billing_account_name,
            "billing_enabled": billing_enabled,
        }
        expected_response = cloud_billing_pb2.ProjectBillingInfo(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        name = "name3373707"

        response = client.get_project_billing_info(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.GetProjectBillingInfoRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_project_billing_info_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        name = "name3373707"

        with pytest.raises(CustomException):
            client.get_project_billing_info(name)

    def test_update_project_billing_info(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        project_id = "projectId-1969970175"
        billing_account_name = "billingAccountName-1056086879"
        billing_enabled = False
        expected_response = {
            "name": name_2,
            "project_id": project_id,
            "billing_account_name": billing_account_name,
            "billing_enabled": billing_enabled,
        }
        expected_response = cloud_billing_pb2.ProjectBillingInfo(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        name = "name3373707"

        response = client.update_project_billing_info(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_billing_pb2.UpdateProjectBillingInfoRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_project_billing_info_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        name = "name3373707"

        with pytest.raises(CustomException):
            client.update_project_billing_info(name)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        resource = "resource-341064690"

        response = client.get_iam_policy(resource)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        resource = "resource-341064690"

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        resource = "resource-341064690"
        policy = {}

        response = client.set_iam_policy(resource, policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        resource = "resource-341064690"
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

    def test_test_iam_permissions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup Request
        resource = "resource-341064690"
        permissions = []

        response = client.test_iam_permissions(resource, permissions)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_test_iam_permissions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = billing_v1.CloudBillingClient()

        # Setup request
        resource = "resource-341064690"
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
