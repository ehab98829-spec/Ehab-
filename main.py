import os
from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is Live and Working!"

@app.route('/playlist.m3u')
def get_m3u():
    url = "http://bossposs.xyz:80/get.php?username=98:06:3c:75:c0:72&password=443367897666trytfg&type=m3u_plus&output=ts"
    try:
        r = requests.get(url, timeout=10)
        return Response(r.text, mimetype='application/mpegurl')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # أهم سطرين في كل القصة:
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
