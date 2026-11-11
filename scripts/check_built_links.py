#!/usr/bin/env python3
"""Check built local links/anchors, accounting for the RTD /en/latest/ prefix."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and "href" in values:
            self.links.append(values["href"])


def main():
    site = (ROOT / "site").resolve()
    prefix = urlsplit(yaml.safe_load((ROOT / "mkdocs.yml").read_text())["site_url"]).path
    pages = {}
    for path in site.rglob("*.html"):
        page = Page()
        page.feed(path.read_text())
        pages[path] = page
    if not pages:
        raise SystemExit("Build the documentation first")
    failures = []
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            local = unquote(url.path)
            if local.startswith("/"):
                if not local.startswith(prefix):
                    failures.append((str(path.relative_to(site)), link, "outside site prefix"))
                    continue
                target = (site / local[len(prefix):]).resolve()
            else:
                target = (path.parent / local).resolve() if local else path
            if target.is_dir():
                target = target / "index.html"
            if not target.is_relative_to(site) or not target.exists():
                failures.append((str(path.relative_to(site)), link, "missing file"))
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                failures.append((str(path.relative_to(site)), link, "missing anchor"))
    if failures:
        raise SystemExit(str(failures))
    print(f"Built links/anchors checked: {len(pages)} HTML pages, no broken internal links")


if __name__ == "__main__":
    main()
