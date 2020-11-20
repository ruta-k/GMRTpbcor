# A script to generate an image corresponding to a GMRT beam.
# Uses the beamshape parameters provided by Nimisha Kantharia. 
#
# Written by Ruta Kale with the help of Divya Oberoi.
#
# The corresponding xml file is gmrtpb.xml.
#
''' To use this task:
 - Have the task_gmrtpb.py and gmrtpb.xml files in the same folder.
 - start casa in this folder
 - at the casa prompt give the command 
   os.system('buildmytasks')
   It produces a few new files in this folder.
 - at the CASA prompt give the command 
   execfile('mytasks.py')
   The task named gmrtpb is ready for use.
 - The command 'inp gmrtpb' at CASA prompt will show the inputs to this task.
   Ruta Kale, 20140129
 - A bug in the increment in ra and dec was spotted by Divya. Correction made.
   Ruta Kale, 20160907'''

from taskinit import *
from imhead_cli import imhead_cli as imhead
import numpy as np
import sys
import os
import math

def gmrtpb(imagein=None,imageout=None):

# Print any logger messages as originating from gmrtpb
	casalog.origin('gmrtpb')
#    casalog.post('Input and output files are'+imagein+' '+imageout)
# Reading the image parameters 
	teles = imhead(imagename=imagein,mode ='get',hdkey='telescope') 
#	print teles
	print 'Image using observation with the', teles
	casalog.post('Image using observation with the'+' '+teles)
# reading the freq and units keywords to identify frequency
	if teles != 'GMRT':
		casalog.post('This is not a GMRT image; this is not the right program to use.')
	else:
		casalog.post('This is a GMRT image...continuing.')
# The crtype3 and crtype4 are exchanged in GMRT image files created in CASA 
# as compared to those imported to CASA using importfits.
# A check is made to pick up the right parameter that contains the 
# frequency information.
 		chkfreq1 = imhead(imagename=imagein, 
                      mode ='get',
                      hdkey='ctype3')

		chkfreq2 = imhead(imagename=imagein, 
                      mode ='get',
                      hdkey='ctype4')

		if chkfreq1 == 'Frequency':
			frequency = imhead(imagename=imagein, 
                           mode ='get',
                           hdkey='crval3')
		elif chkfreq2 == 'Frequency':
			frequency = imhead(imagename=imagein, 
                           mode ='get',
                           hdkey='crval4')
		funit = frequency['unit']
		print 'The image is at', frequency['value'], funit
# frequency['value']  # in Hz
		hz2ghz = 10**(-9)
		nu = hz2ghz*frequency['value']  # in GHz
		print nu, 'GHz'
		imshape = imhead(imagename=imagein, 
                     mode ='get',
                     hdkey='shape')    # read image shape from image file header

		npix_ra, npix_dec = imshape[0], imshape[1] # imsize, pixels
		d_ra = imhead(imagename=imagein, mode ='get', hdkey='cdelt1') ['value']
		# read RA cell size from image header (rad)
		d_dec = imhead(imagename=imagein, mode ='get', hdkey='cdelt2')['value']
		# read Dec cell size from image header (rad)
		print 'imsize in pixels =',npix_ra, npix_dec
		rad2arcsec = ((180.0/math.pi)*3600.0)
		print 'cellsize in arcsec =', d_ra*rad2arcsec, d_dec*rad2arcsec
# Beam parameters (from Nimisha's webpage/gmrt_pb.py)
# Updated in Nov 2020 using the GMRT User's Manual 
# Freq range is approximate
		if 0.2< nu < 0.28:
			hpbw = 114.0 #arcminutes
			a, b, c, d = -3.366, 46.159, -29.963, 7.529
			print 'using pbparms for', nu, 'GHz', a, b, c, d  
		elif 0.3< nu<0.35:
			hpbw = 81.0 #arcminutes
			a, b, c, d = -3.397, 47.192, -30.931, 7.803
			print 'using pbparms for', nu, 'GHz', a, b, c, d   
		elif 0.55<nu<0.65:
			hpbw = 43.0 #arcminutes
			a, b, c, d = -3.486, 47.749, -35.203, 10.399
			print 'using pbparms for', nu, 'GHz', a, b, c, d   
		elif 1.1<nu<1.4:
			hpbw = 26.2 # arcminutes
			a, b, c, d = -2.27961, 21.4611, -9.7929, 1.80153
			print 'using pbparms for', nu, 'GHz', a, b, c, d
		elif 0.12< nu<0.18:
			hpbw = 186.0 #arcminutes
			a, b, c, d = -4.04, 76.2, -68.8, 22.03
			print 'using pbparms for', nu, 'GHz', a, b, c, d 			
		else:
			print 'No GMRT primary beam shape available'  
# Copy the input image to the output image name
		os.system('cp -rp '+imagein+' '+imageout)
		print "Done 1"
		start_ra=(npix_ra/2-0.5)*d_ra*rad2arcsec
		print "Done 1"
		end_ra=(-1.0*npix_ra/2+0.5)*d_ra*rad2arcsec
                print "Done 2"
		ra = np.linspace(start_ra,end_ra,npix_ra)
		start_dec=(-1.0*npix_dec/2+0.5)*d_dec*rad2arcsec
		end_dec=(npix_dec/2-0.5)*d_dec*rad2arcsec
		dec = np.linspace(start_dec,end_dec,npix_dec)
		arcsec2arcmin=1.0/60.0
# use the casa toolkit to open the output image
		ia.open(imageout)
		beam=ia.getchunk()
		i = 0
		while i < npix_ra:
			j = 0
	                print "In the loop"
			while j < npix_dec:
				x = math.sqrt(ra[i]*ra[i]+dec[j]*dec[j])*arcsec2arcmin*nu
				beam[i,j,0,0] = 1.0 + (a/10**3)*x**2 + (b/10**7)*x**4 + (c/10**10)*x**6 + (d/10**13)*x**8
				j = j + 1
			i = i + 1
		ia.putchunk(beam)
		ia.close()
