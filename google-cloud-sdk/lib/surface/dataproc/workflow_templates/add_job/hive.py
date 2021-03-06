# -*- coding: utf-8 -*- #
# Copyright 2015 Google Inc. All Rights Reserved.
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
"""Add a Hive job to the workflow template."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.dataproc import dataproc as dp
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.dataproc import workflow_templates
from googlecloudsdk.command_lib.dataproc.jobs import hive


class Hive(hive.HiveBase, base.Command):
  """Add a Hive job to the workflow template."""

  @staticmethod
  def Args(parser):
    hive.HiveBase.Args(parser)
    workflow_templates.AddWorkflowTemplatesArgs(parser)

  def ConfigureJob(self, messages, job, files_by_type, args):
    hive.HiveBase.ConfigureJob(messages, job, files_by_type, args)
    workflow_templates.ConfigureOrderedJob(messages, job, args)

  def Run(self, args):
    self.PopulateFilesByType(args)
    dataproc = dp.Dataproc(self.ReleaseTrack())
    ordered_job = workflow_templates.CreateWorkflowTemplateOrderedJob(
        args, dataproc)
    self.ConfigureJob(dataproc.messages, ordered_job, self.files_by_type, args)
    return workflow_templates.AddJobToWorkflowTemplate(args, dataproc,
                                                       ordered_job)
