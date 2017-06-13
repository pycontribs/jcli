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

import ConfigParser
import io
import logging
import os

from errors import JcliException

DEFAULT_CONF_FILES = [
    '~/.config/jcli/jcli.ini',
    '~/jcli.ini',
    '/etc/jcli/config.ini',
    '~/.config/jenkins_jobs/jenkins_jobs.ini',  # reuse jjb config if found
]


def read(conf_file):
    """Returns config parser object.

    :param conf_file: the config file.
    """

    cwd_conf_file = os.path.join(os.getcwd(), 'config.ini')

    if os.path.isfile(cwd_conf_file):
        config_file = cwd_conf_file
    elif conf_file:
        config_file = conf_file
    else:
        for f in DEFAULT_CONF_FILES:
            if os.path.isfile(os.path.expanduser(f)):
                config_file = os.path.expanduser(f)
                break
    config = ConfigParser.ConfigParser()

    # Reading the config file
    try:
        logging.debug("Reading configuration from: {}".format(config_file))
        config_data = io.open(config_file, 'r', encoding='utf-8')
        config.readfp(config_data)
    except Exception:
        raise JcliException(
            "A valid configuration file is required."
            "\n{0} is not a valid configuration file".format(config_file))

    return config


def get_value(config, section, option):
    """Get the value of specific option in given section.

    :param config: the configuration object.
    :param section: the name of the section.
    :param option: the name of the option.
    """

    value = config.get(section, option)

    return value
