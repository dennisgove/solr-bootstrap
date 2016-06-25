# solr-bootstrap

Solr Bootstrap, sbs, provides a simple to use python script to install, start, and stop Solr clusters with a non-embedded quorum of zookeeper nodes.

## Configuration File

To function, sbs requires a single configuration file providing options about where to get the Solr & Zookeeper packages to use, where to install them, and under which ports instances should be brought up.

```
{
  "rootDirectory":"/Users/dennis/tmp/solr-go",
    # absolute path to where we want to install everything

  "zk": {
    "artifactUrl":"http://apache.claz.org/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz"
      # url where we can find a valid zookeeper build
      # If you have a local copy of the .tar.gz you can provide its location with format
      # file:///path/to/zookeeper-3.4.8.tar.gz",

    "ports": [ 20001, 20002, 20003 ]
      # array of ports we want to bring zookeeper instances up. This controls how many zookeeper processes are 
      # started and made part of the cluster
  },
  "solr": {
    "artifactUrl":"http://apache.claz.org/lucene/solr/6.1.0/solr-6.1.0.tgz",
      # url where we can find a valid solr build. Currently this doesn't support the -src builds
      # If you have a local copy of the .tgz you can provide its location with format
      # file:///path/to/solr-6.1.0.tgz",
    "ports": [ 30001, 30002, 30003 ],
      # array of ports we want to bring solr instances up. This controls how many zookeeper processes are 
      # started and made part of the cluster

    "memory": "2g"
      # Size of JVM to bring each solr instance up with
  }
}
```

Example,
```json
{
  "rootDirectory":"/tmp/solr-go",
  "zk": {
    "artifactUrl":"http://apache.claz.org/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz",
    "ports": [ 20001, 20002, 20003 ]
  },
  "solr": {
    "artifactUrl":"http://apache.claz.org/lucene/solr/6.1.0/solr-6.1.0.tgz",
    "ports": [ 30001, 30002, 30003 ],
    "memory": "2g"
  }
}
```

## Running

At the moment I'm not providing a packaged build of this (in the works) so for now, navigate to the src/main/python and run from there. Every command below has a required final parameter `-cfg [path to config]` so don't forget to include that.

Each command below acts on both solr and zookeeper but it is possible to act on just one or the other. To do so all you need to provide is one additional argument. For example, instead of `python sbs install -cfg /tmp/my.cfg` you'd provide `python sbs solr install -cfg /tmp/my.cfg` and then only solr will be installed or `python sbs zk install -cfg /tmp/my.cfg` and then only zookeeper would be installed. This is useful you want to replace your instance of solr but have no need to mess around with zookeeper. This pattern holds for all commands you see below.

### Installing

```bash
$> python sbs install -cfg test.cfg
Installing Zookeeper to /tmp/solr-go/bin/zookeeper
Downloading http://apache.claz.org/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz...100%
Installing Solr to /tmp/solr-go/bin/solr
Downloading http://apache.claz.org/lucene/solr/6.1.0/solr-6.1.0.tgz...100%
```

### Starting

```bash
$> python sbs start -cfg test.cfg
Starting zookeeper on port 20001
ZooKeeper JMX enabled by default
Using config: /tmp/solr-go/data/zookeeper/instance-20001.cfg
Starting zookeeper ... STARTED
Starting zookeeper on port 20002
ZooKeeper JMX enabled by default
Using config: /tmp/solr-go/data/zookeeper/instance-20002.cfg
Starting zookeeper ... STARTED
Starting zookeeper on port 20003
ZooKeeper JMX enabled by default
Using config: /tmp/solr-go/data/zookeeper/instance-20003.cfg
Starting zookeeper ... STARTED
Starting solr on port 30001
Waiting up to 30 seconds to see Solr running on port 30001 [|]
Started Solr server on port 30001 (pid=22067). Happy searching!

Starting solr on port 30002
Waiting up to 30 seconds to see Solr running on port 30002 [/]
Started Solr server on port 30002 (pid=22165). Happy searching!

Starting solr on port 30003
Waiting up to 30 seconds to see Solr running on port 30003 [/]
Started Solr server on port 30003 (pid=22306). Happy searching!
```

### Checking Status

```bash
$> python sbs status -cfg test.cfg
Zookeeper Status:
  Installed: Yes, at /tmp/solr-go/bin/zookeeper
  Instances:
    Port 20001:
      Data Directory: Yes, at /tmp/solr-go/data/zookeeper/instance-20001
      Log Directory: Yes, at /tmp/solr-go/log/zookeeper/instance-20001
      Configuration File: Yes, at /tmp/solr-go/data/zookeeper/instance-20001.cfg
      Pid File: Yes, at /tmp/solr-go/data/zookeeper/instance-20001/zookeeper_server.pid
      Running: Yes, under pid 22014
    Port 20002:
      Data Directory: Yes, at /tmp/solr-go/data/zookeeper/instance-20002
      Log Directory: Yes, at /tmp/solr-go/log/zookeeper/instance-20002
      Configuration File: Yes, at /tmp/solr-go/data/zookeeper/instance-20002.cfg
      Pid File: Yes, at /tmp/solr-go/data/zookeeper/instance-20002/zookeeper_server.pid
      Running: Yes, under pid 22026
    Port 20003:
      Data Directory: Yes, at /tmp/solr-go/data/zookeeper/instance-20003
      Log Directory: Yes, at /tmp/solr-go/log/zookeeper/instance-20003
      Configuration File: Yes, at /tmp/solr-go/data/zookeeper/instance-20003.cfg
      Pid File: Yes, at /tmp/solr-go/data/zookeeper/instance-20003/zookeeper_server.pid
      Running: Yes, under pid 22038

Solr Status:
  Installed: Yes, at /tmp/solr-go/bin/solr
  Instances:
    Port 30001:
      Data Directory: Yes, at /tmp/solr-go/data/solr/instance-30001
      Log Directory: Yes, at /tmp/solr-go/log/solr/instance-30001
      Configuration File: Yes, at /tmp/solr-go/data/solr/instance-30001/home/solr.xml
      Pid File: Yes, at /tmp/solr-go/bin/solr/bin/solr-30001.pid
      Running: Yes, under pid 22067
    Port 30002:
      Data Directory: Yes, at /tmp/solr-go/data/solr/instance-30002
      Log Directory: Yes, at /tmp/solr-go/log/solr/instance-30002
      Configuration File: Yes, at /tmp/solr-go/data/solr/instance-30002/home/solr.xml
      Pid File: Yes, at /tmp/solr-go/bin/solr/bin/solr-30002.pid
      Running: Yes, under pid 22165
    Port 30003:
      Data Directory: Yes, at /tmp/solr-go/data/solr/instance-30003
      Log Directory: Yes, at /tmp/solr-go/log/solr/instance-30003
      Configuration File: Yes, at /tmp/solr-go/data/solr/instance-30003/home/solr.xml
      Pid File: Yes, at /tmp/solr-go/bin/solr/bin/solr-30003.pid
      Running: Yes, under pid 22306
```

### Stopping

```bash
$> python sbs stop -cfg test.cfg
Stopping solr on port 30001
Sending stop command to Solr running on port 30001 ... waiting 5 seconds to allow Jetty process 22067 to stop gracefully.
Stopping solr on port 30002
Sending stop command to Solr running on port 30002 ... waiting 5 seconds to allow Jetty process 22165 to stop gracefully.
Stopping solr on port 30003
Sending stop command to Solr running on port 30003 ... waiting 5 seconds to allow Jetty process 22306 to stop gracefully.
Stopping zookeeper on port 20001
ZooKeeper JMX enabled by default
Using config: /tmp/solr-go/data/zookeeper/instance-20001.cfg
Stopping zookeeper ... STOPPED
Stopping zookeeper on port 20002
ZooKeeper JMX enabled by default
Using config: /tmp/solr-go/data/zookeeper/instance-20002.cfg
Stopping zookeeper ... STOPPED
Stopping zookeeper on port 20003
ZooKeeper JMX enabled by default
Using config: /tmp/solr-go/data/zookeeper/instance-20003.cfg
Stopping zookeeper ... STOPPED
```

### Uninstall

This just uninstalls the solr and zookeeper binaries but does not touch the data directories.

```bash
$> python sbs uninstall -cfg test.cfg
Removing Zookeeper from /tmp/solr-go/bin/zookeeper
Removing Solr from /tmp/solr-go/bin/solr
```
