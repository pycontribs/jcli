Node command examples
====================

### Full list of all the available node commands

List all nodes:

    jcli node list

Delete node:

    jcli node delete <node_name>

Create node:

    jcli node create my_node --description "my cool node" --labels "mario" --executors 2

Print information on node:

    jcli node info my_node
