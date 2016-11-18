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
import mock

from jcli.executor.job import Job
from jcli.tests.unit import base


class TestJob(base.BaseTestCase):

    def setUp(self):
        super(TestJob, self).setUp()

    @mock.patch.object(Job, 'get_jobs_names')
    def test_get_all_jobs(self, mock_get_jobs):

        job_executor = Job(self.url, self.user, self.password, action='list')
        job_executor.run()

        mock_get_jobs.assert_called()
