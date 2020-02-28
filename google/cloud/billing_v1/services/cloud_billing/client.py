# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from collections import OrderedDict
from typing import Dict, Iterable, Iterator, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.billing_v1.services.cloud_billing import pagers
from google.cloud.billing_v1.types import cloud_billing
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore

from .transports.base import CloudBillingTransport
from .transports.grpc import CloudBillingGrpcTransport


class CloudBillingClientMeta(type):
    """Metaclass for the CloudBilling client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[CloudBillingTransport]]
    _transport_registry["grpc"] = CloudBillingGrpcTransport

    def get_transport_class(cls, label: str = None) -> Type[CloudBillingTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class CloudBillingClient(metaclass=CloudBillingClientMeta):
    """Retrieves GCP Console billing accounts and associates them
    with projects.
    """

    DEFAULT_OPTIONS = ClientOptions.ClientOptions(
        api_endpoint="cloudbilling.googleapis.com"
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, CloudBillingTransport] = None,
        client_options: ClientOptions = DEFAULT_OPTIONS,
    ) -> None:
        """Instantiate the cloud billing client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudBillingTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, CloudBillingTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                host=client_options.api_endpoint or "cloudbilling.googleapis.com",
            )

    def get_billing_account(
        self,
        request: cloud_billing.GetBillingAccountRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.BillingAccount:
        r"""Gets information about a billing account. The current
        authenticated user must be a `viewer of the billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`~.cloud_billing.GetBillingAccountRequest`):
                The request object. Request message for
                `GetBillingAccount`.
            name (:class:`str`):
                Required. The resource name of the billing account to
                retrieve. For example,
                ``billingAccounts/012345-567890-ABCDEF``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_billing.BillingAccount:
                A billing account in `GCP
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.GetBillingAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_billing_account,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_billing_accounts(
        self,
        request: cloud_billing.ListBillingAccountsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBillingAccountsPager:
        r"""Lists the billing accounts that the current authenticated user
        has permission to
        `view <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`~.cloud_billing.ListBillingAccountsRequest`):
                The request object. Request message for
                `ListBillingAccounts`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListBillingAccountsPager:
                Response message for ``ListBillingAccounts``.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.

        request = cloud_billing.ListBillingAccountsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_billing_accounts,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBillingAccountsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def update_billing_account(
        self,
        request: cloud_billing.UpdateBillingAccountRequest = None,
        *,
        name: str = None,
        account: cloud_billing.BillingAccount = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.BillingAccount:
        r"""Updates a billing account's fields. Currently the only field
        that can be edited is ``display_name``. The current
        authenticated user must have the ``billing.accounts.update`` IAM
        permission, which is typically given to the
        `administrator <https://cloud.google.com/billing/docs/how-to/billing-access>`__
        of the billing account.

        Args:
            request (:class:`~.cloud_billing.UpdateBillingAccountRequest`):
                The request object. Request message for
                `UpdateBillingAccount`.
            name (:class:`str`):
                Required. The name of the billing
                account resource to be updated.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            account (:class:`~.cloud_billing.BillingAccount`):
                Required. The billing account
                resource to replace the resource on the
                server.
                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_billing.BillingAccount:
                A billing account in `GCP
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, account]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.UpdateBillingAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if account is not None:
            request.account = account

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_billing_account,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def create_billing_account(
        self,
        request: cloud_billing.CreateBillingAccountRequest = None,
        *,
        billing_account: cloud_billing.BillingAccount = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.BillingAccount:
        r"""Creates a billing account. This method can only be used to
        create `billing
        subaccounts <https://cloud.google.com/billing/docs/concepts>`__
        by GCP resellers. When creating a subaccount, the current
        authenticated user must have the ``billing.accounts.update`` IAM
        permission on the master account, which is typically given to
        billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.
        This method will return an error if the master account has not
        been provisioned as a reseller account.

        Args:
            request (:class:`~.cloud_billing.CreateBillingAccountRequest`):
                The request object. Request message for
                `CreateBillingAccount`.
            billing_account (:class:`~.cloud_billing.BillingAccount`):
                Required. The billing account
                resource to create. Currently
                CreateBillingAccount only supports
                subaccount creation, so any created
                billing accounts must be under a
                provided master billing account.
                This corresponds to the ``billing_account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_billing.BillingAccount:
                A billing account in `GCP
                Console <https://console.cloud.google.com/>`__. You can
                assign a billing account to one or more projects.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([billing_account]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.CreateBillingAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if billing_account is not None:
            request.billing_account = billing_account

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_billing_account,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_project_billing_info(
        self,
        request: cloud_billing.ListProjectBillingInfoRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProjectBillingInfoPager:
        r"""Lists the projects associated with a billing account. The
        current authenticated user must have the
        ``billing.resourceAssociations.list`` IAM permission, which is
        often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`~.cloud_billing.ListProjectBillingInfoRequest`):
                The request object. Request message for
                `ListProjectBillingInfo`.
            name (:class:`str`):
                Required. The resource name of the billing account
                associated with the projects that you want to list. For
                example, ``billingAccounts/012345-567890-ABCDEF``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListProjectBillingInfoPager:
                Request message for ``ListProjectBillingInfoResponse``.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.ListProjectBillingInfoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_project_billing_info,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListProjectBillingInfoPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_project_billing_info(
        self,
        request: cloud_billing.GetProjectBillingInfoRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.ProjectBillingInfo:
        r"""Gets the billing information for a project. The current
        authenticated user must have `permission to view the
        project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__.

        Args:
            request (:class:`~.cloud_billing.GetProjectBillingInfoRequest`):
                The request object. Request message for
                `GetProjectBillingInfo`.
            name (:class:`str`):
                Required. The resource name of the project for which
                billing information is retrieved. For example,
                ``projects/tokyo-rain-123``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_billing.ProjectBillingInfo:
                Encapsulation of billing information
                for a GCP Console project. A project has
                at most one associated billing account
                at a time (but a billing account can be
                assigned to multiple projects).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.GetProjectBillingInfoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_project_billing_info,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_project_billing_info(
        self,
        request: cloud_billing.UpdateProjectBillingInfoRequest = None,
        *,
        name: str = None,
        project_billing_info: cloud_billing.ProjectBillingInfo = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_billing.ProjectBillingInfo:
        r"""Sets or updates the billing account associated with a project.
        You specify the new billing account by setting the
        ``billing_account_name`` in the ``ProjectBillingInfo`` resource
        to the resource name of a billing account. Associating a project
        with an open billing account enables billing on the project and
        allows charges for resource usage. If the project already had a
        billing account, this method changes the billing account used
        for resource usage charges.

        *Note:* Incurred charges that have not yet been reported in the
        transaction history of the GCP Console might be billed to the
        new billing account, even if the charge occurred before the new
        billing account was assigned to the project.

        The current authenticated user must have ownership privileges
        for both the
        `project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__
        and the `billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        You can disable billing on the project by setting the
        ``billing_account_name`` field to empty. This action
        disassociates the current billing account from the project. Any
        billable activity of your in-use services will stop, and your
        application could stop functioning as expected. Any unbilled
        charges to date will be billed to the previously associated
        account. The current authenticated user must be either an owner
        of the project or an owner of the billing account for the
        project.

        Note that associating a project with a *closed* billing account
        will have much the same effect as disabling billing on the
        project: any paid resources used by the project will be shut
        down. Thus, unless you wish to disable billing, you should
        always call this method with the name of an *open* billing
        account.

        Args:
            request (:class:`~.cloud_billing.UpdateProjectBillingInfoRequest`):
                The request object. Request message for
                `UpdateProjectBillingInfo`.
            name (:class:`str`):
                Required. The resource name of the project associated
                with the billing information that you want to update.
                For example, ``projects/tokyo-rain-123``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            project_billing_info (:class:`~.cloud_billing.ProjectBillingInfo`):
                The new billing information for the project. Read-only
                fields are ignored; thus, you can leave empty all fields
                except ``billing_account_name``.
                This corresponds to the ``project_billing_info`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cloud_billing.ProjectBillingInfo:
                Encapsulation of billing information
                for a GCP Console project. A project has
                at most one associated billing account
                at a time (but a billing account can be
                assigned to multiple projects).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, project_billing_info]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_billing.UpdateProjectBillingInfoRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if project_billing_info is not None:
            request.project_billing_info = project_billing_info

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_project_billing_info,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: iam_policy.GetIamPolicyRequest = None,
        *,
        resource: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
        r"""Gets the access control policy for a billing account. The caller
        must have the ``billing.accounts.getIamPolicy`` permission on
        the account, which is often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`~.iam_policy.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the policy is being
                requested. ``resource`` is usually specified as a path.
                For example, a Project resource is specified as
                ``projects/{project}``.
                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.policy.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.

                A ``Policy`` consists of a list of ``bindings``. A
                ``Binding`` binds a list of ``members`` to a ``role``,
                where the members can be user accounts, Google groups,
                Google domains, and service accounts. A ``role`` is a
                named list of permissions defined by IAM.

                **Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/owner",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-other-app@appspot.gserviceaccount.com",
                          ]
                        },
                        {
                          "role": "roles/viewer",
                          "members": ["user:sean@example.com"]
                        }
                      ]
                    }

                For a description of IAM and its features, see the `IAM
                developer's guide <https://cloud.google.com/iam>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([resource]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.GetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy.GetIamPolicyRequest()

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_iam_policy,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: iam_policy.SetIamPolicyRequest = None,
        *,
        resource: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
        r"""Sets the access control policy for a billing account. Replaces
        any existing policy. The caller must have the
        ``billing.accounts.setIamPolicy`` permission on the account,
        which is often given to billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Args:
            request (:class:`~.iam_policy.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the policy is being
                specified. ``resource`` is usually specified as a path.
                For example, a Project resource is specified as
                ``projects/{project}``.
                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.policy.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.

                A ``Policy`` consists of a list of ``bindings``. A
                ``Binding`` binds a list of ``members`` to a ``role``,
                where the members can be user accounts, Google groups,
                Google domains, and service accounts. A ``role`` is a
                named list of permissions defined by IAM.

                **Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/owner",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-other-app@appspot.gserviceaccount.com",
                          ]
                        },
                        {
                          "role": "roles/viewer",
                          "members": ["user:sean@example.com"]
                        }
                      ]
                    }

                For a description of IAM and its features, see the `IAM
                developer's guide <https://cloud.google.com/iam>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([resource]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.SetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy.SetIamPolicyRequest()

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_iam_policy,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: iam_policy.TestIamPermissionsRequest = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy.TestIamPermissionsResponse:
        r"""Tests the access control policy for a billing
        account. This method takes the resource and a set of
        permissions as input and returns the subset of the input
        permissions that the caller is allowed for that
        resource.

        Args:
            request (:class:`~.iam_policy.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the policy detail is
                being requested. ``resource`` is usually specified as a
                path. For example, a Project resource is specified as
                ``projects/{project}``.
                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (:class:`Sequence[str]`):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.iam_policy.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([resource, permissions]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.TestIamPermissionsRequest(**request)
        elif not request:
            request = iam_policy.TestIamPermissionsRequest()

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if resource is not None:
            request.resource = resource

        if permissions:
            request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.test_iam_permissions,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-billing").version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudBillingClient",)
