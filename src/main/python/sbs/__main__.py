
import argparse
from filemanager import FileManager
from zookeepermanager import ZookeeperManager
from solrmanager import SolrManager

def buildConfig(args):

  # load config file if arg provided
  # config = loadConfigFile(args.configFilePath) if args.configFilePath else {}

  return {

    "rootDirectory":"/Users/dennis/tmp/solr-go",
    "zk": {
      "artifactUrl":"file:///Users/dennis/tmp/zookeeper-3.4.8.tar.gz",
      "ports": [ 20001, 20002, 20003 ],
    },
    "solr": {
      "artifactUrl":"file:///Users/dennis/tmp/solr-6.1.0.tgz",
      "ports": [ 30001, 30002, 30003 ],
      "memory": "2g"
    }
  }

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

  if 'zk' == args.command:
    handleZookeeper(args, config)
  elif 'solr' == args.command:
    handleSolr(args, config)
  else:
    handleBoth(args, config, args.command)


def run():
  parser = argparse.ArgumentParser(description='Solr Bootstrapping')
  subParsers = parser.add_subparsers()

  zkParser = subParsers.add_parser('zk')
  zkParser.set_defaults(command='zk')
  zkParser.add_argument('subcommand', choices=['install','uninstall','start','stop','status'])

  solrParser = subParsers.add_parser('solr')
  solrParser.set_defaults(command='solr')
  solrParser.add_argument('subcommand', choices=['install','uninstall','start','stop','status'])

  installParser = subParsers.add_parser('install')
  installParser.set_defaults(command='install')

  uninstallParser = subParsers.add_parser('uninstall')
  uninstallParser.set_defaults(command='uninstall')

  startParser = subParsers.add_parser('start')
  startParser.set_defaults(command='start')

  stopParser = subParsers.add_parser('stop')
  stopParser.set_defaults(command='stop')

  statusParser = subParsers.add_parser('status')
  statusParser.set_defaults(command='status')
  
  doit(parser.parse_args())

if __name__ == "__main__":
  run()
