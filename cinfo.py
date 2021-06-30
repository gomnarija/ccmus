import ueberzug.lib.v0 as ueberzug
import time
import os 
import subprocess
import ueberzug.tmux_util as uztmux
import curses
import sys


mu_path = "/mu/"






class img:
	x=0
	y=0
	width=0
	height=0


cols = 0
lines = 0

t_left = 0 #starting left position of terminal 
t_top = 0   #starting top   position of terminal 

def_cover = os.path.dirname(__file__)+"/default.jpg"




def cmu_ison():
	return os.system("cmus-remote -C status >> /dev/null") == 0




def cmu_get(field):
	
	raw = subprocess.check_output(["cmus-remote","-Q"])
		
	#status format:	
	#tag album [ALBUMNAME]

	if field in raw.decode():
		tks = raw.decode().split('\n')
		return [x for x in tks if field in x][0].replace("tag","").replace(field,"").strip()

	else:
		return []


def cmu_get_album():
	
	if cmu_ison():
		if cmu_get("status") != "stopped" : #check if song is playing
			res =  cmu_get("album") 
			return res if res != [] else "[ALBUM]"

	return "[ALBUM]"
	

def cmu_get_artist():
	
	if cmu_ison():
		if cmu_get("status") != "stopped" :#check if song is playing
			res =  cmu_get("artist") 
			return res if res != [] else "[ARTIST]"

	return "[ARTIST]"
	

def get_cover_path(album_name):	
	mu_dir = os.listdir(mu_path)
	for dir in mu_dir:
		if album_name.lower() in dir:
			for file in os.listdir(mu_path+dir):
				if "cover" in file:
					return mu_path+dir+"/"+file
	
	return def_cover




	
def place_cover():	



	global cols
	global lines	

	i = img()

	cols = int(subprocess.check_output(["tput", "cols"])) #twice as much as lines
	lines = int(subprocess.check_output(["tput", "lines"]))

	
	if("-h" in sys.argv): #side

		i.height = (lines/3)//1.3 # placed in first third(by height),
		i.width = i.height * 2		#second third is text
		i.x = (cols//2)-(i.width//2)
		i.y = 3


	else:#bellow
		i.height = (lines//2)//1.2 # placed in first half (by height)
		i.width = i.height*2;		#second half is text
		i.x = (cols/2)-(i.width/2)
		i.y = lines//4 - i.height//2

		

	if i.x < 0:
		i.x = 0
	if i.y < 0:
		i.y = 0

	if i.width > cols:
		i.width =  cols
		i.height = cols // 2 

	if i.height > lines:
		i.height =  lines
		i.width = cols // 2

	return i



def setup_curses(h,w,y,x):

	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr = curses.newwin(h,w,y,x)

	return stdscr

def draw_curses(stdscr,album,artist):
	y,x = stdscr.getmaxyx()#rows and collums in curses window

	stdscr.clear()
	curses.resizeterm(y,x)
	stdscr.refresh()
	
	
	#if album or artist name too long, cut it 
	#and add '...' at the end

	if( len(album) >= cols):
		album = album[:cols-4] + "..."
	
	if( len(artist) >= cols):
		artist = artist[:cols-4] + "..."



	ypos = 0
	if "-h" in sys.argv:#side
		ypos = lines-((lines//3)*2) #placed in second third
		ypos += 3			#first third is cover
	else:#bellow
		ypos = lines-((lines//2)) #placed in second half
						#first half is cover

	stdscr.addstr(ypos,cols//2-(len(album)//2),album, curses.A_NORMAL)
	stdscr.addstr(ypos+2,cols//2-(len(artist)//2),artist, curses.A_NORMAL)
	
	stdscr.refresh()




with ueberzug.Canvas() as c:
	cover = c.create_placement('cover', x=0, y=0,width = 50,height=50, scaler=ueberzug.ScalerOption.DISTORT.value)
	cover.path = def_cover
	cover.visibility = ueberzug.Visibility.VISIBLE
	
	t_left = uztmux.get_offset().left if uztmux.is_used() else 0
	t_top   = uztmux.get_offset().top   if uztmux.is_used() else 0
	


	stdscr = setup_curses(lines,cols,0,0)

	while True:

		if(not cmu_ison()):
			exit()

		time.sleep(1/30)
		with c.lazy_drawing:
		

			i = place_cover()
			
			album = cmu_get_album()
			artist = cmu_get_artist()		
	
			if album != "[ALBUM]":
				cover.path = get_cover_path(album)
			else:
				cover.path = def_cover
			

			draw_curses(stdscr,album,artist)

		
			if uztmux.is_used(): 
				if "-h" in sys.argv:
					midx = uztmux.get_offset().left - t_left # mid point between panes
					midy = 0
				else:
					midx = 0
					midy = uztmux.get_offset().top - t_top # mid point between panes
			else:
				midx  = 0
				midy = 0

		
			cover.width   =  i.width
			cover.height  =  i.height
				
			cover.x = midx + i.x
			cover.y = midy + i.y

		
