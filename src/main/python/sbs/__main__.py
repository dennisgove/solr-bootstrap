
import sys
import argparse
import os
from filemanager import FileManager
from zookeepermanager import ZookeeperManager
from solrmanager import SolrManager

def loadConfigFile(path):
  try:
    config = FileManager.loadAsJson(path)
    return config
  except ValueError as e:
    print "Invalid or non-existant config file at %s - %s" % (path, e.message) 
    return None

def validateConfig(config):
  errors = []

  if "rootDirectory" not in config:
    errors.append("Didn't find 'rootDirectory' value")

  if "zk" not in config:
    errors.append("Didn't find 'zk' object")
  else:
    if "artifactUrl" not in config["zk"]:
      errors.append("Didn't find 'artifactUrl' value under zk node")

    if "ports" not in config["zk"] or not isinstance(config["zk"]["ports"], list) or 0 == len(config["zk"]["ports"]):
      errors.append("Didn't find 'ports' array under zk node")

  if "solr" not in config:
    errors.append("Didn't find 'solr' object")
  else:
    if "artifactUrl" not in config["solr"]:
      errors.append("Didn't find 'artifactUrl' value under solr node")

    if "ports" not in config["solr"] or not isinstance(config["solr"]["ports"], list) or 0 == len(config["solr"]["ports"]):
      errors.append("Didn't find 'ports' array under solr node")

    if "memory" not in config["solr"]:
      errors.append("Didn't find 'memory' value under solr node")

  return errors

def buildConfig(args):

  # load config file if arg provided
  config = loadConfigFile(os.path.abspath(args.configFilePath)) if args.configFilePath else {}

  if None != config:
    errors = validateConfig(config)
    if 0 != len(errors):
      print "Invalid config:\n  %s" % ("\n  ".join(errors))
      return None

  return config

  # Expecting json of format
  # {
  #   "rootDirectory":"/Users/dennis/tmp/solr-go",
  #   "zk": {
  #     "artifactUrl":"file:///Users/dennis/tmp/zookeeper-3.4.8.tar.gz",
  #     "ports": [ 20001, 20002, 20003 ],
  #   },
  #   "solr": {
  #     "artifactUrl":"file:///Users/dennis/tmp/solr-6.1.0.tgz",
  #     "ports": [ 30001, 30002, 30003 ],
  #     "memory": "2g"
  #   }
  # }

def handleZookeeper(args, config):
  manager = ZookeeperManager(config)

  if 'install' == args.subcommand:
    manager.uninstall()
    if manager.install():
      print "Zookeeper Installed"

  elif 'uninstall' == args.subcommand:
    if manager.uninstall():
      print "Zookeeper uninstalled"

  elif 'start' == args.subcommand:
    if manager.start():
      print "Zookeeper started"

  elif 'stop' == args.subcommand:
    if manager.stop():
      print "Zookeeper stopped"

  elif 'status' == args.subcommand:
    manager.status()

def handleSolr(args, config):
  manager = SolrManager(config)

  if 'install' == args.subcommand:
    manager.uninstall()
    if manager.install():
      print "Solr Installed"

  elif 'uninstall' == args.subcommand:
    if manager.uninstall():
      print "Solr uninstalled"

  elif 'start' == args.subcommand:
    if manager.start():
      print "Solr started"

  elif 'stop' == args.subcommand:
    if manager.stop():
      print "Solr stopped"

  elif 'status' == args.subcommand:
    manager.status()

def handleBoth(args, config, command):
  zkManager = ZookeeperManager(config)
  solrManager = SolrManager(config)

  if 'install' == command:
    zkManager.install()
    solrManager.install()
  elif 'uninstall' == command:
    zkManager.uninstall()
    solrManager.uninstall()
  elif 'start' == command:
    zkManager.start()
    solrManager.start()
  elif 'stop' == command:
    solrManager.stop()
    zkManager.stop()
  elif 'status' == command:
    zkManager.status()
    print
    solrManager.status()
      

def doit(args):

  config = buildConfig(args)
  if None == config:
    os._exit(-1)

  if 'zk' == args.command:
    handleZookeeper(args, config)
  elif 'solr' == args.command:
    handleSolr(args, config)
  else:
    handleBoth(args, config, args.command)


def run():

  parser = argparse.ArgumentParser(description='Solr Bootstrapping')
  subParsers = parser.add_subparsers()

  globalParser = argparse.ArgumentParser(add_help=False)
  globalParser.add_argument('-cfg', '--config', dest='configFilePath')

  zkParser = subParsers.add_parser('zk', parents=[globalParser])
  zkParser.set_defaults(command='zk')
  zkParser.add_argument('subcommand', choices=['install','uninstall','start','stop','status'])

  solrParser = subParsers.add_parser('solr', parents=[globalParser])
  solrParser.set_defaults(command='solr')
  solrParser.add_argument('subcommand', choices=['install','uninstall','start','stop','status'])

  installParser = subParsers.add_parser('install', parents=[globalParser])
  installParser.set_defaults(command='install')

  uninstallParser = subParsers.add_parser('uninstall', parents=[globalParser])
  uninstallParser.set_defaults(command='uninstall')

  startParser = subParsers.add_parser('start', parents=[globalParser])
  startParser.set_defaults(command='start')

  stopParser = subParsers.add_parser('stop', parents=[globalParser])
  stopParser.set_defaults(command='stop')

  statusParser = subParsers.add_parser('status', parents=[globalParser])
  statusParser.set_defaults(command='status')
  
  doit(parser.parse_args())

if __name__ == "__main__":
  run()
