# Copyright 2016 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import jenkins
import logging
import re

from jcli import exception
from server import Server

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class View(Server):
    """Manages view command execution"""

    def __init__(self, url, user, password, view_args=None, action=None):
        super(View, self).__init__(url, user, password)
        self.action = action
        self.view_args = view_args

    def get_views_names(self):
        """Returns list of all views name"""

        views_names = []

        views = self.server.get_views()
        if self.view_args.name:
            for view_object in views:
                if self.view_args.name in view_object['name']:
                    views_names.append(view_object['name'])
        else:
            for view_object in views:
                views_names.append(view_object['name'])

        return views_names

    def delete_view(self):
        """Removes view from the server"""

        if self.view_args.name:
            try:
                self.server.delete_view(self.view_args.name)
            except Exception:
                raise exception.JcliException(
                    "No such view: {}".format(self.view_args.name))
            logger.info("Removed view: %s", self.view_args.name)
        else:
            logger.info("No name provided. Exiting...")

    def list_jobs(self):
        """Print list of all the jobs in the view"""

        jobs = self.server.get_jobs(view_name=self.view_args.name)

        if jobs:
            logger.info("The jobs under %s:\n", self.view_args.name)
            for job in jobs:
                logger.info(job['fullname'])
        else:
            logger.info(
                "No jobs directly under %s\n", self.view_args.name)

    def create_view(self):
        """Creates new empty view"""

        try:
            self.server.create_view(
                self.view_args.name, jenkins.EMPTY_VIEW_CONFIG_XML)
            logger.info("Created new view: %s", self.view_args.name)
        except Exception as e:
            raise exception.JcliException(e)

    def rename_view(self):
        """Rename the specific view. """

        view_config = self.server.get_view_config(self.view_args.name)
        new_config = re.sub(r"<name>.*</name>",
                            "<name>%s</name>" % self.view_args.new_name,
                            view_config)
        try:
            self.server.reconfig_view(self.view_args.name, new_config)
            logger.info("Renamed. The new name: %s", self.view_args.new_name)

        except Exception as e:
            raise exception.JcliException(e)

    def run(self):
        """Executes chosen action."""

        if self.action == 'list':
            for view in self.get_views_names():
                logger.info(view)

        if self.action == 'delete':
            self.delete_view()

        if self.action == 'jobs':
            self.list_jobs()

        if self.action == 'create':
            self.create_view()

        if self.action == 'rename':
            self.rename_view()

        if self.action == 'config':
            self.get_config()
