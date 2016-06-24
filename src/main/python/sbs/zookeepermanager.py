#!/bin/python

import os
import shutil
import json
import urllib
import tarfile
import subprocess
import sys

from filemanager import FileManager

class ZookeeperManager(object):

  def __init__(self, configuration):
    self.configuration = configuration

  def install(self):
    print "Installing Zookeeper to %s/bin/zookeeper" % (self.configuration["rootDirectory"])
    
    # create install directories
    FileManager.createDirectory("%s" % (self.configuration["rootDirectory"]))
    FileManager.createDirectory("%s/packages" % (self.configuration["rootDirectory"]))
    FileManager.createDirectory("%s/bin" % (self.configuration["rootDirectory"]))

    # download zookeeper
    FileManager.download(self.configuration["zk"]["artifactUrl"], "%s/packages/zookeeper.tgz" % (self.configuration["rootDirectory"]))

    # unpack zookeeper
    extractionDir = FileManager.extractTarball("%s/packages/zookeeper.tgz" % (self.configuration["rootDirectory"]), "%s/bin" % (self.configuration["rootDirectory"]))
    shutil.move("%s/bin/%s" % (self.configuration["rootDirectory"], extractionDir), "%s/bin/zookeeper" % (self.configuration["rootDirectory"]))

  def uninstall(self):
    path = "%s/bin/zookeeper" % (self.configuration["rootDirectory"])
    if os.path.exists(path):
      print "Removing Zookeeper from %s" % (path)
      shutil.rmtree(path)
      return True
    else:
      print "Zookeeper install not found at %s" % (path)
      return False

  def start(self):

    # create base data/conf directory
    FileManager.createDirectory("%s/data/zookeeper" % (self.configuration["rootDirectory"]))
    FileManager.createDirectory("%s/log/zookeeper" % (self.configuration["rootDirectory"]))

    for port in self.configuration["zk"]["ports"]:
      print "Starting zookeeper on port %d" % port

      # create required items
      dataDirectory = "%s/data/zookeeper/instance-%d" % (self.configuration["rootDirectory"], port)
      logDirectory = "%s/log/zookeeper/instance-%d" % (self.configuration["rootDirectory"], port)
      configurationFilePath = "%s/data/zookeeper/instance-%d.cfg" % (self.configuration["rootDirectory"], port)
      myidFilePath = "%s/data/zookeeper/instance-%d/myid" % (self.configuration["rootDirectory"], port)

      FileManager.createDirectory(logDirectory)
      FileManager.createDirectory(dataDirectory)

      configLines = self.createConfigLines(port, dataDirectory)
      with open(configurationFilePath, 'w') as f:
        f.writelines(configLines)

      with open(myidFilePath, 'w') as f:
        f.writelines(["%s" % port])

      # actually start zookeeper
      arguments = [
        "ZOOCFGDIR=%s/data/zookeeper" % (self.configuration["rootDirectory"]),
        "ZOOCFG=instance-%d.cfg" % (port),
        "ZOO_LOG_DIR=%s" % (logDirectory),
        "%s/bin/zookeeper/bin/zkServer.sh" % (self.configuration["rootDirectory"]),
        "start"
      ]
      os.system(" ".join(arguments))

  def stop(self):
    
    for port in self.configuration["zk"]["ports"]:
      configurationFilePath = "%s/data/zookeeper/instance-%d.cfg" % (self.configuration["rootDirectory"], port)

      if os.path.exists(configurationFilePath):
        print "Stopping zookeeper on port %d" % port

        # actually stop zookeeper
        arguments = [
          "ZOOCFGDIR=%s/data/zookeeper" % (self.configuration["rootDirectory"]),
          "ZOOCFG=instance-%d.cfg" % (port),
          "%s/bin/zookeeper/bin/zkServer.sh" % (self.configuration["rootDirectory"]),
          "stop"
        ]
        # print " ".join(arguments)
        os.system(" ".join(arguments))

  def status(self):
    print "Zookeeper Status:"

    # Check installation
    installPath = "%s/bin/zookeeper" % self.configuration["rootDirectory"]
    if os.path.exists(installPath):
      print "  Installed: Yes, at %s" % (installPath)
    else:
      print "  Installed: No, expected at %s" % (installPath)

    # Check running status
    print "  Instances:"
    for port in self.configuration["zk"]["ports"]:
      print "    Port %d:" % (port)

      dataDirectory = "%s/data/zookeeper/instance-%d" % (self.configuration["rootDirectory"], port)
      if os.path.exists(dataDirectory):
        print "      Data Directory: Yes, at %s" % (dataDirectory)
      else:
        print "      Data Directory: No, expected at %s" % (dataDirectory)

      logDirectory = "%s/log/zookeeper/instance-%d" % (self.configuration["rootDirectory"], port)
      if os.path.exists(logDirectory):
        print "      Log Directory: Yes, at %s" % (logDirectory)
      else:
        print "      Log Directory: No, expected at %s" % (logDirectory)

      configurationFilePath = "%s/data/zookeeper/instance-%d.cfg" % (self.configuration["rootDirectory"], port)
      if os.path.exists(configurationFilePath):
        print "      Configuration File: Yes, at %s" % (configurationFilePath)
      else:
        print "      Configuration File: No, expected at %s" % (configurationFilePath)

      pidFilePath = "%s/data/zookeeper/instance-%d/zookeeper_server.pid" % (self.configuration["rootDirectory"], port)
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

  def createConfigLines(self, instancePort, dataDirectory):
    lines = [
      "tickTime=2000\n",
      "dataDir=%s\n" % dataDirectory,
      "clientPort=%d\n" % instancePort,
      "initLimit=5\n",
      "syncLimit=2\n",
    ]

    for port in self.configuration["zk"]["ports"]:
      lines.append("server.%d=localhost:%d:%d\n" % (port, port + 1000, port + 2000))

    return lines
