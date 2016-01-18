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


class Arg(object):
    def __init__(self, name, shortcut=None, metavar=None, action=None):
        self.name = name
        self.shortcut = shortcut
        self.metavar = metavar
        self.action = action


class Action(object):
    def __init__(self, name, optional_args=None, help=None):
        self.name = name
        self.optional_args = optional_args
        self.help = help
