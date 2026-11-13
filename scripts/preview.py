"""Preview the existing static site, including its clean service-page URLs."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit


SITE = Path(__file__).resolve().parents[1] / "site"


class SiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def send_head(self):
        # Discard validators from resources cached before no-store was enabled.
        if "If-Modified-Since" in self.headers:
            del self.headers["If-Modified-Since"]
        url = urlsplit(self.path)
        # This server is development-only. Never run production analytics here,
        # even when the editor uses a hostname not covered by the client guard.
        if url.path == "/js/head":
            content = b"/* Production tracking is disabled in development previews. */\n"
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            return BytesIO(content)

        if url.path.rstrip("/") == "/outdoorliving":
            self.send_response(301)
            self.send_header(
                "Location",
                urlunsplit(("", "", "/outdoor-living", url.query, "")),
            )
            self.end_headers()
            return None

        path = Path(self.translate_path(url.path))
        if not path.exists() and not Path(unquote(url.path)).suffix:
            html_path = path.with_suffix(".html")
            if html_path.is_file():
                self.path = urlunsplit(("", "", url.path + ".html", url.query, ""))
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    print("Serving the static site on port 5000", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 5000), SiteHandler).serve_forever()
