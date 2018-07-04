import bs4
import vlc
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# place show titles here
show_titles = ['']


base_url = 'https://www.watchcartoononline.com/anime/'

my_url = base_url+random.choice(show_titles)
chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options);

# sets the media 
def set_my_media(_instance, _player, _src):
	_Media = _instance.media_new(_src)
	_Media.get_mrl()
	_player.set_media(_Media)

# uses random.choice to pick a random episode from a random title in show_titles[]
def get_src_of_rand_video(_url):
	uClient = uReq(_url) 
	page_soup = soup(uClient.read(), "html.parser")
	uClient.close()
	episodes = page_soup.select("div.cat-eps a.sonra")
	link = random.choice(episodes).get('href')
	print(link)
	#get video source
	driver.get(link)
	iframes = driver.find_elements_by_tag_name('iframe')
	driver.switch_to.frame(1)
	src = driver.find_element_by_id('video-js').find_element_by_tag_name('source').get_attribute('src')
	return src

# set up vlc
Instance = vlc.Instance()
player = Instance.media_player_new()
isFullscreen = True

# attatch function to start new video when the current one ends
# TODO: correct this to call set_my_media() when a show has ended
def end_reached(self):
    src = get_src_of_rand_video(my_url)
    set_my_media(Instance, player, src)
    player.set_fullscreen(isFullscreen)
    player.play()
    
event_manager = player.event_manager() # Attach event to player
event=vlc.EventType()
event_manager.event_attach(event.MediaPlayerEndReached, end_reached)

# main loop
src = get_src_of_rand_video(my_url)
set_my_media(Instance, player, src)
player.set_fullscreen(isFullscreen)
player.play()
while True:
     pass