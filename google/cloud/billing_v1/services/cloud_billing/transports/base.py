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

import abc
import typing
import pkg_resources

from google import auth
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1    # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.billing_v1.types import cloud_billing
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            'google-cloud-billing',
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()

class CloudBillingTransport(abc.ABC):
    """Abstract transport class for CloudBilling."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
    )

    def __init__(
            self, *,
            host: str = 'cloudbilling.googleapis.com',
            credentials: credentials.Credentials = None,
            credentials_file: typing.Optional[str] = None,
            scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
            quota_project_id: typing.Optional[str] = None,
            **kwargs,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs("'credentials_file' and 'credentials' are mutually exclusive")

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                                credentials_file,
                                scopes=scopes,
                                quota_project_id=quota_project_id
                            )

        elif credentials is None:
            credentials, _ = auth.default(scopes=scopes, quota_project_id=quota_project_id)

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages()

    def _prep_wrapped_messages(self):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.get_billing_account: gapic_v1.method.wrap_method(
                self.get_billing_account,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.list_billing_accounts: gapic_v1.method.wrap_method(
                self.list_billing_accounts,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.update_billing_account: gapic_v1.method.wrap_method(
                self.update_billing_account,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.create_billing_account: gapic_v1.method.wrap_method(
                self.create_billing_account,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.list_project_billing_info: gapic_v1.method.wrap_method(
                self.list_project_billing_info,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.get_project_billing_info: gapic_v1.method.wrap_method(
                self.get_project_billing_info,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.update_project_billing_info: gapic_v1.method.wrap_method(
                self.update_project_billing_info,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=_client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=_client_info,
            ),

        }

    @property
    def get_billing_account(self) -> typing.Callable[
            [cloud_billing.GetBillingAccountRequest],
            typing.Union[
                cloud_billing.BillingAccount,
                typing.Awaitable[cloud_billing.BillingAccount]
            ]]:
        raise NotImplementedError()

    @property
    def list_billing_accounts(self) -> typing.Callable[
            [cloud_billing.ListBillingAccountsRequest],
            typing.Union[
                cloud_billing.ListBillingAccountsResponse,
                typing.Awaitable[cloud_billing.ListBillingAccountsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def update_billing_account(self) -> typing.Callable[
            [cloud_billing.UpdateBillingAccountRequest],
            typing.Union[
                cloud_billing.BillingAccount,
                typing.Awaitable[cloud_billing.BillingAccount]
            ]]:
        raise NotImplementedError()

    @property
    def create_billing_account(self) -> typing.Callable[
            [cloud_billing.CreateBillingAccountRequest],
            typing.Union[
                cloud_billing.BillingAccount,
                typing.Awaitable[cloud_billing.BillingAccount]
            ]]:
        raise NotImplementedError()

    @property
    def list_project_billing_info(self) -> typing.Callable[
            [cloud_billing.ListProjectBillingInfoRequest],
            typing.Union[
                cloud_billing.ListProjectBillingInfoResponse,
                typing.Awaitable[cloud_billing.ListProjectBillingInfoResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_project_billing_info(self) -> typing.Callable[
            [cloud_billing.GetProjectBillingInfoRequest],
            typing.Union[
                cloud_billing.ProjectBillingInfo,
                typing.Awaitable[cloud_billing.ProjectBillingInfo]
            ]]:
        raise NotImplementedError()

    @property
    def update_project_billing_info(self) -> typing.Callable[
            [cloud_billing.UpdateProjectBillingInfoRequest],
            typing.Union[
                cloud_billing.ProjectBillingInfo,
                typing.Awaitable[cloud_billing.ProjectBillingInfo]
            ]]:
        raise NotImplementedError()

    @property
    def get_iam_policy(self) -> typing.Callable[
            [iam_policy.GetIamPolicyRequest],
            typing.Union[
                policy.Policy,
                typing.Awaitable[policy.Policy]
            ]]:
        raise NotImplementedError()

    @property
    def set_iam_policy(self) -> typing.Callable[
            [iam_policy.SetIamPolicyRequest],
            typing.Union[
                policy.Policy,
                typing.Awaitable[policy.Policy]
            ]]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(self) -> typing.Callable[
            [iam_policy.TestIamPermissionsRequest],
            typing.Union[
                iam_policy.TestIamPermissionsResponse,
                typing.Awaitable[iam_policy.TestIamPermissionsResponse]
            ]]:
        raise NotImplementedError()


__all__ = (
    'CloudBillingTransport',
)
