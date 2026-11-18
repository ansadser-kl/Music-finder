import asyncio
import os
import uuid
from flask import Flask, render_template, request, jsonify
from shazamio import Shazam

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30MB
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.webm', '.mp4', '.opus'}

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/recognize', methods=['OPTIONS'])
def api_recognize_options():
    return ('', 204)

def extract_info(data: dict) -> dict:
    track = data.get('track') or {}
    if not track:
        return {'found': False}

    images = track.get('images') or {}
    share = track.get('share') or {}
    sections = track.get('sections') or []

    album = None
    release_date = None
    label = None
    genre = None
    for sec in sections:
        if sec.get('type') == 'SONG':
            meta = sec.get('metadata') or []
            for m in meta:
                title = (m.get('title') or '').lower()
                text = m.get('text')
                if title == 'album':
                    album = text
                elif title in ('released', 'release date'):
                    release_date = text
                elif title == 'label':
                    label = text
    genres = (track.get('genres') or {}).get('primary')

    return {
        'found': True,
        'title': track.get('title'),
        'artist': track.get('subtitle'),
        'coverart': images.get('coverart') or images.get('coverarthq') or share.get('image'),
        'background': images.get('background'),
        'share_url': share.get('href') or track.get('url'),
        'album': album,
        'release_date': release_date,
        'label': label,
        'genre': genre or genres,
        'shazam_url': track.get('url'),
    }

async def recognize_file(path: str) -> dict:
    shazam = Shazam()
    try:
        if hasattr(shazam, 'recognize'):
            result = await shazam.recognize(path)
        elif hasattr(shazam, 'recognize_song'):
            result = await shazam.recognize_song(path)
        else:
            return {'found': False, 'error': 'Recognizer method not available'}
    except Exception as e:
        return {'found': False, 'error': str(e)}
    if not result or not isinstance(result, dict) or not result.get('track'):
        return {'found': False}
    return extract_info(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recognize', methods=['POST'])
def api_recognize():
    if 'file' not in request.files:
        return jsonify({'found': False, 'error': 'No file uploaded'}), 400
    f = request.files['file']
    if not f or f.filename == '':
        return jsonify({'found': False, 'error': 'No file selected'}), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({'found': False, 'error': f'Unsupported file type: {ext}'}), 400

    name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, name)
    try:
        f.save(path)
        result = asyncio.run(recognize_file(path))
        return jsonify(result)
    except Exception as e:
        return jsonify({'found': False, 'error': str(e)}), 500
    finally:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
