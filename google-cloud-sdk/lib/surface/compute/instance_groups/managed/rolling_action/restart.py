# -*- coding: utf-8 -*- #
# Copyright 2017 Google Inc. All Rights Reserved.
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
"""Command for restarting instances of managed instance group."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.instance_groups import flags as instance_groups_flags
from googlecloudsdk.command_lib.compute.instance_groups.managed import flags as instance_groups_managed_flags
from googlecloudsdk.command_lib.compute.instance_groups.managed import rolling_action


def _AddArgs(parser, supports_min_ready=False):
  """Adds args."""
  instance_groups_managed_flags.AddMaxUnavailableArg(parser)
  if supports_min_ready:
    instance_groups_managed_flags.AddMinReadyArg(parser)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class StartUpdate(base.Command):
  """Start restart instances of managed instance group."""

  @staticmethod
  def Args(parser):
    _AddArgs(parser)
    instance_groups_flags.MULTISCOPE_INSTANCE_GROUP_MANAGER_ARG.AddArgument(
        parser)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client
    resources = holder.resources

    minimal_action = (client.messages.InstanceGroupManagerUpdatePolicy.
                      MinimalActionValueValuesEnum.RESTART)
    return client.MakeRequests([
        rolling_action.CreateRequest(args, client, resources, minimal_action)
    ])


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class StartUpdateAlphaBeta(StartUpdate):
  """Start restart instances of managed instance group."""

  @staticmethod
  def Args(parser):
    _AddArgs(parser, supports_min_ready=True)
    instance_groups_flags.MULTISCOPE_INSTANCE_GROUP_MANAGER_ARG.AddArgument(
        parser)


StartUpdate.detailed_help = {
    'brief':
        'Restarts instances in a managed instance group',
    'DESCRIPTION':
        """\
        *{command}* restarts instances in a managed instance group, effectively
        performing a stop and start request. Note, if your request
        requires that the instance be replaced to pick up changes, a forced
        `replace` will be performed instead."""
}
