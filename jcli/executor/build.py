# Copyright 2017 Arie Bregman
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
import jenkins

from jcli import exception
from jcli.executor.server import Server

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class Build(Server):
    """Manages build commands execution"""

    def __init__(self, url, user, password, build_args=None, action=None):
        super(Build, self).__init__(url, user, password)
        self.action = action
        self.build_args = build_args

    def stop_build(self):
        """Stops running build."""
        try:
            if not self.build_args.build_number:
                build_number = int(self.server.get_job_info(
                    self.build_args.job_name[0])['lastBuild']['number'])
            else:
                build_number = self.build_args.build_number

            self.server.stop_build(self.build_args.job_name[0], build_number)
            logger.info(
                "Stopped build {} for {}".format(build_number,
                                                 self.build_args.job_name[0]))

        except jenkins.NotFoundException as e:
            raise exception.JcliJobNotFound(self.build_args.job_name[0])
        except Exception as e:
            raise exception.JcliException(e)

    def run(self):
        """Executes chosen action."""

        if self.action == 'stop' or self.action == 'abandon':
            self.stop_build()
