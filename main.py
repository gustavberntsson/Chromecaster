# Python backend exempel
from flask import Flask
from pychromecast import Chromecast

app = Flask(__name__)

def find_chromecast():
    chromecasts = pychromecast.get_chromecasts()
    if chromecasts:
        return chromecasts[0]
    return None

@app.route('/play/<filename>')
def play_media(filename):
    cast = find_chromecast()
    if cast:
        media_url = f"http://your_server/{filename}"
        cast.media_controller.play_media(media_url, 'video/mp4')
        return {"status": "playing"}
    return {"error": "No Chromecast found"}