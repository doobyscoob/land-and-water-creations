"""Normalize known local HTML anchor targets and add explicit canonical URLs."""
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

root = Path(__file__).parent / 'site'
origin = 'https://landandwatercreations.com'
pages = list(root.rglob('*.html'))
routes = {}
for page in pages:
    path = '/' + page.relative_to(root).as_posix()
    route = path[:-5] if not path.endswith('/index.html') else path[:-10]
    route = route or '/'
    routes[path] = route
    routes[route] = route

count = 0
for page in pages:
    path = '/' + page.relative_to(root).as_posix()
    route = routes[path]
    html = page.read_text()
    html = re.sub(r'<link\b(?=[^>]*\brel=[\"\']canonical[\"\'])[^>]*>\s*', '', html, flags=re.I)
    html = re.sub(r'</head>', f'<link rel="canonical" href="{origin}{route}" />\n</head>', html, count=1, flags=re.I)
    def anchor(match):
        global count
        tag = match.group(0)
        def href(m):
            global count
            value = m.group(2)
            if value.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                return m.group(0)
            u = urlsplit(urljoin(origin + route, value))
            if u.hostname not in ('landandwatercreations.com', 'www.landandwatercreations.com') or u.path not in routes:
                return m.group(0)
            target = urlunsplit(('', '', routes[u.path], u.query, u.fragment))
            if target != value:
                count += 1
            return f'href={m.group(1)}{target}{m.group(1)}'
        return re.sub(r'\bhref=([\"\'])(.*?)\1', href, tag, flags=re.I)
    html = re.sub(r'<a\b[^>]*>', anchor, html, flags=re.I)
    page.write_text(html)
print(f'{len(pages)} canonical tags; {count} anchor targets normalized')
