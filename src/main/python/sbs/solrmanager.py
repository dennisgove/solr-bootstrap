#!/bin/python

import os
import shutil
import json
import urllib
import tarfile
import subprocess
import sys

from filemanager import FileManager

class SolrManager(object):

  def __init__(self, configuration):
    self.configuration = configuration

  def install(self):
    print "Installing Solr to %s/bin/solr" % (self.configuration["rootDirectory"])
    
    # create install directories
    FileManager.createDirectory("%s" % (self.configuration["rootDirectory"]))
    FileManager.createDirectory("%s/packages" % (self.configuration["rootDirectory"]))
    FileManager.createDirectory("%s/bin" % (self.configuration["rootDirectory"]))

    # download solr
    FileManager.download(self.configuration["solr"]["artifactUrl"], "%s/packages/solr.tgz" % (self.configuration["rootDirectory"]))

    # unpack solr
    extractionDir = FileManager.extractTarball("%s/packages/solr.tgz" % (self.configuration["rootDirectory"]), "%s/bin" % (self.configuration["rootDirectory"]))
    shutil.move("%s/bin/%s" % (self.configuration["rootDirectory"], extractionDir), "%s/bin/solr" % (self.configuration["rootDirectory"]))

  def uninstall(self):
    path = "%s/bin/solr" % (self.configuration["rootDirectory"])
    if os.path.exists(path):
      print "Removing Solr from %s" % (path)
      shutil.rmtree(path)
      return True
    else:
      print "Solr install not found at %s" % (path)
      return False

  def start(self):

    # create base data/conf directory
    FileManager.createDirectory("%s/data/solr" % (self.configuration["rootDirectory"]))
    FileManager.createDirectory("%s/log/solr" % (self.configuration["rootDirectory"]))

    for port in self.configuration["solr"]["ports"]:
      print "Starting solr on port %d" % port

      # create required items
      dataDirectory = "%s/data/solr/instance-%d" % (self.configuration["rootDirectory"], port)
      logDirectory = "%s/log/solr/instance-%d" % (self.configuration["rootDirectory"], port)
      FileManager.createDirectory(logDirectory)
      FileManager.createDirectory(dataDirectory)
      FileManager.createDirectory("%s/home" % dataDirectory)

      solrXmlFile = "%s/home/solr.xml" % (dataDirectory)
      configLines = self.createConfigLines(port)
      with open(solrXmlFile, 'w') as f:
        f.writelines(configLines)

      zookeeperConnectionString = ",".join(["localhost:%d" % zkPort for zkPort in self.configuration["zk"]["ports"]])

      # actually start solr
      arguments = [
        "%s/bin/solr/bin/solr" % (self.configuration["rootDirectory"]),
        "-cloud",
        "-m", self.configuration["solr"]["memory"],
        "-p", "%s" % port,
        "-s", "%s/home" % (dataDirectory),
        "-z", zookeeperConnectionString
      ]
      os.system(" ".join(arguments))

  def stop(self):
        
    for port in self.configuration["solr"]["ports"]:
      pidFile = "%s/bin/solr/bin/solr-%d.pid" % (self.configuration["rootDirectory"], port)
      if os.path.exists(pidFile):
        print "Stopping solr on port %d" % port

        arguments = [
          "%s/bin/solr/bin/solr" % (self.configuration["rootDirectory"]),
          "stop",
          "-p", "%s" % (port)
        ]
      
        os.system(" ".join(arguments))

  def status(self):
    print "Solr Status:"

    # Check installation
    installPath = "%s/bin/solr" % self.configuration["rootDirectory"]
    if os.path.exists(installPath):
      print "  Installed: Yes, at %s" % (installPath)
    else:
      print "  Installed: No, expected at %s" % (installPath)

    # Check running status
    print "  Instances:"
    for port in self.configuration["solr"]["ports"]:
      print "    Port %d:" % (port)

      dataDirectory = "%s/data/solr/instance-%d" % (self.configuration["rootDirectory"], port)
      if os.path.exists(dataDirectory):
        print "      Data Directory: Yes, at %s" % (dataDirectory)
      else:
        print "      Data Directory: No, expected at %s" % (dataDirectory)

      logDirectory = "%s/log/solr/instance-%d" % (self.configuration["rootDirectory"], port)
      if os.path.exists(logDirectory):
        print "      Log Directory: Yes, at %s" % (logDirectory)
      else:
        print "      Log Directory: No, expected at %s" % (logDirectory)

      configurationFilePath = "%s/data/solr/instance-%d/home/solr.xml" % (self.configuration["rootDirectory"], port)
      if os.path.exists(configurationFilePath):
        print "      Configuration File: Yes, at %s" % (configurationFilePath)
      else:
        print "      Configuration File: No, expected at %s" % (configurationFilePath)

      pidFilePath = "%s/bin/solr/bin/solr-%d.pid" % (self.configuration["rootDirectory"], port)
      if os.path.exists(pidFilePath):
        print "      Pid File: Yes, at %s" % (pidFilePath)
        pid = FileManager.readPid(pidFilePath)
        if pid:
          if FileManager.isRunning(pid):
            print "      Running: Yes, under pid %d" % (pid)
          else:
            print "      Running: Maybe, expecting process under pid %d but unable to find it" % (pid)
        else:
          print "      Running: Maybe, but unable to find pid"
      else:
        print "      Pid File: No, expected at %s" % (pidFilePath)
        print "      Running: No"

  def createConfigLines(self, instancePort):
    lines = [
      "<solr> ",
      "  <solrcloud>",
      "    <str name='host'>${host:}</str>",
      "    <int name='hostPort'>${jetty.port:%d}</int>" % (instancePort),
      "    <str name='hostContext'>${hostContext:solr}</str>",
      "    <int name='zkClientTimeout'>${zkClientTimeout:15000}</int>",
      "    <bool name='genericCoreNodeNames'>${genericCoreNodeNames:true}</bool>",
      "  </solrcloud>",
      "  <shardHandlerFactory name='shardHandlerFactory' class='HttpShardHandlerFactory'>",
      "    <int name='socketTimeout'>${socketTimeout:0}</int>",
      "    <int name='connTimeout'>${connTimeout:0}</int>",
      "  </shardHandlerFactory>",
      "</solr>",
    ]
    return lines

