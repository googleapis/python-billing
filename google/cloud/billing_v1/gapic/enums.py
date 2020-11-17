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

"""Wrappers for protocol buffer enum types."""

import enum


class AggregationInfo(object):
    class AggregationInterval(enum.IntEnum):
        """
        The interval at which usage is aggregated to compute cost.
        Example: "MONTHLY" aggregation interval indicates that usage for tiered
        pricing is aggregated every month.

        Attributes:
          AGGREGATION_INTERVAL_UNSPECIFIED (int)
          DAILY (int)
          MONTHLY (int)
        """

        AGGREGATION_INTERVAL_UNSPECIFIED = 0
        DAILY = 1
        MONTHLY = 2

    class AggregationLevel(enum.IntEnum):
        """
        The level at which usage is aggregated to compute cost.
        Example: "ACCOUNT" aggregation level indicates that usage for tiered
        pricing is aggregated across all projects in a single account.

        Attributes:
          AGGREGATION_LEVEL_UNSPECIFIED (int)
          ACCOUNT (int)
          PROJECT (int)
        """

        AGGREGATION_LEVEL_UNSPECIFIED = 0
        ACCOUNT = 1
        PROJECT = 2
