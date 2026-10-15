#!/usr/bin/env python3
"""Check local links, bilingual Matchday pages and shared app navigation.

The blog regeneration check uses a disposable directory; source files are read-only.
No network access, package installation or deployment is performed.
"""
from contextlib import redirect_stdout
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self, path=None, content=None):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.images, self.scripts = [], set(), [], []
        self.lang, self.h1, self.switch = None, 0, 0
        self.canonical, self.languages, self.social_images = [], {}, []
        self.redirect = False
        self.region = None
        self.menus = {"nav": [], "footer": []}
        self.feed(path.read_text(encoding="utf-8") if content is None else content)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag in self.menus:
            self.region = tag
        if tag == "a" and self.region is not None:
            self.menus[self.region].append((data.get("href", ""), "data-app-switch" in data))
        if tag == "html":
            self.lang = data.get("lang")
        if tag == "h1":
            self.h1 += 1
        if "id" in data:
            self.ids.add(data["id"])
        if "data-app-switch" in data:
            self.switch += 1
        if tag == "a" and data.get("href"):
            self.refs.append(data["href"])
        if tag in ("img", "script", "source") and data.get("src"):
            self.refs.append(data["src"])
        if tag == "img":
            self.images.append(data)
        if tag == "script":
            self.scripts.append(data)
        if tag == "meta" and data.get("http-equiv", "").lower() == "refresh":
            self.redirect = True
        if tag == "meta" and data.get("property") == "og:image":
            self.social_images.append(data.get("content", ""))
        if tag == "link":
            if data.get("rel") in ("stylesheet", "icon", "preload"):
                self.refs.append(data["href"])
            if data.get("rel") == "canonical":
                self.canonical.append(data["href"])
            if data.get("hreflang"):
                self.languages[data["hreflang"]] = data["href"]


    def handle_endtag(self, tag):
        if tag == self.region:
            self.region = None


def app_switch_follows_imprint(page):
    for links in page.menus.values():
        positions = [index for index, (_, switch) in enumerate(links) if switch]
        if len(positions) != 1 or positions[0] == 0:
            return False
        previous = urlsplit(links[positions[0] - 1][0]).path
        if not previous.endswith(("impressum-de.html", "imprint-en.html")):
            return False
    return True


def matchday_sitemap(path):
    root = ET.parse(path).getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [element.text for element in root.findall("s:url/s:loc", ns)]
    assert len(locations) == len(set(locations)), "Duplicate sitemap URLs"
    return {url for url in locations if "/matchdayxi/" in url}


def check_blog_rebuild():
    import build_blog

    posts = build_blog.load_posts()
    for post in posts:
        rendered = build_blog.render_article(post, None)
        expected = "index-de.html" if post["lang"] == "de" else "index.html"
        assert rendered.count("data-app-switch") == 2, "Generated article loses app switch"
        assert app_switch_follows_imprint(Page(content=rendered)), "Generated article moves app switch away from imprint"
        assert rendered.count(f'../matchdayxi/{expected}') == 2, "Wrong article app language"
    before = matchday_sitemap(ROOT / "sitemap.xml")
    original_root, original_blog = build_blog.ROOT, build_blog.BLOG_DIR
    with TemporaryDirectory(prefix="matchday-blog-check-") as directory:
        temporary = Path(directory)
        for name in ("blog-en.html", "blog-de.html", "sitemap.xml"):
            shutil.copy2(ROOT / name, temporary / name)
        build_blog.ROOT, build_blog.BLOG_DIR = temporary, temporary / "blog"
        try:
            with redirect_stdout(StringIO()):
                build_blog.main()
            assert matchday_sitemap(temporary / "sitemap.xml") == before, "Blog build changes Matchday sitemap entries"
            for name in ("blog-en.html", "blog-de.html"):
                assert Page(temporary / name).switch == 2, "Blog overview loses app switch"
        finally:
            build_blog.ROOT, build_blog.BLOG_DIR = original_root, original_blog


def main():
    paths = [*ROOT.glob("*.html"), *(ROOT / "blog").glob("*.html"), *(ROOT / "matchdayxi").glob("*.html")]
    pages = {path.resolve(): Page(path) for path in paths}
    failures, checked = [], 0
    for path, page in pages.items():
        for reference in page.refs:
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path.startswith("/"):
                target = ROOT / unquote(parsed.path).lstrip("/")
            else:
                target = path.parent / unquote(parsed.path) if parsed.path else path
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            checked += 1
            if not target.exists():
                failures.append(f"{path.relative_to(ROOT)}: missing {reference}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                failures.append(f"{path.relative_to(ROOT)}: missing anchor {reference}")
        if page.switch < 2 and not page.redirect:
            failures.append(f"{path.relative_to(ROOT)}: missing navigation/footer app switches")
        if not page.redirect and not app_switch_follows_imprint(page):
            failures.append(f"{path.relative_to(ROOT)}: app switch must follow imprint in navigation and footer")
        if path.parent.name != "matchdayxi":
            continue
        if page.lang not in ("de", "en") or page.h1 != 1:
            failures.append(f"{path.name}: invalid language or primary heading")
        if set(page.languages) != {"de", "en", "x-default"}:
            failures.append(f"{path.name}: incomplete language alternatives")
        if len(page.canonical) != 1 or "/matchdayxi/" not in page.canonical[0]:
            failures.append(f"{path.name}: invalid canonical")
        for image_url in page.social_images:
            if not (ROOT / urlsplit(image_url).path.lstrip("/")).exists():
                failures.append(f"{path.name}: missing social preview image")
        if any("analytics" in script.get("src", "") for script in page.scripts):
            failures.append(f"{path.name}: unexpected website analytics")
        if any("alt" not in image for image in page.images):
            failures.append(f"{path.name}: missing image alternative")
        if any("blog" in ref or "apps.apple.com" in ref for ref in page.refs):
            failures.append(f"{path.name}: unexpected blog or download link")
    if len(matchday_sitemap(ROOT / "sitemap.xml")) != 10:
        failures.append("Expected ten Matchday sitemap entries")
    if failures:
        raise SystemExit("\n".join(failures))
    check_blog_rebuild()
    print(f"PASS: {len(pages)} pages; {checked} local references; Matchday SEO/languages/assets; shared app switches; isolated blog regeneration.")


if __name__ == "__main__":
    main()
