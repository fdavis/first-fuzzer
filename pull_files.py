#!/usr/bin/python

# Fletcher Davis
# The purpose of this file is to walk your filesystem
# Starting from directory -d, and copy into directory -t
# All files with a file extension given by 
# -e, a csv list of file extensions
# To avoid file bloat, we do not copy files 
# when the name already exists into -t

import os
import sys
from optparse import OptionParser
from shutil import copyfile

parser = OptionParser()
parser.add_option("-d", "--directory", dest="dir", default=".", type="string",
                  help="directory to recurse into", metavar="D")
parser.add_option("-e", "--extensions", dest="ext", default="txt", type="string",
                  help="comma separated list of file extensions to copy", metavar="E")
parser.add_option("-t", "--target", dest="target", default=".", type="string",
                  help="target directory to copy to", metavar="T")
parser.add_option("-v", action="store_true", dest="verbose")
(options, args) = parser.parse_args()

tag_error = "ERROR"
tag_warn = "WARNING"

if options.verbose:
    def v(msg):
        sys.stdout.write(msg + "\n")
else:
    def v(msg):
        pass

def wstderr(tag, msg):
    sys.stderr.write(tag + ":\t" + msg)

options.dire = os.path.realpath(os.path.expanduser(options.dir))
if not os.path.exists(options.dire) or not os.path.isdir(options.dire):
    wstderr(tag_error, "The directory: " + options.dire + " expanded from: " + options.dir + " either does not exist or is not a directory\n")
    exit(2)

v("starting directory will be: " + options.dire)

options.tare = os.path.realpath(os.path.expanduser(options.target))
if not os.path.exists(options.tare) or not os.path.isdir(options.tare):
    wstderr(tag_error, "The directory: " + options.tare + " expanded from: " + options.target + " either does not exist or is not a directory\n")
    exit(2)

v("target copy directory will be: " + options.tare)

extensions = set()
for e in options.ext.split(','):
    extensions.add(e)

v("extensions set is: " + str(extensions))

cnt = 0
for dir in os.walk(options.dire):
    for file in dir[2]:
        tpath = os.path.join(options.tare, file)
        v("have tpath: " + tpath)
        if not os.path.exists(tpath):
            ext = os.path.splitext(file)[1][1:]
            v("have extension: " + ext) 
            if ext in extensions:
                fpath = os.path.join(dir[0], file)
                v("have fpath: " + fpath)
                try:
                    v("trying to copy")
                    copyfile(fpath, tpath)
                    v("finished copy")
                    cnt += 1
                except IOError as e:
                    wstderr(tag_warn, "Copyfile failed with: copyfile(" + fpath + ", " + tpath + ")\n")

sys.stdout.write("Copyfile copied " + str(cnt) + " files into " + options.tare + "\n")
