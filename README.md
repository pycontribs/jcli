Jcli - Jenkins Command-line Interface
=====================================

The ultimate Jenkins CLI ;)

Install
-------

A virtual environment is recommended for development. To install `jcli` on your
system, run the following commands:

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt -e .

Setup config
------------

`jcli` is using configuration file to connect the server.

It can be setup in one of the following paths, in that order:

    ~/.config/jcli/jcli.ini
    ~/jcli/jcli.ini
    /etc/jcli/config.ini
    `pwd`/config.ini

or filename can be passed as an argument.

Minimal configuration is:

    [jenkins]
    user=<jenkins_user>
    password=<api_token>
    url=<jenkins_url>

Examples
--------

### Job examples

Print list of all the jobs:

    jcli job list

Print jobs which contain the string 'coreci' in their names:

    jcli job list coreci

Print the number of jobs on Jenkins server:

    jcli job count


Full list of job commands can be found [here](https://github.com/bregman-arie/jcli/tree/master/doc/job.md)

### View examples

List all views:

    jcli view list

Delete view:

    jcli view delete view90


Full list of view commands can be found [here](https://github.com/bregman-arie/jcli/tree/master/doc/view.md)

### Node examples

List all nodes:

    jcli node list

Delete node:

    jcli node delete <node_name>

### Plugin examples

List all installed plugins:

    jcli plugin list

List infromation on specific plugin:

    jcli plugin info my_plugin


Full list of plugin commands can be found [here](https://github.com/bregman-arie/jcli/tree/master/doc/plugin.md)


License
-------

Apache

Author Information
------------------

Arie Bregman - abregman@redhat.com
