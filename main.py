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
IPTV_HEADERS = {
    'User-Agent': 'IPTVSmarters/1.0.3 (iPad; iPhone; iOS 13.5.1; Scale/2.00)',
}

@app.route('/')
def index():
    return "Ihab IPTV Server is Active on Render!"

def make_playlist(host):
    r = requests.get(MASTER_URL, timeout=20)
    r.raise_for_status()
    # تحويل الروابط لتمر عبر السيرفر الجديد
    return r.text.replace(STREAM_ORIGIN, f'https://{host}/api/proxy')

@app.route('/playlist.m3u')
@app.route('/api/playlist.m3u')
def playlist():
    try:
        # Render يستخدم X-Forwarded-Host للروابط الخارجية
        host = request.headers.get('X-Forwarded-Host', request.host)
        content = make_playlist(host)
        return Response(content, status=200, content_type='application/x-mpegurl')
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/epg.xml')
@app.route('/api/epg')
def epg():
    try:
        upstream = requests.get(EPG_URL, stream=True, timeout=20)
        def generate():
            for chunk in upstream.iter_content(chunk_size=1024 * 64):
                yield chunk
        return Response(stream_with_context(generate()), content_type='application/xml')
    except Exception as e:
        return f"EPG Error: {e}", 500

@app.route('/api/proxy/<path:url_path>')
def proxy(url_path):
    qs = request.query_string.decode()
    target_url = f"{STREAM_ORIGIN}/{url_path}"
    if qs: target_url += f"?{qs}"
    try:
        upstream = requests.get(target_url, headers=IPTV_HEADERS, stream=True, timeout=15)
        def generate():
            for chunk in upstream.iter_content(chunk_size=1024 * 64):
                yield chunk
        return Response(stream_with_context(generate()), content_type=upstream.headers.get('Content-Type'))
    except Exception as e:
        return f"Stream Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
