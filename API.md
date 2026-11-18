# Music Finder API Documentation

Base URL (local): `http://localhost:5000`

This API identifies a song from an uploaded audio file and returns metadata (title, artist, cover/thumbnail, album, etc.) using Shazam recognition via `shazamio`.

## Endpoints

### `GET /`
Serves the web UI for uploading and identifying songs.

**Response:** `200 OK` (HTML page)

---

### `POST /api/recognize`
Recognize a song from an uploaded audio/music file.

#### Request
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Body field:**
  - `file` (required): audio file to identify

#### Supported formats
`mp3`, `wav`, `m4a`, `ogg`, `flac`, `aac`, `webm`, `mp4`, `opus`

#### Limits
- Max upload size: **30 MB**

#### cURL example
```bash
curl -X POST http://localhost:5000/api/recognize \
  -F "file=@/path/to/song.mp3"
```

#### JavaScript (fetch) example
```js
const form = new FormData();
form.append("file", fileInput.files[0]); // <input type="file" />

const res = await fetch("http://localhost:5000/api/recognize", {
  method: "POST",
  body: form,
});

const data = await res.json();
console.log(data);
```

#### Python example
```python
import requests

with open("song.mp3", "rb") as f:
    response = requests.post(
        "http://localhost:5000/api/recognize",
        files={"file": f},
        timeout=60,
    )

print(response.json())
```

---

## Responses

### Success (song found)
**Status:** `200 OK`

```json
{
  "found": true,
  "title": "Blinding Lights",
  "artist": "The Weeknd",
  "coverart": "https://...",
  "background": "https://...",
  "share_url": "https://www.shazam.com/track/...",
  "album": "After Hours",
  "release_date": "2019",
  "label": "Republic Records",
  "genre": "Pop",
  "shazam_url": "https://www.shazam.com/track/..."
}
```

#### Fields
| Field | Type | Description |
|---|---|---|
| `found` | boolean | `true` when a matching song is identified |
| `title` | string \| null | Song title |
| `artist` | string \| null | Artist/subtitle |
| `coverart` | string \| null | Cover/thumbnail image URL |
| `background` | string \| null | Background image URL (if available) |
| `share_url` | string \| null | Share/song page URL |
| `album` | string \| null | Album name (if available) |
| `release_date` | string \| null | Release date/year (if available) |
| `label` | string \| null | Record label (if available) |
| `genre` | string \| null | Primary genre (if available) |
| `shazam_url` | string \| null | Shazam track URL (if available) |

### Not found / recognition failure
**Status:** `200 OK` (or error status depending on case)

```json
{
  "found": false
}
```

or

```json
{
  "found": false,
  "error": "Song not found. Try a clearer/longer audio clip."
}
```

### Client/server errors
Examples:
- `400 Bad Request` – missing file, empty filename, unsupported file type
- `413 Request Entity Too Large` – file exceeds size limit (Flask max content length)
- `500 Internal Server Error` – unexpected processing error

Example:
```json
{
  "found": false,
  "error": "No file uploaded"
}
```

---

## CORS
The API includes permissive CORS headers for browser-based clients:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

`OPTIONS /api/recognize` is supported for preflight requests.

---

## Notes
- Recognition quality depends on audio clarity, length, and Shazam match availability.
- Internet access is required for recognition requests.
- Uploaded files are stored temporarily and deleted after processing.
