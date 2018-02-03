#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  TMLinux.py
#  
#  Copyright 2017 DW <dworth@moby.local>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
"""A time machine like backup prgoram for Linux.  Uses rsync as its base
	and manages backups using hard links.
	
Args:
	-c or --conf: The path of the configuration file
	-i or --inclist: The path of the backup include file.  This contains
						a list of what to backup.
	-d or --debug: Print out debug information.
	
	
"""

import sys
import os
import argparse
import subprocess
import time
from configparser import ConfigParser
    
MYNAME =  os.path.basename(sys.argv[0])
print('prog name is ', MYNAME)

parser = argparse.ArgumentParser(prog=MYNAME, description='%(MYNAME)s is a backup program for linux that is in the spirit of Time Machine for Mac OSX.')
parser.add_argument('-c', '--conf', action='store', required=True, dest="tmcfg", help="Path of the configuration file")
parser.add_argument('-i', '--inclist', action='store', required=True, dest="tminclude", help="The path of the backup include file")
parser.add_argument('-d', '--debug', action='store_true', default=False, dest="dflag", help="Print out debug information")
    
opts = parser.parse_args()

##print("DFLAG: ", opts.dflag)



def bld_cmd(cfgfile, lst):
	cfgs = ConfigParser()
	cfgs.read(cfgfile)
	
	##Get current date/time
	DATE = time.strftime("%Y%m%d.%H%M%S")
	Debug('DATE is: ' + DATE)
	##Get hostname for Backupdir
	hostname = os.uname().nodename
	
	for section_name in cfgs.sections():
		print('Section: ', section_name)
		print(' Options: ', cfgs.options(section_name))
		for name, value in cfgs.items(section_name):
			Debug(' {} = {}'.format(name, value))
		##Debug()
		
	cmd = cfgs['cmd']
	##print(cmd['rsync'], cmd['opts'])
	
	LOGFILE = cfgs.get('usercfg', 'LOGFILE')
	TMEXCLUDE = cfgs.get('usercfg', 'TMEXCLUDE')
	BKUPDIR = cfgs.get('usercfg', 'BKUPDIR')
	BKUPDIR += "/" + hostname
	BKUPDUMP = BKUPDIR + "/" + DATE
	BKUPDUMPLN = DATE
	##LATEST = BKUPDIR + "/Latest"
	LATEST = "./Latest"
	RSYNC = cfgs.get('cmd','RSYNC')
	INITIAL_BKUP_OPTS = cfgs.get('cmd','INIT_OPTS')
	EXIST_BKUP_OPTS = cfgs.get('cmd','EXIST_OPTS')
	EXIST_BKUP_OPTS += BKUPDIR + "/Latest"
	OPTEX = cfgs.get('cmd','OPTEX')
	OPTEX += TMEXCLUDE
	OPTLOG = cfgs.get('cmd','OPTLOG')
	OPTLOG += LOGFILE
	OPTDEL = cfgs.get('cmd', 'OPTDEL')
	
	##Debug
	#Build command
	LS = "ls"
	o1 = "-l"
	o2 = "-t"
	##End debug
	
	STATUS = check_run_type(BKUPDIR)
	Debug('STATUS OF RUN IS:  ' + STATUS)
	
	if (STATUS == 'EXISTING'):
		RSYNCMD = (RSYNC + " " + EXIST_BKUP_OPTS + " " +  OPTEX + " " + OPTLOG + " " + OPTDEL + " " + lst + " " + BKUPDUMP)
		Debug(RSYNCMD)
		RSYNCOPTS = (EXIST_BKUP_OPTS + " " +  OPTEX + " " + OPTLOG + " " + OPTDEL + " " + lst + " " + BKUPDUMP)
		Debug(RSYNCOPTS)
		os.chdir(BKUPDIR)
		##python 3.6 code
		##subprocess.run([LS, o1, o2, BKUPDIR])
		##End python 3.6 code
		
		##Run Rsync
		##ps = subprocess.Popen(RSYNC, EXIST_BKUP_OPTS, OPTEX, OPTLOG, OPTDEL, lst, BKUPDUMP)
		
		try:
			print("Starting Backup...")
			#####ps = subprocess.check_call(RSYNCMD.split())
		except OSError as err:
			print("OS Error: Error with rsync cmd: {0}".format(err))
			raise
		except:
			print("Unexplained error:", sys.exc_info()[0])
			raise
			
		##print("PS1 is: ",ps)
		
		
		##TESTING CODE
		##os.mkdir(BKUPDUMP)
		##END TEST CODE
		
		print("Removing Latest: ", LATEST)
		try:
			os.remove(LATEST)
		except:
			print("Symling Latest: ", LATEST, "Does not exist")
			pass
			
		print("Creating Latest Sym Link")
		os.symlink(BKUPDUMPLN,LATEST)
		ps = subprocess.Popen([LS, o1, o2, BKUPDIR])
		ps = ("PS2 is: ", ps)
		Debug(ps)
	else:
		RSYNCMD = (RSYNC + " " + INITIAL_BKUP_OPTS + " " + OPTEX + " " + OPTLOG + " " + OPTDEL + " " + lst + " " + BKUPDUMP)
		##RSYNCMD = [RSYNC, INITIAL_BKUP_OPTS, OPTEX, OPTLOG, OPTDEL, lst, BKUPDUMP]
		Debug(RSYNCMD)
		RSYNCOPTS = (INITIAL_BKUP_OPTS + " " + OPTEX + " " + OPTLOG + " " + OPTDEL + " " + lst + " " + BKUPDUMP)
		Debug(RSYNCOPTS)
		os.chdir(BKUPDIR)
		##python 3.6 code
		##subprocess.run([LS, o1, o2, BKUPDIR])
		##end python 3.6 code
		
		##Run Rsync
		##ps = subprocess.Popen([RSYNC, INITIAL_BKUP_OPTS, OPTDEL.split(), OPTEX, OPTLOG, lst, BKUPDUMP])
		try:
			print("Starting Backup...")
			####ps = subprocess.check_call(RSYNCMD.split())
		except OSError as err:
			print("OS Error: Error with rsync cmd: {0}".format(err))
			raise
		except:
			print("Unexplained error:", sys.exc_info()[0])
			raise
			
		##print("PS1 is: ",ps)
		
		
		##TESTING CODE
		##os.mkdir(BKUPDUMP)
		##END TEST CODE
		print("Removing Latest: ", LATEST)
		try:
			os.remove(LATEST)
		except:
			print("Symling Latest: ", LATEST, "Does not exist")
			pass
		print("Creating Latest Sym Link")
		os.symlink(BKUPDUMPLN,LATEST)
		ps = subprocess.call([LS, o1, o2, BKUPDIR])
		ps = ("PS2 is: ", ps)
		Debug(ps)
		
		
	##subprocess.run([LS, o1, o2])
	##rtn = subprocess.Popen([LS, o1, o2])
	##RSYNCMD = (RSYNC +  OPTS +  OPTEX + " OPTLOG" +  " OPTDEL" + " lst" + " BKUPDIR")
	##print("Listing is: ", rtn)
	##RSYNCMD = [RSYNC, OPTS, OPTEX, OPTLOG, OPTDEL, lst, BKUPDIR]
	##print(RSYNCMD)
	##print(RSYNC, OPTS, OPTEX, OPTLOG, OPTDEL, lst, BKUPDIR)
	
	
def Debug(msg):
	if(opts.dflag):
		print("DEBUG: ", msg)
		
	
def check_run_type(path):
	
	##Might want to check if Backup exists and mounted
	
	##Check to see if Backup Path exists
	if os.path.exists(path):
		Debug("The Path: " + path + " exists")
		path += "/Latest"
		Debug("The Path is now: " + path)
		##if os.path.lexists(path):
		if os.path.islink(path) and os.path.isdir(path):
			return("EXISTING")
		else:
			return("NEWRUN")
	else:
		##Make new dir
		os.makedirs(path)
		return("FIRSTRUN")
		
	
def get_bkup_list(filelist):
	with open(filelist, mode='rt', encoding='utf-8') as f:
		bkup_list = []
		lst=""
		for line in f:
			a = line.strip()
			bkup_list.append(a+" ")
			lst+=a+" "
	return bkup_list, lst
	
#def main(filename, cfgfile):
def main(tminclude, tmcfg):
	bkup_list, lst = get_bkup_list(tminclude)
	Debug(bkup_list)
	Debug(lst)
	for dir in bkup_list:
		print(dir)
	bld_cmd(tmcfg, lst)

if __name__ == '__main__':
    main(opts.tminclude, opts.tmcfg)
    ##main(sys.argv[1],sys.argv[2])
