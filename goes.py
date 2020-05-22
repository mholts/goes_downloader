# Brian Blaylock
# Requres `s3fs`
# Website: https://s3fs.readthedocs.io/en/latest/
# In Anaconda, download via conda-forge.

import s3fs
import numpy as np
import shutil
import os
from datetime import datetime, timedelta
import argparse

#defaults
VIEW = 'CMIPC'
BAND = 'M6C01'
GOES = '16'

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

parse_command_line()


#time information
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

try:
	shutil.rmtree('imagery')
except:
	print 'no directory to delete'

try: 
	os.mkdir('imagery')
except:
	print 'could not create directory'

# Use the anonymous credentials to access public data
fs = s3fs.S3FileSystem(anon=True)

files1 = np.array(fs.ls(directory_one_hour_ago))
files2 = np.array(fs.ls(directory_now))

# Download the first file, and rename it the same name (without the directory structure)
for fi in files1:
	if BAND in fi:
		try:
			loc=fi.split("/")[-1]
			loc = 'imagery/'+loc
			fs.get(fi, loc)
		except:
			print 'previous hour not downloaded'
for fi in files2:
	if BAND in fi:
		try:
			loc=fi.split("/")[-1]
			loc = 'imagery/'+loc
			fs.get(fi, loc)
		except:
			print 'latest hour not downloaded'

print "Downloading finished"