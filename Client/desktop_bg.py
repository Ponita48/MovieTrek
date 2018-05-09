import threading, time, json
import requests
import wx
from login import LoginFrame
from register import RegisterFrame
from urllib.request import urlopen
from bs4 import BeautifulSoup
from infi.systray import SysTrayIcon

url = "http://localhost:13579/variables.html"
running = True

# What to do when running
def run():
	global running
	# set our timer to 5 seconds
	every = 5
	start = time.time()
	future = start + every
	while running:
		try:
			# open the page provided
			page = urlopen(url)
			# use BeautifulSoup to parse the HTML
			soup = BeautifulSoup(page, "html.parser")
			# Find the movie name (based on folder name)
			filedir = soup.find(id="filedir").string
			movie_name = filedir.split('\\')
			movie_name = movie_name[-1]
			# Find the filename
			file = soup.find(id="file").string
			# Find the position now and the duration of the movie
			pos = soup.find(id="positionstring").string
			duration = soup.find(id="durationstring").string

			# Check our timer to upload the data
			if time.time() > future:
				sync(movie_name, file, pos, duration)
				start = time.time()
				future = start + every
		except Exception as e:
			# print("Player Offline or Web Interface disabled")
			print(str(e))

# sync to server
def sync(movie_name, file, pos, duration):
	global uid
	data = {
		'folder' : movie_name,
		'title': file,
		'last_position': pos,
		'duration': duration
	}
	req = requests.post('http://localhost:5000/api/insert/' + uid, data=data)
	data = json.loads(json.dumps(req.json()))
	print(data["status"])
	if data["status"] == 0:
		print("Something went wrong" )
	elif data["status"] == 1:
		print("Successfully Updated!")

# stop service
def stop(systray):
	global running
	running = False

# start service
def start(systray):
	thread = threading.Thread(target=run, args=())
	thread.start()

# logout
def logout(systray):
	try:
		os.remove("data")
		wx.MessageBox('Successfully Logged Out!', 'MovieTrek', wx.OK | wx.ICON_INFORMATION)
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise

# login
def login(systray):
	app = wx.App()
	frm = LoginFrame(None)
	frm.Show()
	app.MainLoop()

# register
def register(systray):
	app = wx.App()
	frm = RegisterFrame(None)
	frm.Show()
	app.MainLoop()

menu_option = (("Start", None, start), ("Stop", None, stop), ("Login", None, login), ("Logout", None, logout), ("Register", None, register))
systray = SysTrayIcon("icon.ico", "Example", menu_option)
systray.start()