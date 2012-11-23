#!/usr/bin/python

import glob

# List of files to use as initial seed
file_list= glob.glob('./files/*')

# List of applications to test
apps = [
#    "/usr/bin/libreoffice"
    "/usr/bin/gedit",
    "/bin/ed",
    "/usr/bin/w3m",
#    "/usr/bin/emacs",
#    "/usr/bin/bluefish",
    "/bin/nano",
    "/usr/bin/vim"
    ]

fuzz_output = "fuzz.txt"

fuzzes = [ 	10,
		27,
		47,
		51,
		100,
	   	200,
		250
	 ]

#FuzzFactor = 250
num_tests = 100

tempf = "./temp"
res_dir = "./results/"

########### end configuration ##########

import math
import random
import string
import subprocess
import time
import datetime
import os
from shutil import copyfile

nil = open('/dev/null', 'r')

while True:
#for i in range(num_tests):
    file_choice = random.choice(file_list)
    FuzzFactor = random.choice(fuzzes)
#    app = random.choice(apps)

    buf = bytearray(open(file_choice, 'rb').read())

    # start Charlie Miller code
    try:
        numwrites=random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1
    except ValueError as ve:
#        print "Skipping empty file"
        continue

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)
    #end Charlie Miller code

    open(fuzz_output, 'wb').write(buf)

    for app in apps:
        f = open(tempf, 'w')
#        print app
        try:
            process = subprocess.Popen([app, fuzz_output], stderr=subprocess.STDOUT, \
                                   stdout=f, stdin=nil, bufsize=-1)
        except OSError as e:
            print e, e.args, e.message
#        print process, app 
        time.sleep(1)
        crashed = process.poll()
        # nano returns 1 on sigs term and hup.. why is this a problem?
        if not crashed or app == "/bin/nano" and crashed == 1:
            try:
                process.terminate()
            except OSError:
                f.close()
                f = open(tempf, 'r')
#                print app, f.read()
            f.close()
        else:
            print 'else saving results...', app
            f.close()
            dt = datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")
            fname = res_dir + os.path.basename(app) + ".ttyout" + dt
            copyfile(tempf, fname)
            fname = res_dir + os.path.basename(app) + ".fuzz_dat" + dt
            copyfile(fuzz_output, fname)


nil.close()

