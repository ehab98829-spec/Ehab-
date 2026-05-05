from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/playlist.m3u')
def get_playlist():
    target_url = "http://bossposs.xyz:80/get.php?username=98:06:3c:75:c0:72&password=443367897666trytfg&type=m3u_plus&output=ts" 
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(target_url, headers=headers, timeout=15)
        return Response(r.text, mimetype='application/mpegurl')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/')
def home():
    return "Ihab IPTV Server is Running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
