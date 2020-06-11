# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.billing_v1.services.cloud_billing import CloudBillingClient
from google.cloud.billing_v1.services.cloud_billing import pagers
from google.cloud.billing_v1.services.cloud_billing import transports
from google.cloud.billing_v1.types import cloud_billing
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CloudBillingClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudBillingClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudBillingClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudBillingClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudBillingClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudBillingClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_cloud_billing_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = CloudBillingClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = CloudBillingClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "cloudbilling.googleapis.com:443"


def test_cloud_billing_client_get_transport_class():
    transport = CloudBillingClient.get_transport_class()
    assert transport == transports.CloudBillingGrpcTransport

    transport = CloudBillingClient.get_transport_class("grpc")
    assert transport == transports.CloudBillingGrpcTransport


def test_cloud_billing_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.CloudBillingClient.get_transport_class"
    ) as gtc:
        transport = transports.CloudBillingGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = CloudBillingClient(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.CloudBillingClient.get_transport_class"
    ) as gtc:
        client = CloudBillingClient(transport="grpc")
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBillingClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    os.environ["GOOGLE_API_USE_MTLS"] = "never"
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBillingClient()
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    os.environ["GOOGLE_API_USE_MTLS"] = "always"
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBillingClient()
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=None,
            credentials=None,
            host=client.DEFAULT_MTLS_ENDPOINT,
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBillingClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_MTLS_ENDPOINT,
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            grpc_transport.return_value = None
            client = CloudBillingClient()
            grpc_transport.assert_called_once_with(
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                credentials=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            grpc_transport.return_value = None
            client = CloudBillingClient()
            grpc_transport.assert_called_once_with(
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                credentials=None,
                host=client.DEFAULT_ENDPOINT,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    os.environ["GOOGLE_API_USE_MTLS"] = "Unsupported"
    with pytest.raises(MutualTLSChannelError):
        client = CloudBillingClient()

    del os.environ["GOOGLE_API_USE_MTLS"]


def test_cloud_billing_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.transports.CloudBillingGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBillingClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_get_billing_account(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.GetBillingAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount(
            name="name_value",
            open=True,
            display_name="display_name_value",
            master_billing_account="master_billing_account_value",
        )

        response = client.get_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.BillingAccount)
    assert response.name == "name_value"

    assert response.open is True
    assert response.display_name == "display_name_value"
    assert response.master_billing_account == "master_billing_account_value"


def test_get_billing_account_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.GetBillingAccountRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_billing_account), "__call__"
    ) as call:
        call.return_value = cloud_billing.BillingAccount()

        client.get_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_billing_account_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_billing_account(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_billing_account_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_billing_account(
            cloud_billing.GetBillingAccountRequest(), name="name_value"
        )


def test_list_billing_accounts(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.ListBillingAccountsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_billing_accounts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ListBillingAccountsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_billing_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBillingAccountsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_billing_accounts_pager():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_billing_accounts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[], next_page_token="def"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[cloud_billing.BillingAccount()], next_page_token="ghi"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_billing_accounts(request={})]
        assert len(results) == 6
        assert all(isinstance(i, cloud_billing.BillingAccount) for i in results)


def test_list_billing_accounts_pages():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_billing_accounts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[], next_page_token="def"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[cloud_billing.BillingAccount()], next_page_token="ghi"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ]
            ),
            RuntimeError,
        )
        pages = list(client.list_billing_accounts(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_update_billing_account(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.UpdateBillingAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount(
            name="name_value",
            open=True,
            display_name="display_name_value",
            master_billing_account="master_billing_account_value",
        )

        response = client.update_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.BillingAccount)
    assert response.name == "name_value"

    assert response.open is True
    assert response.display_name == "display_name_value"
    assert response.master_billing_account == "master_billing_account_value"


def test_update_billing_account_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.UpdateBillingAccountRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_billing_account), "__call__"
    ) as call:
        call.return_value = cloud_billing.BillingAccount()

        client.update_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_update_billing_account_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_billing_account(
            name="name_value", account=cloud_billing.BillingAccount(name="name_value")
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].account == cloud_billing.BillingAccount(name="name_value")


def test_update_billing_account_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_billing_account(
            cloud_billing.UpdateBillingAccountRequest(),
            name="name_value",
            account=cloud_billing.BillingAccount(name="name_value"),
        )


def test_create_billing_account(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.CreateBillingAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount(
            name="name_value",
            open=True,
            display_name="display_name_value",
            master_billing_account="master_billing_account_value",
        )

        response = client.create_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.BillingAccount)
    assert response.name == "name_value"

    assert response.open is True
    assert response.display_name == "display_name_value"
    assert response.master_billing_account == "master_billing_account_value"


def test_create_billing_account_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_billing_account(
            billing_account=cloud_billing.BillingAccount(name="name_value")
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].billing_account == cloud_billing.BillingAccount(
            name="name_value"
        )


def test_create_billing_account_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_billing_account(
            cloud_billing.CreateBillingAccountRequest(),
            billing_account=cloud_billing.BillingAccount(name="name_value"),
        )


def test_list_project_billing_info(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.ListProjectBillingInfoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ListProjectBillingInfoResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProjectBillingInfoPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_project_billing_info_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.ListProjectBillingInfoRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        call.return_value = cloud_billing.ListProjectBillingInfoResponse()

        client.list_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_list_project_billing_info_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ListProjectBillingInfoResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_project_billing_info(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_list_project_billing_info_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_project_billing_info(
            cloud_billing.ListProjectBillingInfoRequest(), name="name_value"
        )


def test_list_project_billing_info_pager():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[], next_page_token="def"
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[cloud_billing.ProjectBillingInfo()],
                next_page_token="ghi",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_project_billing_info(request={})]
        assert len(results) == 6
        assert all(isinstance(i, cloud_billing.ProjectBillingInfo) for i in results)


def test_list_project_billing_info_pages():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[], next_page_token="def"
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[cloud_billing.ProjectBillingInfo()],
                next_page_token="ghi",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ]
            ),
            RuntimeError,
        )
        pages = list(client.list_project_billing_info(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_project_billing_info(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.GetProjectBillingInfoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo(
            name="name_value",
            project_id="project_id_value",
            billing_account_name="billing_account_name_value",
            billing_enabled=True,
        )

        response = client.get_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.ProjectBillingInfo)
    assert response.name == "name_value"
    assert response.project_id == "project_id_value"
    assert response.billing_account_name == "billing_account_name_value"

    assert response.billing_enabled is True


def test_get_project_billing_info_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.GetProjectBillingInfoRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_project_billing_info), "__call__"
    ) as call:
        call.return_value = cloud_billing.ProjectBillingInfo()

        client.get_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_project_billing_info_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_project_billing_info(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_project_billing_info_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_project_billing_info(
            cloud_billing.GetProjectBillingInfoRequest(), name="name_value"
        )


def test_update_project_billing_info(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.UpdateProjectBillingInfoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo(
            name="name_value",
            project_id="project_id_value",
            billing_account_name="billing_account_name_value",
            billing_enabled=True,
        )

        response = client.update_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.ProjectBillingInfo)
    assert response.name == "name_value"
    assert response.project_id == "project_id_value"
    assert response.billing_account_name == "billing_account_name_value"

    assert response.billing_enabled is True


def test_update_project_billing_info_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.UpdateProjectBillingInfoRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_project_billing_info), "__call__"
    ) as call:
        call.return_value = cloud_billing.ProjectBillingInfo()

        client.update_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_update_project_billing_info_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_project_billing_info(
            name="name_value",
            project_billing_info=cloud_billing.ProjectBillingInfo(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].project_billing_info == cloud_billing.ProjectBillingInfo(
            name="name_value"
        )


def test_update_project_billing_info_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_project_billing_info(
            cloud_billing.UpdateProjectBillingInfoRequest(),
            name="name_value",
            project_billing_info=cloud_billing.ProjectBillingInfo(name="name_value"),
        )


def test_get_iam_policy(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_get_iam_policy_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_iam_policy(resource="resource_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"


def test_get_iam_policy_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value"
        )


def test_set_iam_policy(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={"resource": "resource_value", "policy": policy.Policy(version=774)}
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_iam_policy(resource="resource_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"


def test_set_iam_policy_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value"
        )


def test_test_iam_permissions(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"]
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={"resource": "resource_value", "permissions": ["permissions_value"]}
        )
        call.assert_called()


def test_test_iam_permissions_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.test_iam_permissions(
            resource="resource_value", permissions=["permissions_value"]
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"
        assert args[0].permissions == ["permissions_value"]


def test_test_iam_permissions_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudBillingGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = CloudBillingClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBillingGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = CloudBillingClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.CloudBillingGrpcTransport)


def test_cloud_billing_base_transport():
    # Instantiate the base transport.
    transport = transports.CloudBillingTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_billing_account",
        "list_billing_accounts",
        "update_billing_account",
        "create_billing_account",
        "list_project_billing_info",
        "get_project_billing_info",
        "update_project_billing_info",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_cloud_billing_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        CloudBillingClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_cloud_billing_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.CloudBillingGrpcTransport(host="squid.clam.whelk")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_cloud_billing_host_no_port():
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbilling.googleapis.com"
        ),
    )
    assert client._transport._host == "cloudbilling.googleapis.com:443"


def test_cloud_billing_host_with_port():
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbilling.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "cloudbilling.googleapis.com:8000"


def test_cloud_billing_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.CloudBillingGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_cloud_billing_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.CloudBillingGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_cloud_billing_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.CloudBillingGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
        )
        assert transport.grpc_channel == mock_grpc_channel
