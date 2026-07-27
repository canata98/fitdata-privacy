#!/usr/bin/env python3
"""Generate blog HTML, sitemap entries, and RSS feeds from content/blog/*.md."""

from __future__ import annotations

import html
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "blog"
BLOG_DIR = ROOT / "blog"
SITE = "https://fitdata.app"

MONTHS_EN = (
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
)
MONTHS_DE = (
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
)

LANG = {
    "en": {
        "overview": "blog-en.html",
        "index": "index.html",
        "blog_nav": "blog-en.html",
        "alt_overview": "blog-de.html",
        "support": "support-en.html",
        "privacy": "privacy-en.html",
        "terms": "terms-en.html",
        "imprint": "imprint-en.html",
        "back_home": "← Back to FitData",
        "back_blog": "← Back to Blog",
        "coming_soon": "New articles coming soon.",
        "read_time": "{n} min read",
        "cta_label": "Get Started",
        "cta_title": "Build your plan<br>in FitData today.",
        "cta_text": "Free to download. Works offline. iPhone &amp; Apple Watch.",
        "app_store_alt": "Download on the App Store",
        "app_store_badge": "assets/Download_on_the_App_Store_Badge_US-UK_RGB_wht_092917.svg",
        "nav_features": "Features",
        "nav_blog": "Blog",
        "nav_faq": "FAQ",
        "nav_support": "Support",
        "nav_privacy": "Privacy",
        "nav_terms": "Terms",
        "nav_imprint": "Imprint",
        "nav_download": "Download",
        "footer_tagline": "WORKOUTS &amp; RUNNING FOR IPHONE &amp; APPLE WATCH",
        "footer_app": "App",
        "footer_legal": "Legal",
        "footer_support": "Support",
        "footer_privacy": "Privacy Policy",
        "footer_terms": "Terms of Use",
        "footer_imprint": "Imprint",
        "footer_rights": "© 2026 FitData. All rights reserved.",
        "footer_made": "Made for athletes everywhere.",
        "og_locale": "en_US",
        "html_lang": "en",
        "feed_title": "FitData Blog",
        "feed_desc": "Tips on workouts, running, and training with FitData.",
        "page_title": "FitData Blog — Workouts, Running &amp; Training Tips",
        "page_desc": (
            "Tips on building workout plans, tracking runs, and getting more "
            "from FitData on iPhone and Apple Watch."
        ),
        "page_h1_sub": "Workouts, running, and training — practical tips from the FitData team.",
    },
    "de": {
        "overview": "blog-de.html",
        "index": "index-de.html",
        "blog_nav": "blog-de.html",
        "alt_overview": "blog-en.html",
        "support": "support.html",
        "privacy": "privacy-de.html",
        "terms": "terms-de.html",
        "imprint": "impressum-de.html",
        "back_home": "← Zurück zu FitData",
        "back_blog": "← Zurück zum Blog",
        "coming_soon": "Neue Artikel folgen in Kürze.",
        "read_time": "{n} Min. Lesezeit",
        "cta_label": "Loslegen",
        "cta_title": "Erstelle deinen Plan<br>heute in FitData.",
        "cta_text": "Kostenlos. Offline nutzbar. iPhone &amp; Apple Watch.",
        "app_store_alt": "Im App Store laden",
        "app_store_badge": "assets/Download_on_the_App_Store_Badge_DE_RGB_wht_092917.svg",
        "nav_features": "Funktionen",
        "nav_blog": "Blog",
        "nav_faq": "Fragen",
        "nav_support": "Support",
        "nav_privacy": "Datenschutz",
        "nav_terms": "AGB",
        "nav_imprint": "Impressum",
        "nav_download": "Download",
        "footer_tagline": "WORKOUTS &amp; LAUFEN FÜR IPHONE &amp; APPLE WATCH",
        "footer_app": "App",
        "footer_legal": "Rechtliches",
        "footer_support": "Support",
        "footer_privacy": "Datenschutz",
        "footer_terms": "Nutzungsbedingungen",
        "footer_imprint": "Impressum",
        "footer_rights": "© 2026 FitData. Alle Rechte vorbehalten.",
        "footer_made": "Für Sportler überall gemacht.",
        "og_locale": "de_DE",
        "html_lang": "de",
        "feed_title": "FitData Blog",
        "feed_desc": "Tipps zu Workouts, Laufen und Training mit FitData.",
        "page_title": "FitData Blog — Workouts, Laufen &amp; Trainingstipps",
        "page_desc": (
            "Tipps zu Trainingsplänen, Lauftracking und mehr aus FitData "
            "für iPhone und Apple Watch."
        ),
        "page_h1_sub": "Workouts, Laufen und Training — praktische Tipps vom FitData-Team.",
    },
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        raise ValueError("Missing frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("Unclosed frontmatter")
    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        meta[key.strip()] = value
    return meta, body


def parse_bool(value: str) -> bool:
    return value.lower() in ("true", "yes", "1")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def format_date(d: date, lang: str) -> str:
    if lang == "de":
        return f"{d.day}. {MONTHS_DE[d.month - 1]} {d.year}"
    return f"{MONTHS_EN[d.month - 1]} {d.day}, {d.year}"


def markdown_to_html(md: str) -> str:
    lines = md.strip().splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("## "):
            out.append(f"  <h2>{html.escape(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"    <li>{html.escape(lines[i][2:].strip())}</li>")
                i += 1
            out.append("  <ul>")
            out.extend(items)
            out.append("  </ul>")
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("## ") and not lines[i].startswith("- "):
            para.append(lines[i].strip())
            i += 1
        out.append(f"  <p>{html.escape(' '.join(para))}</p>")
    return "\n\n".join(out)


def load_posts() -> list[dict]:
    posts: list[dict] = []
    for path in sorted(CONTENT_DIR.glob("*.md")):
        if path.name.startswith("_") or path.name.lower() == "readme.md":
            continue
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        lang = meta.get("lang", "")
        if lang not in LANG:
            print(f"Skip {path.name}: unknown lang {lang!r}", file=sys.stderr)
            continue
        slug = meta["slug"]
        posts.append(
            {
                "path": path,
                "slug": slug,
                "lang": lang,
                "title": meta["title"],
                "description": meta["description"],
                "date": parse_date(meta["date"]),
                "category": meta["category"],
                "read_time": int(meta.get("readTime", meta.get("read_time", "5"))),
                "thumbnail": meta["thumbnail"],
                "thumbnail_fallback": meta.get("thumbnailFallback", meta.get("thumbnail_fallback", "")),
                "hero": meta["hero"],
                "hero_fallback": meta.get("heroFallback", meta.get("hero_fallback", "")),
                "hero_alt": meta.get("heroAlt", meta.get("hero_alt", meta["title"])),
                "published": parse_bool(meta.get("published", "false")),
                "author": meta.get("author", ""),
                "card_teaser": meta.get("cardTeaser", meta.get("card_teaser", meta["description"])),
                "body_html": markdown_to_html(body),
            }
        )
    return posts


def article_filename(slug: str, lang: str) -> str:
    return f"{slug}-{lang}.html"


def article_url(slug: str, lang: str) -> str:
    return f"{SITE}/blog/{article_filename(slug, lang)}"


def replace_block(text: str, start: str, end: str, content: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = start + "\n" + content + "\n  " + end
    if not pattern.search(text):
        raise ValueError(f"Markers not found: {start} / {end}")
    return pattern.sub(replacement, text, count=1)


def render_card(post: dict, cfg: dict) -> str:
    prefix = "" if post["lang"] == "en" else ""
    assets = "assets" if post["lang"] == "en" else "assets"
    href = f"blog/{article_filename(post['slug'], post['lang'])}"
    d = post["date"]
    cfg_lang = LANG[post["lang"]]
    return f"""    <a class="blog-card" href="{href}">
      <div class="blog-card-thumb">
        <picture>
          <source srcset="{post['thumbnail']}" type="image/webp" />
          <img src="{post['thumbnail_fallback']}" alt="{html.escape(post['hero_alt'])}" width="800" height="450" loading="lazy" decoding="async" />
        </picture>
      </div>
      <div class="blog-card-body">
        <span class="blog-category">{html.escape(post['category'])}</span>
        <h2>{html.escape(post['title'])}</h2>
        <p>{html.escape(post['card_teaser'])}</p>
        <div class="blog-meta">
          <time datetime="{d.isoformat()}">{format_date(d, post['lang'])}</time>
          <span>{cfg_lang['read_time'].format(n=post['read_time'])}</span>
        </div>
      </div>
    </a>"""


def render_overview_grid(posts: list[dict], lang: str) -> str:
    cfg = LANG[lang]
    published = sorted(
        [p for p in posts if p["lang"] == lang and p["published"]],
        key=lambda p: p["date"],
        reverse=True,
    )
    if not published:
        return f'  <p class="blog-coming-soon" style="text-align:center;font-size:17px;color:var(--text-2);padding:48px 0;">{cfg["coming_soon"]}</p>'
    cards = "\n".join(render_card(p, cfg) for p in published)
    return f'  <div class="blog-grid">\n{cards}\n  </div>'


def render_article(post: dict, alt_lang_post: dict | None) -> str:
    lang = post["lang"]
    cfg = LANG[lang]
    slug = post["slug"]
    filename = article_filename(slug, lang)
    alt_lang = "de" if lang == "en" else "en"
    alt_filename = article_filename(slug, alt_lang)
    d = post["date"]
    hero_fb = post["hero_fallback"] or post["hero"].replace(".webp", ".jpg")
    og_image = f"{SITE}/{hero_fb.lstrip('/')}"
    canonical = article_url(slug, lang)
    read_label = cfg["read_time"].format(n=post["read_time"])

    has_alt = alt_lang_post is not None and alt_lang_post["published"]
    alt_href = alt_filename if has_alt else f"../{cfg['alt_overview']}"
    alt_url = article_url(slug, alt_lang) if has_alt else f"{SITE}/{cfg['alt_overview']}"
    x_default = article_url(slug, "en") if lang == "en" or has_alt else canonical

    if lang == "en":
        en_nav = f'<a class="active" href="{filename}">EN</a>'
        de_nav = f'<a href="{alt_href}" data-alt-href="{alt_href}">DE</a>'
    else:
        en_href = alt_filename if has_alt else "../blog-en.html"
        en_nav = f'<a href="{en_href}">EN</a>'
        de_nav = f'<a class="active" href="{filename}">DE</a>'

    return f"""<!DOCTYPE html>
<html lang="{cfg['html_lang']}" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(post['title'])} — FitData Blog</title>
  <meta name="description" content="{html.escape(post['description'])}" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="{lang}" href="{canonical}" />
  <link rel="alternate" hreflang="{alt_lang}" href="{alt_url}" />
  <link rel="alternate" hreflang="x-default" href="{x_default}" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="{cfg['og_locale']}" />
  <meta property="og:title" content="{html.escape(post['title'])}" />
  <meta property="og:description" content="{html.escape(post['description'])}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(post['title'])}" />
  <meta name="twitter:description" content="{html.escape(post['description'])}" />
  <meta name="twitter:image" content="{og_image}" />
  <link rel="icon" type="image/png" href="../assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" />
  <link rel="preload" href="../assets/fonts/gabarito-400.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="../assets/fonts/atkinson-400.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="../assets/site.css" />
  <script src="../analytics-consent.js" defer></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": {json_str(post['title'])},
    "description": {json_str(post['description'])},
    "image": "{og_image}",
    "datePublished": "{d.isoformat()}",
    "author": {{ "@type": "Organization", "name": "FitData" }},
    "publisher": {{ "@type": "Organization", "name": "FitData", "url": "{SITE}" }},
    "mainEntityOfPage": "{canonical}",
    "inLanguage": "{lang}"
  }}
  </script>
</head>
<body>

<nav>
  <a class="nav-logo" href="../{cfg['index']}">
    <img src="../assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" alt="FitData" width="36" height="36" />
    <span>FitData</span>
  </a>
  <div class="nav-links">
    <a href="../{cfg['index']}#features">{cfg['nav_features']}</a>
    <a href="../{cfg['blog_nav']}">{cfg['nav_blog']}</a>
    <a href="../{cfg['index']}#faq">{cfg['nav_faq']}</a>
    <a href="../{cfg['support']}">{cfg['nav_support']}</a>
    <a href="../{cfg['privacy']}">{cfg['nav_privacy']}</a>
    <a href="../{cfg['terms']}">{cfg['nav_terms']}</a>
    <a href="../{cfg['imprint']}">{cfg['nav_imprint']}</a>
    <div class="nav-lang">
      {en_nav}
      {de_nav}
    </div>
    <a class="btn-nav" href="https://apps.apple.com/us/app/fitdata-workout-app/id6740706351" target="_blank" rel="noopener">{cfg['nav_download']}</a>
  </div>
</nav>

<article class="article-wrap">
  <a class="back" href="../{cfg['overview']}">{cfg['back_blog']}</a>

  <div class="article-meta">
    <span class="blog-category">{html.escape(post['category'])}</span>
    <time datetime="{d.isoformat()}">{format_date(d, lang)}</time>
    <span>{read_label}</span>
  </div>

  <h1>{html.escape(post['title'])}</h1>

  <div class="article-hero">
    <picture>
      <source srcset="../{post['hero']}" type="image/webp" />
      <img src="../{hero_fb}" alt="{html.escape(post['hero_alt'])}" width="1200" height="675" loading="eager" decoding="async" />
    </picture>
  </div>

{post['body_html']}

  <p class="article-author">{html.escape(post['author'])}</p>
</article>

<div class="cta-sec">
  <span class="label-tag">{cfg['cta_label']}</span>
  <h2>{cfg['cta_title']}</h2>
  <p>{cfg['cta_text']}</p>
  <div class="cta-btns">
    <a class="btn-cta-primary" href="https://apps.apple.com/us/app/fitdata-workout-app/id6740706351" target="_blank" rel="noopener">
      <img src="../{cfg['app_store_badge']}" alt="{cfg['app_store_alt']}" width="180" height="52" />
    </a>
  </div>
</div>

<footer>
  <div class="ft">
    <div class="fb">
      <a class="nav-logo" href="../{cfg['index']}">
        <img src="../assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" alt="FitData" width="36" height="36" />
        <span>FitData</span>
      </a>
      <p>{cfg['footer_tagline']}</p>
    </div>
    <div class="fcol"><h4>{cfg['footer_app']}</h4><a href="https://apps.apple.com/us/app/fitdata-workout-app/id6740706351" target="_blank" rel="noopener">{cfg['nav_download']}</a><a href="../{cfg['index']}#features">{cfg['nav_features']}</a><a href="../{cfg['blog_nav']}">{cfg['nav_blog']}</a><a href="../{cfg['index']}#faq">{cfg['nav_faq']}</a></div>
    <div class="fcol"><h4>{cfg['footer_legal']}</h4><a href="../{cfg['privacy']}">{cfg['footer_privacy']}</a><a href="../{cfg['terms']}">{cfg['footer_terms']}</a><a href="../{cfg['imprint']}">{cfg['footer_imprint']}</a></div>
    <div class="fcol"><h4>{cfg['footer_support']}</h4><a href="../{cfg['support']}">{cfg['nav_support']}</a></div>
  </div>
  <div class="fbot">
    <p>{cfg['footer_rights']}</p>
    <p>{cfg['footer_made']}</p>
  </div>
</footer>
<script src="../assets/nav.js" defer></script>
</body>
</html>
"""


def json_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_sitemap_entries(posts: list[dict]) -> str:
    slugs = sorted({p["slug"] for p in posts if p["published"]})
    lines: list[str] = []
    for slug in slugs:
        en = next((p for p in posts if p["slug"] == slug and p["lang"] == "en" and p["published"]), None)
        de = next((p for p in posts if p["slug"] == slug and p["lang"] == "de" and p["published"]), None)
        if en:
            lines.extend(sitemap_url_block(f"blog/{article_filename(slug, 'en')}", slug, bool(de)))
        if de:
            lines.extend(sitemap_url_block(f"blog/{article_filename(slug, 'de')}", slug, bool(en)))
    return "\n".join(lines)


def sitemap_url_block(path: str, slug: str, has_pair: bool) -> list[str]:
    loc = f"{SITE}/{path}"
    en_url = f"{SITE}/blog/{slug}-en.html"
    de_url = f"{SITE}/blog/{slug}-de.html"
    if not has_pair:
        en_url = loc if path.endswith("-en.html") else en_url
        de_url = loc if path.endswith("-de.html") else de_url
    return [
        "  <url>",
        f"    <loc>{loc}</loc>",
        f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url if has_pair or path.endswith("-en.html") else loc}"/>',
        f'    <xhtml:link rel="alternate" hreflang="de" href="{de_url if has_pair or path.endswith("-de.html") else loc}"/>',
        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>',
        "  </url>",
    ]


def render_feed_items(posts: list[dict], lang: str) -> str:
    cfg = LANG[lang]
    published = sorted(
        [p for p in posts if p["lang"] == lang and p["published"]],
        key=lambda p: p["date"],
        reverse=True,
    )
    items = []
    for p in published:
        url = article_url(p["slug"], lang)
        hero = p["hero_fallback"] or p["hero"]
        items.append(
            f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{p['date'].strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>
      <description>{html.escape(p['description'])}</description>
    </item>"""
        )
    feed_path = f"feed-{lang}.xml"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{cfg['feed_title']}</title>
    <link>{SITE}/{cfg['overview']}</link>
    <description>{cfg['feed_desc']}</description>
    <language>{lang}</language>
    <atom:link href="{SITE}/{feed_path}" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""


def update_overview(lang: str, grid_html: str) -> None:
    path = ROOT / LANG[lang]["overview"]
    text = path.read_text(encoding="utf-8")
    text = replace_block(text, "<!-- BLOG-GENERATED-START -->", "<!-- BLOG-GENERATED-END -->", grid_html)
    text = text.replace('<script src="assets/blog-dev.js" defer></script>\n', "")
    text = re.sub(
        r'  <script>document\.documentElement\.dataset\.env=.*?</script>\n',
        "",
        text,
    )
    path.write_text(text, encoding="utf-8")


def update_sitemap(posts: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    entries = render_sitemap_entries(posts)
    if "<!-- BLOG-SITEMAP-START -->" in text:
        text = replace_block(text, "<!-- BLOG-SITEMAP-START -->", "<!-- BLOG-SITEMAP-END -->", entries)
    else:
        insert = f"\n  <!-- BLOG-SITEMAP-START -->\n{entries}\n  <!-- BLOG-SITEMAP-END -->\n"
        text = text.replace("</urlset>", insert + "</urlset>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    posts = load_posts()
    by_slug_lang = {(p["slug"], p["lang"]): p for p in posts}

    BLOG_DIR.mkdir(exist_ok=True)

    # Remove generated articles no longer published
    published_files = {
        article_filename(p["slug"], p["lang"])
        for p in posts
        if p["published"]
    }
    for html_file in BLOG_DIR.glob("*-en.html"):
        if html_file.name not in published_files:
            html_file.unlink(missing_ok=True)
    for html_file in BLOG_DIR.glob("*-de.html"):
        if html_file.name not in published_files:
            html_file.unlink(missing_ok=True)

    for post in posts:
        if not post["published"]:
            continue
        alt = by_slug_lang.get((post["slug"], "de" if post["lang"] == "en" else "en"))
        article = render_article(post, alt if alt and alt["published"] else None)
        out = BLOG_DIR / article_filename(post["slug"], post["lang"])
        out.write_text(article, encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")

    for lang in ("en", "de"):
        grid = render_overview_grid(posts, lang)
        update_overview(lang, grid)
        print(f"Updated {LANG[lang]['overview']}")

    update_sitemap(posts)
    print("Updated sitemap.xml")

    for lang in ("en", "de"):
        feed = render_feed_items(posts, lang)
        (ROOT / f"feed-{lang}.xml").write_text(feed, encoding="utf-8")
        print(f"Updated feed-{lang}.xml")

    print(f"Done — {sum(1 for p in posts if p['published'])} published article(s).")


if __name__ == "__main__":
    main()
