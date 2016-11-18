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
import fixtures
import os
import testtools

_TRUE_VALUES = ('true', '1', 'yes')


class TestCase(testtools.TestCase):
    """Test case base class for all tests."""

    TIMEOUT_SCALING_FACTOR = 1.0
    BASE_URL = "http://example.com/jenkins"

    def setUp(self):
        """Run before each test method to initialize test environment."""

        super(TestCase, self).setUp()
        
        # Timeout
        test_timeout = int(os.environ.get('OS_TEST_TIMEOUT', 0))
        try:
            test_timeout = int(test_timeout * self.TIMEOUT_SCALING_FACTOR)
        except ValueError:
            # If timeout value is invalid do not set a timeout.
            test_timeout = 0
        if test_timeout > 0:
            # gentle timeout = raise TimeoutException
            self.useFixture(fixtures.Timeout(test_timeout, gentle=True))

        # Nest all temporary files and directories inside another directory
        self.useFixture(fixtures.NestedTempfile())

        # Create a temporary directory and set it as $HOME
        self.useFixture(fixtures.TempHomeDir())

        # Capture STDOUT
        if os.environ.get('OS_STDOUT_CAPTURE') in _TRUE_VALUES:
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))

        # Capture STDERR
        if os.environ.get('OS_STDERR_CAPTURE') in _TRUE_VALUES:
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))
