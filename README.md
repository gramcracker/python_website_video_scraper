# This no longer works
Because watchcartoonsonline.com is no longer operational, this program will no longer work, but I heve decided to leave this up as an example of how someone could go about using python to scrape and stream content from a similar website.

# wco_streamer
This is a program I created in order to stream a randomized list of episodes given a predefined list of show titles picked from watchcartoonsonline.com through the VLC media player.
At it's current stage, the player doesn't have any controls, and will only play one episode when run.

## How it works
It takes a specified list of show titles and pics a random episode from a random title in the
list, then streams the episode from the website through vlc.

## Installing
Prerequisites: Must have chromedriver in path. Must have vlc, BeautifulSoup,
and selenium installed, as well as python, and an internet connection.

## Running
Once once the Prerequisites are installed, open wco_streamer, and define the show_titles variable with the titles that you would like to watch. If it is having trouble finding the title, find the title on watchcartoonsonline.com, and make sure it matches the title in the url. To run, simply open a terminal in the containing directory and type:

```
$python wco_streamer

```
It takes a moment to load, but If all works well, vlc should open with an episode from the show_title list.
