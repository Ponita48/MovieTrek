import threading, time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from infi.systray import SysTrayIcon

url = "http://localhost:13579/variables.html"
running = True

def run():
	global running
	while running:
		try:
			page = urlopen(url)
			soup = BeautifulSoup(page)
			filedir = soup.find(id="filedir").string
			movie_name = filedir.split('\\')
			movie_name = movie_name[-1]

			file = soup.find(id="file").string

			pos = soup.find(id="positionstring").string
			duration = soup.find(id="durationstring").string

			print(movie_name, file, pos, duration)
		except Exception as e:
			print("Player Offline or Web Interface disabled")

def stop(systray):
	global running
	running = False

def start(systray):
	thread = threading.Thread(target=run, args=())
	thread.start()

menu_option = (("Start", None, start),("Stop", None, stop))
systray = SysTrayIcon("icon.ico", "Example", menu_option)
systray.start()