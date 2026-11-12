"""Preview the existing static site, including its clean service-page URLs."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit


SITE = Path(__file__).resolve().parents[1] / "site"


class SiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def send_head(self):
        url = urlsplit(self.path)
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
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    print("Serving the static site on port 5000", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 5000), SiteHandler).serve_forever()
