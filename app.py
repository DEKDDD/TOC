"""Dependency-free WSGI application; run locally with python app.py."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from wsgiref.simple_server import make_server, WSGIRequestHandler
from masking import mask_text

ROOT = Path(__file__).parent
MAX_BYTES = 1_000_000
MAX_CHARS = 100_000


def application(environ, start_response):
    def respond(status, data, content_type="application/json; charset=utf-8"):
        body = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode("utf-8")
        start_response(status, [("Content-Type", content_type), ("Content-Length", str(len(body))),
                                ("Cache-Control", "no-store"), ("X-Content-Type-Options", "nosniff"),
                                ("Referrer-Policy", "no-referrer"),
                                ("Content-Security-Policy", "default-src 'self'; script-src 'self' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")])
        return [body]

    path, method = environ.get("PATH_INFO", "/"), environ.get("REQUEST_METHOD", "GET")
    assets = {"/": ("index.html", "text/html; charset=utf-8"),
              
              "/app.js": ("app.js", "text/javascript; charset=utf-8")}
    if method == "GET" and path in assets:
        filename, content_type = assets[path]
        return respond("200 OK", (ROOT / "static" / filename).read_bytes(), content_type)
    if method == "GET" and path == "/api/config":
        url = os.environ.get("SOURCE_CODE_URL", "")
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parsed.path.strip("/").split("/")) < 2:
            url = ""
        return respond("200 OK", {"source_url": url})
    if path != "/api/mask":
        return respond("404 Not Found", {"error": "ไม่พบหน้าที่ร้องขอ"})
    if method != "POST":
        return respond("405 Method Not Allowed", {"error": "ใช้ POST สำหรับเซ็นเซอร์ข้อความ"})
    if environ.get("CONTENT_TYPE", "").split(";", 1)[0].strip().lower() != "application/json":
        return respond("415 Unsupported Media Type", {"error": "กรุณาส่งข้อมูลแบบ JSON"})
    try:
        size = int(environ.get("CONTENT_LENGTH") or "0")
    except ValueError:
        return respond("400 Bad Request", {"error": "ขนาดข้อมูลไม่ถูกต้อง"})
    if size < 0 or size > MAX_BYTES:
        return respond("413 Payload Too Large", {"error": "ข้อมูลมีขนาดใหญ่เกินกำหนด"})
    try:
        payload = json.loads(environ["wsgi.input"].read(size).decode("utf-8"))
    except (ValueError, UnicodeError):
        return respond("400 Bad Request", {"error": "ข้อมูล JSON ไม่ถูกต้อง"})
    if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
        return respond("400 Bad Request", {"error": "text ต้องเป็นข้อความ"})
    if len(payload["text"]) > MAX_CHARS:
        return respond("413 Payload Too Large", {"error": "รองรับข้อความไม่เกิน 100,000 ตัวอักษร"})
    return respond("200 OK", mask_text(payload["text"]))


class QuietHandler(WSGIRequestHandler):
    # Do not write request paths or submitted content into local access logs.
    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "8000"))
    print(f"PDPA app running at http://{host}:{port} (Ctrl+C to stop)")
    with make_server(host, port, application, handler_class=QuietHandler) as server:
        server.serve_forever()
