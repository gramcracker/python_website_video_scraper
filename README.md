# wco_streamer
This is a program I created in order to stream a randomized list of episodes given a predefined list of show titles picked from watchcartoonsonline.com through the VLC media player.
At it's current stage, the player doesn't have any controls, and will only play one episode when run, but the goal is to have it play continuously for a specified amount of time.

## How it works
It takes a specified list of show titles and pics a random episode from a random title in the
list, then streams the episode from the website through vlc.

## Installing
To run this, you must have chromedriver in your path. and you must have vlc, BeautifulSoup,
and selenium installed, as well as python, and an internet connection. Once that is done simply
open a terminal in the containing directory and type:

```
$python wco_streamer

```
It takes a moment to load, but If all works well, vlc should open with an show from the show_title list.