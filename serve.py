"""Local preview of public/. Like Cloudflare, unknown URLs get public/404.html.

    python3 serve.py   # http://localhost:56469
"""

import functools
import http.server
from pathlib import Path

ROOT = Path(__file__).parent / "public"


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        if code != 404:
            return super().send_error(code, message, explain)
        body = (ROOT / "404.html").read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


handler = functools.partial(Handler, directory=ROOT)
http.server.ThreadingHTTPServer(("127.0.0.1", 56469), handler).serve_forever()
