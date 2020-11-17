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


import google.api_core.grpc_helpers

from google.cloud.billing_v1.proto import cloud_billing_pb2_grpc


class CloudBillingGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.billing.v1 CloudBilling API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="cloudbilling.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive.",
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "cloud_billing_stub": cloud_billing_pb2_grpc.CloudBillingStub(channel),
        }

    @classmethod
    def create_channel(
        cls, address="cloudbilling.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def get_billing_account(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.get_billing_account`.

        Gets information about a billing account. The current authenticated
        user must be a `viewer of the billing
        account <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].GetBillingAccount

    @property
    def list_billing_accounts(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.list_billing_accounts`.

        Lists the billing accounts that the current authenticated user has
        permission to
        `view <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].ListBillingAccounts

    @property
    def update_billing_account(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.update_billing_account`.

        Updates a billing account's fields. Currently the only field that
        can be edited is ``display_name``. The current authenticated user must
        have the ``billing.accounts.update`` IAM permission, which is typically
        given to the
        `administrator <https://cloud.google.com/billing/docs/how-to/billing-access>`__
        of the billing account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].UpdateBillingAccount

    @property
    def create_billing_account(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.create_billing_account`.

        Creates a billing account. This method can only be used to create
        `billing subaccounts <https://cloud.google.com/billing/docs/concepts>`__
        by GCP resellers. When creating a subaccount, the current authenticated
        user must have the ``billing.accounts.update`` IAM permission on the
        master account, which is typically given to billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.
        This method will return an error if the master account has not been
        provisioned as a reseller account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].CreateBillingAccount

    @property
    def list_project_billing_info(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.list_project_billing_info`.

        Lists the projects associated with a billing account. The current
        authenticated user must have the ``billing.resourceAssociations.list``
        IAM permission, which is often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].ListProjectBillingInfo

    @property
    def get_project_billing_info(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.get_project_billing_info`.

        Gets the billing information for a project. The current
        authenticated user must have `permission to view the
        project <https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].GetProjectBillingInfo

    @property
    def update_project_billing_info(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.update_project_billing_info`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].UpdateProjectBillingInfo

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.get_iam_policy`.

        Gets the access control policy for a billing account. The caller
        must have the ``billing.accounts.getIamPolicy`` permission on the
        account, which is often given to billing account
        `viewers <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].GetIamPolicy

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.set_iam_policy`.

        Sets the access control policy for a billing account. Replaces any
        existing policy. The caller must have the
        ``billing.accounts.setIamPolicy`` permission on the account, which is
        often given to billing account
        `administrators <https://cloud.google.com/billing/docs/how-to/billing-access>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].SetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`CloudBillingClient.test_iam_permissions`.

        Tests the access control policy for a billing account. This method takes
        the resource and a set of permissions as input and returns the subset of
        the input permissions that the caller is allowed for that resource.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_billing_stub"].TestIamPermissions
