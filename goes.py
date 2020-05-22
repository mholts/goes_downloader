#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Mike Holts
#
# Simple script to download GOES data based off of work done by Brian Blaylock
# Reference page: http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi
# See more info in the 'Other Ways to Download' section

import s3fs
import numpy as np
import shutil
import os
import glob
from datetime import datetime, timedelta
import argparse
import logging

#defaults

VIEW = 'CMIPC'
BAND = 'M6C01'
GOES = '16'
debug_enabled = False

def parse_command_line():
	global VIEW, BAND, GOES
	aparser = argparse.ArgumentParser(prog='goes.py')
	aparser.add_argument('-v', '--view', help='select sat view (conus, full, meso1, meso2)')
	aparser.add_argument('-b', '--band', help='select which band(s); (2 digit number.. ie: 02, 14')
	aparser.add_argument('-g', '--goes', help='select which GOES satellite (16 or 17)')
	args = aparser.parse_args()
	if args.view:
		if args.view == 'conus':
			VIEW = 'CMIPC'
		if args.view == 'full':
			VIEW = 'CMIPF'
		if args.view == 'meso1':
			VIEW = 'CMIPM'
		if args.view == 'meso2':
			VIEW = 'CMIPM'			
	if args.band:
		BAND = 'M6C' + args.band
	if args.goes:
		GOES = args.goes

if __name__ == '__main__': 
	# set the logging
	logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z',
		  level=logging.INFO if not debug_enabled else logging.DEBUG)

	parse_command_line()

	day_of_year_now = datetime.utcnow().timetuple().tm_yday
	now = datetime.utcnow()
	year = now.year
	hour = now.hour
	one_hour_ago = now - timedelta(hours=1)
	one_hour_ago_year = one_hour_ago.year
	one_hour_ago_hour = one_hour_ago.hour
	one_hour_ago_days = one_hour_ago.timetuple().tm_yday

	directory_one_hour_ago = "noaa-goes{}/ABI-L2-{}/{}/{}/{}".format(GOES, VIEW, one_hour_ago_year, one_hour_ago_days, one_hour_ago_hour)
	directory_now = "noaa-goes{}/ABI-L2-{}/{}/{}/{}".format(GOES, VIEW, year, day_of_year_now, hour)

	if os.path.isdir('imagery'):
		sat_files = glob.glob('imagery/*')
		logging.info("Imagery folder exists, deleting all files in it.")
		for f in sat_files:
			os.remove(f)
		logging.info("Files deleted.")
	else:
		try:
			logging.info("Imagery folder does not exist, attempting to create it now.")
			os.mkdir('imagery')
		except:
			logging.info("Could not create the imagery folder, this is a problem. Exiting script...")

	# Use the anonymous credentials to access public data
	fs = s3fs.S3FileSystem(anon=True)
	files=[]
	try:
		files1 = np.array(fs.ls(directory_one_hour_ago))
		files.append(files1)
	except:
		logging.info("Could not get files from the previous hour, likely because the source is empty.")
	try:
		files2 = np.array(fs.ls(directory_now))
		files.append(files2)
	except:
		logging.info("Could not get files from the current hour, likely because the source is empty.")

	# Download the first file, and rename it the same name (without the directory structure)
	for f in files:
		for fi in f:
			if BAND in fi:
				try:
					loc=fi.split("/")[-1]
					loc = 'imagery/'+loc
					logging.info("Downloading {}".format(loc))
					fs.get(fi, loc)
				except:
					logging.info("Downloading {} failed.  Continuing...".format(loc))
					continue
	logging.info("Download complete.")
