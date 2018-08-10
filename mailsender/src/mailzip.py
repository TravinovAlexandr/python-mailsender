#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno

def makeArhiveFromDir(path):
    if os.access(path, os.R_OK) == True:
        try:
            import shutil
            dirName = "/tmp%s" % path[ path.rfind("/") :]
            os.mkdir(dirName)
            shutil.make_archive(dirName + path[ path.rfind("/") :], "zip", path)
            return dirName
        except OSError as err:
            if err.errno == errno.EEXIST:
                return -1
            if err.errno == 13:
                removeTmpDir(path)
                return -2
    else:
            return -3

def makeArhiveFromFile(path):
    if os.access(path, os.R_OK):
        import zipfile
        zipOb = None
        try:
            dirName = "/tmp%s" % path[ path.rfind("/") :]
            os.mkdir(dirName)
            zipOb = zipfile.ZipFile(dirName + path[ path.rfind("/") : ]+ ".zip", "w")
            zipOb.write(path)
            return dirName
        except OSError as err:
            if err.errno == errno.EEXIST:
                return -1
            if err.errno == 13:
                removeTmpDir(path)
                return -2
        finally:
            try:
                zipOb.close()
            except:
                pass
    else:
        return -3

def removeTmpDir(path):
    try:
        import shutil
        import sys
        shutil.rmtree("/tmp%s" % path[ path.rfind("/") :])
    except IOError:
        print("{0}: File is not found: {1}".format(sys.argv[0], path))
    except:
        print("{0}: Some file(s) in {1} is not writhable:".format(sys.argv[0],  path))