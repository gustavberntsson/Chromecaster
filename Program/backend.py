from flask import Flask, jsonify
from pychromecast import Chromecast

app = Flask(__name__)

def find_chromecast():
    chromecasts = Chromecast.get_chromecasts()
    if chromecasts:
        return chromecasts[0]
    return None

@app.route('/play/<filename>')
def play_media(filename):
    cast = find_chromecast()
    if cast:
        media_url = f"http://din_server_ip:5000/media/{filename}"
        cast.media_controller.play_media(media_url, 'video/mp4')
        return jsonify({"status": "playing"})
    return jsonify({"error": "Ingen Chromecast hittades"})

@app.route('/media/<filename>')
def serve_video(filename):
    # Returnera den faktiska videofilen
    return send_file(os.path.join(MEDIA_FOLDER, filename))

@app.route('/subtitles/<filename>')
def serve_subtitles(filename):
    # Returnera den faktiska undertextsfilen
    return send_file(os.path.join(SUBTITLES_FOLDER, filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)