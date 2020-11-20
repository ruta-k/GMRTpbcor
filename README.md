# GMRTpbcor
A recipe for GMRT primary beam correction in CASA. This works in CASA 4.7 (casa-release-4.7.2-el7). 
The task may not work in other more recent versions of CASA.

How to use the task 'gmrtpb':
 - Keep the task_gmrtpb.py and gmrtpb.xml files in the same directory.
 - Start CASA in this directory.
 - At the CASA prompt give the command
   os.system('buildmytasks')
   It produces a few new files in this directory; one of which is 'mytasks.py'.
 - At the CASA prompt give the command
   execfile('mytasks.py')
   The task named gmrtpb is ready for use.
 - The command 'inp gmrtpb' at CASA prompt will show the inputs to this task.

Ruta Kale, 20140129

