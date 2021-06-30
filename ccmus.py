import os
import subprocess
import sys

cols = int(subprocess.check_output(["tput", "cols"])) #twice as much as lines
lines = int(subprocess.check_output(["tput", "lines"]))



prc = 60 # at this cols/line ratio, it wil flip the rotation
		#if not stated othervise

#cinfo panel position, can be on the right side or below cmus pane
ori = "-v" if cols / 100 * prc <= lines else "-h" #default if no arguments are given

if "-v" in sys.argv:
	ori = "-v"
if "-h" in sys.argv:
	ori = "-h"
		


rsz_way = "-R" if ori == "-h" else "-D"
rsz_size = cols//4  if ori == "-h" else lines//6


curdir = os.path.dirname(__file__)


#tmux setup
os.system("tmux new-session -d python "+curdir+"/cinfo.py " + ori )
os.system("tmux split-window "+ori+" cmus")
os.system("tmux resize-pane "+rsz_way +" "+ str(rsz_size))
os.system("tmux swap-pane -U")
os.system("tmux -2 attach-session -d")

