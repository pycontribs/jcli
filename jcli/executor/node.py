#!/usr/bin/env python
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
import logging

from jcli import errors
from server import Server

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class Node(Server):
    """Manages node command execution"""

    def __init__(self, action, url, user, password, node_args):
        super(Node, self).__init__(url, user, password)
        self.action = action
        self.node_args = node_args

    def get_nodes_names(self):
        """Returns list of all nodes name"""

        nodes_names = []

        nodes = self.server.get_nodes()
        if self.node_args.name:
            for node_object in nodes:
                if self.node_args.name in node_object['name']:
                    nodes_names.append(node_object['name'])
        else:
            for node_object in nodes:
                nodes_names.append(node_object['name'])

        return nodes_names

    def delete_node(self):
        """Removes node from the server"""

        if self.node_args.name:
            try:
                self.server.delete_node(self.node_args.name)
            except Exception:
                raise errors.JcliException(
                    "No such node: {}".format(self.node_args.name))
            logger.info("Removed node: %s", self.node_args.name)
        else:
            logger.info("No name provided. Exiting...")

    def create_node(self):
        """Creates node."""

        name = self.node_args.name

        if self.server.node_exists(name):
            raise errors.JcliException(
                "There is already node with this name: %s", name)

        try:
            self.server.create_node(name, self.node_args.executors,
                                    self.node_args.description,
                                    self.node_args.remotefs,
                                    self.node_args.labels,
                                    self.node_args.exclusive)
            logger.info("Node created: %s", name)

        except Exception:
            raise errors.JcliException("Couldn't create node: %s",
                                       Exception.message)

    def node_info(self):
        """Print information on a specific plugin."""

        if not self.server.node_exists(self.node_args.name):
            raise errors.JcliException(
                "There is node with such name: %s", self.node_args.name)
        try:
            node_json = self.server.get_node_info(
                self.node_args.name)

            logger.info("Name: %s", self.node_args.name)
            logger.info("Idle? %s", node_json['idle'])
            logger.info("Number of executors: %s", node_json['numExecutors'])
            logger.info("Offline? %s", node_json['offline'])
            if node_json['offline'] and node_json['offlineCauseReason']:
                logger.info("Cause: %s", node_json['offlineCauseReason'])

        except Exception as e:
            raise errors.JcliException(e)

    def run(self):
        """Executes chosen action."""

        if self.action == 'list':
            for node in self.get_nodes_names():
                logger.info(node)

        if self.action == 'delete':
            self.delete_node()

        if self.action == 'create':
            self.create_node()

        if self.action == 'info':
            self.node_info()
