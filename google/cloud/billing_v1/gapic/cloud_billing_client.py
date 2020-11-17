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

"""Accesses the google.cloud.billing.v1 CloudBilling API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.billing_v1.gapic import cloud_billing_client_config
from google.cloud.billing_v1.gapic import enums
from google.cloud.billing_v1.gapic.transports import cloud_billing_grpc_transport
from google.cloud.billing_v1.proto import cloud_billing_pb2
from google.cloud.billing_v1.proto import cloud_billing_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-billing",).version


class CloudBillingClient(object):
    """Retrieves GCP Console billing accounts and associates them with projects."""

    SERVICE_ADDRESS = "cloudbilling.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.billing.v1.CloudBilling"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudBillingClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def billing_account_path(cls, billing_account):
        """Return a fully-qualified billing_account string."""
        return google.api_core.path_template.expand(
            "billingAccounts/{billing_account}", billing_account=billing_account,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.CloudBillingGrpcTransport,
                    Callable[[~.Credentials, type], ~.CloudBillingGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = cloud_billing_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=cloud_billing_grpc_transport.CloudBillingGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cloud_billing_grpc_transport.CloudBillingGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def get_billing_account(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets information about a billing account. The current authenticated
        user must be a `viewer of the billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> name = client.billing_account_path('[BILLING_ACCOUNT]')
            >>>
            >>> response = client.get_billing_account(name)

        Args:
            name (str): Required. The resource name of the billing account to retrieve. For
                example, ``billingAccounts/012345-567890-ABCDEF``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.BillingAccount` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_billing_account" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_billing_account"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_billing_account,
                default_retry=self._method_configs["GetBillingAccount"].retry,
                default_timeout=self._method_configs["GetBillingAccount"].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.GetBillingAccountRequest(name=name,)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_billing_account"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_billing_accounts(
        self,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the billing accounts that the current authenticated user has
        permission to
        `view <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_billing_accounts():
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_billing_accounts().pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): Options for how to filter the returned billing accounts. Currently
                this only supports filtering for
                `subaccounts <https://cloud.google.com/billing/docs/concepts>`__ under a
                single provided reseller billing account. (e.g.
                "master_billing_account=billingAccounts/012345-678901-ABCDEF"). Boolean
                algebra and other fields are not currently supported.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.billing_v1.types.BillingAccount` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_billing_accounts" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_billing_accounts"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_billing_accounts,
                default_retry=self._method_configs["ListBillingAccounts"].retry,
                default_timeout=self._method_configs["ListBillingAccounts"].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.ListBillingAccountsRequest(
            page_size=page_size, filter=filter_,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_billing_accounts"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="billing_accounts",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_billing_account(
        self,
        name,
        account,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a billing account's fields. Currently the only field that
        can be edited is ``display_name``. The current authenticated user must
        have the ``billing.accounts.update`` IAM permission, which is typically
        given to the
        `administrator <https://cloud.google.com/billing/docs/how-to/billing-access>`__
        of the billing account.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> name = client.billing_account_path('[BILLING_ACCOUNT]')
            >>>
            >>> # TODO: Initialize `account`:
            >>> account = {}
            >>>
            >>> response = client.update_billing_account(name, account)

        Args:
            name (str): Required. The name of the billing account resource to be updated.
            account (Union[dict, ~google.cloud.billing_v1.types.BillingAccount]): Required. The billing account resource to replace the resource on the server.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.billing_v1.types.BillingAccount`
            update_mask (Union[dict, ~google.cloud.billing_v1.types.FieldMask]): The update mask applied to the resource. Only "display_name" is
                currently supported.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.billing_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.BillingAccount` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_billing_account" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_billing_account"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_billing_account,
                default_retry=self._method_configs["UpdateBillingAccount"].retry,
                default_timeout=self._method_configs["UpdateBillingAccount"].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.UpdateBillingAccountRequest(
            name=name, account=account, update_mask=update_mask,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_billing_account"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_billing_account(
        self,
        billing_account,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a billing account. This method can only be used to create
        `billing subaccounts <https://cloud.google.com/billing/docs/concepts>`__
        by GCP resellers. When creating a subaccount, the current authenticated
        user must have the ``billing.accounts.update`` IAM permission on the
        master account, which is typically given to billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.
        This method will return an error if the master account has not been
        provisioned as a reseller account.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # TODO: Initialize `billing_account`:
            >>> billing_account = {}
            >>>
            >>> response = client.create_billing_account(billing_account)

        Args:
            billing_account (Union[dict, ~google.cloud.billing_v1.types.BillingAccount]): Required. The billing account resource to create.
                Currently CreateBillingAccount only supports subaccount creation, so
                any created billing accounts must be under a provided master billing
                account.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.billing_v1.types.BillingAccount`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.BillingAccount` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_billing_account" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_billing_account"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_billing_account,
                default_retry=self._method_configs["CreateBillingAccount"].retry,
                default_timeout=self._method_configs["CreateBillingAccount"].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.CreateBillingAccountRequest(
            billing_account=billing_account,
        )
        return self._inner_api_calls["create_billing_account"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_project_billing_info(
        self,
        name,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the projects associated with a billing account. The current
        authenticated user must have the ``billing.resourceAssociations.list``
        IAM permission, which is often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> name = client.billing_account_path('[BILLING_ACCOUNT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_project_billing_info(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_project_billing_info(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): Required. The resource name of the billing account associated with
                the projects that you want to list. For example,
                ``billingAccounts/012345-567890-ABCDEF``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.billing_v1.types.ProjectBillingInfo` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_project_billing_info" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_project_billing_info"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_project_billing_info,
                default_retry=self._method_configs["ListProjectBillingInfo"].retry,
                default_timeout=self._method_configs["ListProjectBillingInfo"].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.ListProjectBillingInfoRequest(
            name=name, page_size=page_size,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_project_billing_info"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="project_billing_info",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_project_billing_info(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the billing information for a project. The current
        authenticated user must have `permission to view the
        project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # TODO: Initialize `name`:
            >>> name = ''
            >>>
            >>> response = client.get_project_billing_info(name)

        Args:
            name (str): Required. The resource name of the project for which billing
                information is retrieved. For example, ``projects/tokyo-rain-123``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.ProjectBillingInfo` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_project_billing_info" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_project_billing_info"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_project_billing_info,
                default_retry=self._method_configs["GetProjectBillingInfo"].retry,
                default_timeout=self._method_configs["GetProjectBillingInfo"].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.GetProjectBillingInfoRequest(name=name,)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_project_billing_info"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_project_billing_info(
        self,
        name,
        project_billing_info=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets or updates the billing account associated with a project. You
        specify the new billing account by setting the ``billing_account_name``
        in the ``ProjectBillingInfo`` resource to the resource name of a billing
        account. Associating a project with an open billing account enables
        billing on the project and allows charges for resource usage. If the
        project already had a billing account, this method changes the billing
        account used for resource usage charges.

        *Note:* Incurred charges that have not yet been reported in the
        transaction history of the GCP Console might be billed to the new
        billing account, even if the charge occurred before the new billing
        account was assigned to the project.

        The current authenticated user must have ownership privileges for both
        the
        `project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__
        and the `billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        You can disable billing on the project by setting the
        ``billing_account_name`` field to empty. This action disassociates the
        current billing account from the project. Any billable activity of your
        in-use services will stop, and your application could stop functioning
        as expected. Any unbilled charges to date will be billed to the
        previously associated account. The current authenticated user must be
        either an owner of the project or an owner of the billing account for
        the project.

        Note that associating a project with a *closed* billing account will
        have much the same effect as disabling billing on the project: any paid
        resources used by the project will be shut down. Thus, unless you wish
        to disable billing, you should always call this method with the name of
        an *open* billing account.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # TODO: Initialize `name`:
            >>> name = ''
            >>>
            >>> response = client.update_project_billing_info(name)

        Args:
            name (str): Required. The resource name of the project associated with the
                billing information that you want to update. For example,
                ``projects/tokyo-rain-123``.
            project_billing_info (Union[dict, ~google.cloud.billing_v1.types.ProjectBillingInfo]): The new billing information for the project. Read-only fields are
                ignored; thus, you can leave empty all fields except
                ``billing_account_name``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.billing_v1.types.ProjectBillingInfo`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.ProjectBillingInfo` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_project_billing_info" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_project_billing_info"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_project_billing_info,
                default_retry=self._method_configs["UpdateProjectBillingInfo"].retry,
                default_timeout=self._method_configs[
                    "UpdateProjectBillingInfo"
                ].timeout,
                client_info=self._client_info,
            )

        request = cloud_billing_pb2.UpdateProjectBillingInfoRequest(
            name=name, project_billing_info=project_billing_info,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_project_billing_info"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for a billing account. The caller
        must have the ``billing.accounts.getIamPolicy`` permission on the
        account, which is often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.billing_v1.types.GetPolicyOptions]): OPTIONAL: A ``GetPolicyOptions`` object for specifying options to
                ``GetIamPolicy``. This field is only used by Cloud IAM.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.billing_v1.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy for a billing account. Replaces any
        existing policy. The caller must have the
        ``billing.accounts.setIamPolicy`` permission on the account, which is
        often given to billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.billing_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.billing_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy,)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Tests the access control policy for a billing account. This method takes
        the resource and a set of permissions as input and returns the subset of
        the input permissions that the caller is allowed for that resource.

        Example:
            >>> from google.cloud import billing_v1
            >>>
            >>> client = billing_v1.CloudBillingClient()
            >>>
            >>> # TODO: Initialize `resource`:
            >>> resource = ''
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions
                with wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.billing_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
