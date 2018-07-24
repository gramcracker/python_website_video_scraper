import bs4
import vlc
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import Gtk

Gdk.threads_init ()


show_titles = ['']


base_url = 'https://www.watchcartoononline.com/anime/'


chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options);

# uses random.choice to pick a random episode from a random title in show_titles[]
def get_src_of_rand_video():
	_url = base_url+random.choice(show_titles)
	uClient = uReq(_url) 
	page_soup = soup(uClient.read(), "html.parser")
	uClient.close()
	episodes = page_soup.select("div.cat-eps a.sonra")
	link = random.choice(episodes).get('href')
	#get video source
	driver.get(link)
	iframes = driver.find_elements_by_tag_name('iframe')
	driver.switch_to.frame(1)
	src = driver.find_element_by_id('video-js').find_element_by_tag_name('source').get_attribute('src')
	return src


class ApplicationWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Python-Vlc Media Player")
		self.player_paused=False
		self.is_player_active = False
		self.connect("destroy",Gtk.main_quit)
		self.isFullscreen = False
		self.volume = 100

	def show(self):
		self.show_all()


	def setup_objects_and_events(self):
		self.connect("key-press-event",self._key_press_event)
		self.playback_button = Gtk.Button()
		self.stop_button = Gtk.Button()
		self.update_button = Gtk.Button()
		self.play_image = Gtk.Image.new_from_icon_name(
				"gtk-media-play",
				Gtk.IconSize.MENU
			)
		self.pause_image = Gtk.Image.new_from_icon_name(
				"gtk-media-pause",
				Gtk.IconSize.MENU
			)
		self.stop_image = Gtk.Image.new_from_icon_name(
				"gtk-media-stop",
				Gtk.IconSize.MENU
			)
		self.update_image = Gtk.Image.new_from_icon_name(
				"gtk-media-update",
				Gtk.IconSize.MENU
			)
		self.playback_button.set_image(self.play_image)
		self.stop_button.set_image(self.stop_image)
		self.update_button.set_image(self.update_image)


		self.playback_button.connect("clicked", self.toggle_player_playback)
		self.stop_button.connect("clicked", self.stop_player)
		self.update_button.connect("clicked", self.update)

		self.draw_area = Gtk.DrawingArea()
		self.draw_area.set_size_request(300,300)

		self.draw_area.connect("realize",self._realized)

		self.hbox = Gtk.Box(spacing=6)
		self.hbox.pack_start(self.playback_button, True, True, 0)
		self.hbox.pack_start(self.stop_button, True, True, 0)
		self.hbox.pack_start(self.update_button, True, True, 0)

		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.vbox)
		self.vbox.pack_start(self.draw_area, True, True, 0)
		self.vbox.pack_start(self.hbox, False, False, 0)

	def toggle_player_playback(self, widget, data=None):

		"""
		Handler for Player's Playback Button (Play/Pause).
		"""

		if self.is_player_active == False and self.player_paused == False:
			self.player.play()
			self.playback_button.set_image(self.pause_image)
			self.is_player_active = True

		elif self.is_player_active == True and self.player_paused == True:
			self.player.play()
			self.playback_button.set_image(self.pause_image)
			self.player_paused = False

		elif self.is_player_active == True and self.player_paused == False:
			self.player.pause()
			self.playback_button.set_image(self.play_image)
			self.player_paused = True
		else:
			pass

	def _key_press_event(self,widget,event):
		keyval = event.keyval
		keyval_name = Gdk.keyval_name(keyval)
		state = event.state
		print(keyval_name)
		if  keyval_name == 'space':
			self.toggle_player_playback(self)
		elif keyval_name == 'Tab':
			self.update(self)
		elif keyval_name == "s":
			self.stop_player(self)
		elif keyval_name == "Escape":
			self.destroy()
		elif keyval_name == "f":
			self.toggle_fullscreen(self)
		elif keyval_name == "Up":
			if self.volume < 100:
				self.volume +=1
				print(self.volume)
				self.player.audio_set_volume(self.volume)
		elif keyval_name == "Down":
			if self.volume > 0:
				self.volume -=1
				print(self.volume)
				self.player.audio_set_volume(self.volume)
		else:
			return False
		return True

	def update(self,widget, data=None):
		self.stop_player(self)
		self.src = get_src_of_rand_video()
		self.set_my_media(self.player, self.vlcInstance, self.src)
		self.player.play()

	def toggle_fullscreen(self, widget, data=None):
		if self.isFullscreen == True:
			self.isFullscreen = False
			self.hbox.show()
			self.set_decorated(True)
			self.unmaximize()
			self.unfullscreen()
			
		elif self.isFullscreen == False: 
			self.isFullscreen = True
			self.set_decorated(False)
			self.hbox.hide()
			self.maximize()
			self.fullscreen()

	def stop_player(self, widget, data=None):
		self.player.stop()
		self.is_player_active = False
		self.playback_button.set_image(self.play_image)

	def set_my_media(self, _player, _instance, _source):
		_media = _instance.media_new(_source)
		_media.get_mrl
		_player.set_media(_media)
		return _player

	def end_reached(self):
		self.update(self)

	def _realized(self, widget, data=None):
		self.vlcInstance = vlc.Instance("--no-xlib")
		self.src = get_src_of_rand_video()

		self.player = self.vlcInstance.media_player_new()
		win_id = widget.get_window().get_xid()
		self.player.set_xwindow(win_id)
		self.player.set_fullscreen(True)
		self.player = self.set_my_media(self.player, self.vlcInstance, self.src)
		self.player.play()
		self.playback_button.set_image(self.pause_image)
		self.is_player_active = True

if __name__ == '__main__': 
		window = ApplicationWindow()
		window.setup_objects_and_events()
		window.show()
		Gtk.main()
		window.player.stop()
		window.vlcInstance.release()





# attatch function to start new video when the current one ends
def end_reached(self):
    src = get_src_of_rand_video()
    set_my_media(Instance, player, src)
    player.play()
    
