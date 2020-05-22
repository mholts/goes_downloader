# GOES 16/17 Data Downloader


----

## Overview

This script is built to download GOES 16/17 data from public Amazon Web Services (AWS) to the local machine.  The intention was for this to be a quick download for users of WSV3 Weather Display software.  

This script was based off of work done by Brian Blaylock found here: http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi

## Use

When run on the command line , the script defaults to use GOES 16, Conus View, Band 01.  These parameters can be set using the following arguments:

-v; conus, full, meso1, meso2 (right now I don't think it matters if you pick meso1 or meso2, I think both will download)

-b; 01, 02, 03 .... 16 (which band to download)

-g; 16 or 17 (which GOES satellite to use)

So if you wanted to download the full disk for band 16 your command line command would look like:

python goes.py -v full -b 16

