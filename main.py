import os
import requests
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# الروابط الخاصة بك
MASTER_URL = "http://bossposs.xyz:80/get.php?username=98:06:3c:75:c0:72&password=443367897666trytfg&type=m3u_plus&output=ts"
EPG_URL    = "http://bossposs.xyz:80/xmltv.php?username=98:06:3c:75:c0:72&password=443367897666trytfg"
STREAM_ORIGIN = "http://bossposs.xyz:8080"

# هيدرز قوية لفك حظر 469
REAL_HEADERS = {
    'User-Agent': 'IPTVSmartersPlayer/1.6.2 (iPad; iOS 15.1; Scale/2.00)',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

@app.route('/')
def index():
    return "Server is Live - Ehab IPTV"

@app.route('/playlist.m3u')
def playlist():
    try:
        host = request.headers.get('X-Forwarded-Host', request.host)
        # نرسل الهيدرز الحقيقية للسيرفر الأصلي
        r = requests.get(MASTER_URL, headers=REAL_HEADERS, timeout=20)
        r.raise_for_status()
        content = r.text.replace(STREAM_ORIGIN, f'https://{host}/api/proxy')
        return Response(content, content_type='application/x-mpegurl')
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/api/proxy/<path:url_path>')
def proxy(url_path):
    target_url = f"{STREAM_ORIGIN}/{url_path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode()}"
    try:
        # التمويه حتى عند تشغيل القناة
        upstream = requests.get(target_url, headers=REAL_HEADERS, stream=True, timeout=15)
        def generate():
            for chunk in upstream.iter_content(chunk_size=1024 * 64):
                yield chunk
        return Response(stream_with_context(generate()), content_type=upstream.headers.get('Content-Type'))
    except Exception as e:
        return f"Stream Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
