# Music Finder

Web app + API to upload an audio/music file, identify the song, and show details (title, artist, cover/thumbnail, album, genre, release date, label, and link).

## Features
- Upload audio file (drag & drop or file picker)
- Song recognition using Shazam (via [`shazamio`](https://github.com/shazamio/ShazamIO), no API key required)
- Displays thumbnail/cover art and song metadata
- JSON API endpoint for integration: `POST /api/recognize`

## Project structure
- `app.py` – Flask backend + recognition API
- `templates/index.html` – Web UI
- `static/` – static assets (if needed)
- `uploads/` – temporary upload folder (processed files are deleted after recognition)
- `API.md` – API documentation

## Requirements
- Python 3.10+
- Internet access (for Shazam recognition)

## Setup

```bash
pip install flask shazamio
```

If your environment is externally managed (PEP 668), you may need:

```bash
pip3 install --break-system-packages flask shazamio
```

## Run

```bash
python3 app.py
```

Open: [http://localhost:5000](http://localhost:5000)

By default the app listens on `0.0.0.0:5000`.

## API
See [API.md](API.md) for request/response details and examples.

Quick example:

```bash
curl -X POST http://localhost:5000/api/recognize \
  -F "file=@/path/to/song.mp3"
```

## Notes
- Supported formats: `mp3, wav, m4a, ogg, flac, aac, webm, mp4, opus`
- Max upload size: 30MB
- Recognition quality depends on clip clarity/length and Shazam match availability
