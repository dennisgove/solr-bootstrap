#!/bin/python

import os
import shutil
import sys
import json
import urllib
import tarfile

class FileManager(object):

  @staticmethod
  def createDirectory(path):
    # Creates the directory if it doesn't already exist
    if not os.path.exists(path):
      os.makedirs(path)

  @staticmethod
  def deleteDirectory(path):
    if os.path.exists(path):
      shutil.rmtree(path)

  @staticmethod
  def loadAsJson(path):
    # Loads file as path to a json object
    with open(path) as f:
      return json.load(f)

  @staticmethod
  def download(url, toPath, progress=True):
    # Downloads file at url to path, if progress is True then print progress bar
    # If url begins with file:// then is effectively a file copy
    # eg. file:///tmp/foo.txt

    def dlProgress(count, blockSize, totalSize):
      # dlProgress gotten from http://stackoverflow.com/questions/51212/how-to-write-a-download-progress-indicator-in-python
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("\rDownloading " + url + "...%d%%" % percent)
      sys.stdout.flush()

    urllib.urlretrieve(url, filename=toPath, reporthook=dlProgress if progress else None)
    
    if progress:
      # print newline if we're printing the progress bar
      print

  @staticmethod
  def extractTarball(atPath, toPath):
    # Extracts tarball at path to path, returns name of first seen root directory
    with tarfile.open(atPath) as t:
      t.extractall(path=toPath)
      return t.getmembers()[0].name.split("/")[0]

  @staticmethod
  def readPid(path):
    with open(path, 'r') as f:
      lines = f.readlines()
      if len(lines) >= 1:
        try:
          return int(lines[0].strip())
        except:
          pass

    return None

  @staticmethod
  def isRunning(pid):
    try:
      os.kill(pid, 0)
      return True
    except OSError, err:
      return False

