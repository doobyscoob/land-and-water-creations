import re, subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.tags = []; self.feed(html)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

root = Path(__file__).parent
pages = list((root/'site').rglob('*.html'))
base = 'origin/seo/water-features-orangedale-pond'
for p in pages:
    rel = p.relative_to(root).as_posix()
    before = Page(subprocess.check_output(['git','show',f'{base}:{rel}'], text=True))
    after = Page(p.read_text())
    canon = [a['href'] for t,a in after.tags if t=='link' and a.get('rel')=='canonical']
    expected = '/' + p.relative_to(root/'site').as_posix()
    expected = expected[:-10] if expected.endswith('/index.html') else expected[:-5]
    assert canon == ['https://landandwatercreations.com' + (expected or '/')], (p,canon)
    # All non-anchor attributes other than canonical are byte-value equivalent.
    def stable(page):
        return [(t,a) for t,a in page.tags if t!='a' and not(t=='link' and a.get('rel')=='canonical')]
    assert stable(before) == stable(after), f'Form, script, styling or other attribute changed: {p}'
    for t,a in after.tags:
        if t=='a' and a.get('href','').startswith('/') and not a['href'].startswith('//'):
            path = urlsplit(a['href']).path
            if path.endswith('.html'): raise AssertionError((p,path))
            assert (root/'site'/path.lstrip('/')).is_file() or (root/'site'/(path.lstrip('/')+'.html')).is_file() or path=='/', (p,path)
urls = [e.text for e in ET.parse(root/'site/sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==len(set(urls))==27
print(f'PASS: {len(pages)} canonical tags; internal routes exist; form/script/style attributes preserved; 27 unique sitemap URLs')
