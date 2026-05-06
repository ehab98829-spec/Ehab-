import os
from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Koyeb Server is Active!"

@app.route('/playlist.m3u')
def get_playlist():
    target_url = "http://bossposs.xyz:80/get.php?username=98:06:3c:75:c0:72&password=443367897666trytfg&type=m3u_plus&output=ts"
    try:
        r = requests.get(target_url, timeout=10)
        return Response(r.text, mimetype='application/mpegurl')
    except:
        return "Error", 500

if __name__ == "__main__":
    # Koyeb بيستخدم بورت 8080 تلقائياً
    app.run(host='0.0.0.0', port=8080)
