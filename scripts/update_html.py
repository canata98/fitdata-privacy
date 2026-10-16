#!/usr/bin/env python3
"""Update FitData HTML pages: shared CSS, nav, SEO, performance."""

import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEAD_ASSETS = '''  <link rel="icon" type="image/png" href="{prefix}assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" />
  <link rel="preload" href="{prefix}assets/fonts/gabarito-400.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{prefix}assets/fonts/atkinson-400.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="{prefix}assets/site.css" />
  <script src="{prefix}analytics-consent.js" defer></script>'''

SCRIPTS = '''<script src="{prefix}assets/nav.js" defer></script>'''

# SEO configs per page
PAGES_SEO = {
    'index.html': {
        'lang': 'en', 'title': 'FitData — Progress, made visible',
        'desc': 'Plan workouts and structured runs, log food and macros, and follow your progress. FitData for iPhone, iPhone Duo and Apple Watch.',
        'canonical': 'https://fitdata.app/index.html',
        'href_en': 'https://fitdata.app/index.html', 'href_de': 'https://fitdata.app/index-de.html',
        'og_locale': 'en_US', 'prefix': '',
    },
    'index-de.html': {
        'lang': 'de', 'title': 'FitData — Fortschritt sichtbar machen',
        'desc': 'Plane Trainings und strukturierte Läufe, erfasse Mahlzeiten und Makros und verfolge deinen Fortschritt. FitData für iPhone, iPhone Duo und Apple Watch.',
        'canonical': 'https://fitdata.app/index-de.html',
        'href_en': 'https://fitdata.app/index.html', 'href_de': 'https://fitdata.app/index-de.html',
        'og_locale': 'de_DE', 'prefix': '',
    },
    'support-en.html': {
        'lang': 'en', 'title': 'FitData — Help & Support',
        'desc': 'Get help with FitData — FAQs, troubleshooting, and direct support for workouts, running, and Apple Watch.',
        'canonical': 'https://fitdata.app/support-en.html',
        'href_en': 'https://fitdata.app/support-en.html', 'href_de': 'https://fitdata.app/support.html',
        'og_locale': 'en_US', 'prefix': '',
    },
    'support.html': {
        'lang': 'de', 'title': 'FitData — Hilfe & Support',
        'desc': 'Hilfe zu FitData — FAQ, Fehlerbehebung und direkter Support für Workouts, Laufen und Apple Watch.',
        'canonical': 'https://fitdata.app/support.html',
        'href_en': 'https://fitdata.app/support-en.html', 'href_de': 'https://fitdata.app/support.html',
        'og_locale': 'de_DE', 'prefix': '',
    },
    'privacy-en.html': {
        'lang': 'en', 'title': 'FitData — Privacy Policy',
        'desc': 'FitData Privacy Policy — how we collect, use, and protect your workout and health data.',
        'canonical': 'https://fitdata.app/privacy-en.html',
        'href_en': 'https://fitdata.app/privacy-en.html', 'href_de': 'https://fitdata.app/privacy-de.html',
        'og_locale': 'en_US', 'prefix': '',
    },
    'privacy-de.html': {
        'lang': 'de', 'title': 'FitData — Datenschutzerklärung',
        'desc': 'FitData Datenschutzerklärung — wie wir deine Trainings- und Gesundheitsdaten erheben, nutzen und schützen.',
        'canonical': 'https://fitdata.app/privacy-de.html',
        'href_en': 'https://fitdata.app/privacy-en.html', 'href_de': 'https://fitdata.app/privacy-de.html',
        'og_locale': 'de_DE', 'prefix': '',
    },
    'terms-en.html': {
        'lang': 'en', 'title': 'FitData — Terms of Use',
        'desc': 'FitData Terms of Use — rules and conditions for using the FitData app and services.',
        'canonical': 'https://fitdata.app/terms-en.html',
        'href_en': 'https://fitdata.app/terms-en.html', 'href_de': 'https://fitdata.app/terms-de.html',
        'og_locale': 'en_US', 'prefix': '',
    },
    'terms-de.html': {
        'lang': 'de', 'title': 'FitData — Nutzungsbedingungen',
        'desc': 'FitData Nutzungsbedingungen — Regeln und Bedingungen für die Nutzung der FitData App.',
        'canonical': 'https://fitdata.app/terms-de.html',
        'href_en': 'https://fitdata.app/terms-en.html', 'href_de': 'https://fitdata.app/terms-de.html',
        'og_locale': 'de_DE', 'prefix': '',
    },
    'imprint-en.html': {
        'lang': 'en', 'title': 'FitData — Imprint',
        'desc': 'FitData Imprint — legal information and contact details.',
        'canonical': 'https://fitdata.app/imprint-en.html',
        'href_en': 'https://fitdata.app/imprint-en.html', 'href_de': 'https://fitdata.app/impressum-de.html',
        'og_locale': 'en_US', 'prefix': '',
    },
    'impressum-de.html': {
        'lang': 'de', 'title': 'FitData — Impressum',
        'desc': 'FitData Impressum — rechtliche Informationen und Kontaktdaten.',
        'canonical': 'https://fitdata.app/impressum-de.html',
        'href_en': 'https://fitdata.app/imprint-en.html', 'href_de': 'https://fitdata.app/impressum-de.html',
        'og_locale': 'de_DE', 'prefix': '',
    },
}

NAV_EN = '''  <div class="nav-links">
    <a href="{home}#features">Features</a>
    <a href="{blog}">Blog</a>
    <a href="{home}#faq">FAQ</a>
    <a href="support-en.html">Support</a>
    <a href="privacy-en.html">Privacy</a>
    <a href="terms-en.html">Terms</a>
    <a href="imprint-en.html">Imprint</a>
    <div class="nav-lang"><a{class_en} href="{self_en}">EN</a><a{class_de} href="{self_de}" data-alt-href="{alt_de}">DE</a></div>
    <a class="btn-nav" href="https://apps.apple.com/us/app/fitdata-workout-app/id6740706351" target="_blank" rel="noopener">Download</a>
  </div>'''

NAV_DE = '''  <div class="nav-links">
    <a href="{home}#features">Funktionen</a>
    <a href="{blog}">Blog</a>
    <a href="{home}#faq">Fragen</a>
    <a href="support.html">Hilfe</a>
    <a href="privacy-de.html">Datenschutz</a>
    <a href="terms-de.html">Nutzungsbedingungen</a>
    <a href="impressum-de.html">Impressum</a>
    <div class="nav-lang"><a{class_en} href="{self_en}" data-alt-href="{alt_en}">EN</a><a{class_de} href="{self_de}">DE</a></div>
    <a class="btn-nav" href="https://apps.apple.com/de/app/fitdata-workout-app/id6740706351" target="_blank" rel="noopener">Download</a>
  </div>'''


def seo_block(cfg):
    return f'''  <meta name="description" content="{cfg['desc']}" />
  <link rel="canonical" href="{cfg['canonical']}" />
  <link rel="alternate" hreflang="en" href="{cfg['href_en']}" />
  <link rel="alternate" hreflang="de" href="{cfg['href_de']}" />
  <link rel="alternate" hreflang="x-default" href="{cfg['href_en']}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="{cfg['og_locale']}" />
  <meta property="og:title" content="{cfg['title']}" />
  <meta property="og:description" content="{cfg['desc']}" />
  <meta property="og:url" content="{cfg['canonical']}" />
  <meta property="og:image" content="https://fitdata.app/assets/og-image.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{cfg['title']}" />
  <meta name="twitter:description" content="{cfg['desc']}" />
  <meta name="twitter:image" content="https://fitdata.app/assets/og-image.png" />'''


def remove_shared_css(css):
    """Remove CSS blocks now in site.css from inline styles."""
    patterns = [
        r'\s*\*, \*::before, \*::after \{[^}]+\}',
        r'\s*:root \{[^}]+\}',
        r'\s*html \{ scroll-behavior: smooth; \}',
        r'\s*body \{[^}]+min-height: 100vh;[^}]+\}',
        r"\s*h1, h2, h3, h4, nav \.nav-logo span \{[^}]+\}",
        r'\s*/\* NAV \*/.*?\.nav-lang a\.active, \.nav-lang a:hover \{[^}]+\}',
        r'\s*/\* FOOTER \*/.*?\.fbot p \{[^}]+\}',
        r'\s*@media \(max-width: 960px\) \{ nav \{ padding: 0 32px; \} footer \{[^}]+\} \.ft \{ flex-direction: column;[^}]+\} \}',
        r'\s*@media \(max-width: 600px\) \{ nav \{ padding: 0 20px; height: 64px; \} \.nav-links \{ display: none; \}[^}]+\}',
        r'\s*@media \(max-width: 600px\) \{ nav \{ padding: 0 20px; height: 64px; \} \.nav-links \{ display: none; \} \.page-header \{[^}]+\} footer \{[^}]+\} \}',
    ]
    for p in patterns:
        css = re.sub(p, '', css, flags=re.DOTALL)
    return css


def update_subpage(filename):
    path = ROOT / filename
    content = path.read_text(encoding='utf-8')
    cfg = PAGES_SEO[filename]
    is_de = cfg['lang'] == 'de'

    # Update html tag
    content = re.sub(r'<html lang="[^"]*">', f'<html lang="{cfg["lang"]}" class="no-js">', content)

    # Replace title
    content = re.sub(r'<title>[^<]+</title>', f'<title>{cfg["title"]}</title>', content)

    # Remove google fonts and old head assets, add new
    content = re.sub(
        r'  <link rel="preconnect" href="https://fonts\.googleapis\.com" />\s*'
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin />\s*'
        r'<link href="https://fonts\.googleapis\.com/css2[^"]+" rel="stylesheet" />\s*'
        r'  <script src="analytics-consent\.js" defer></script>',
        seo_block(cfg) + '\n' + HEAD_ASSETS.format(prefix=cfg['prefix']),
        content
    )

    # Clean inline CSS
    def clean_style(m):
        css = remove_shared_css(m.group(1))
        return f'<style>{css}</style>'

    content = re.sub(r'<style>(.*?)</style>', clean_style, content, count=1, flags=re.DOTALL)

    # Update nav - insert Blog link
    if is_de:
        content = re.sub(
            r'<a href="[^"]*#features">Funktionen</a>\s*<a href="[^"]*#faq">Fragen</a>',
            '<a href="index-de.html#features">Funktionen</a>\n    <a href="blog-de.html">Blog</a>\n    <a href="index-de.html#faq">Fragen</a>',
            content
        )
        # Footer blog link
        content = re.sub(
            r'(<div class="fcol"><h4>App</h4>.*?<a href="[^"]*#features">Funktionen</a>)',
            r'\1<a href="blog-de.html">Blog</a>',
            content,
            count=1
        )
    else:
        content = re.sub(
            r'<a href="[^"]*#features">Features</a>\s*<a href="[^"]*#faq">FAQ</a>',
            '<a href="index.html#features">Features</a>\n    <a href="blog-en.html">Blog</a>\n    <a href="index.html#faq">FAQ</a>',
            content
        )
        content = re.sub(
            r'(<div class="fcol"><h4>App</h4>.*?<a href="[^"]*#features">Features</a>)',
            r'\1<a href="blog-en.html">Blog</a>',
            content,
            count=1
        )

    # Add width/height to nav logo img
    content = content.replace(
        '<img src="assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" alt="FitData" />',
        '<img src="assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" alt="FitData" width="36" height="36" />'
    )

    # Add nav.js before </body>
    if 'assets/nav.js' not in content:
        content = content.replace('</body>', SCRIPTS.format(prefix='') + '\n</body>')

    path.write_text(content, encoding='utf-8')
    print(f'Updated {filename}')


def update_index(filename):
    path = ROOT / filename
    content = path.read_text(encoding='utf-8')
    cfg = PAGES_SEO[filename]
    is_de = cfg['lang'] == 'de'

    content = re.sub(r'<html lang="[^"]*">', f'<html lang="{cfg["lang"]}" class="no-js">', content)
    content = re.sub(r'<title>[^<]+</title>', f'<title>{cfg["title"]}</title>', content)

    # Replace fonts block
    old_head = re.search(
        r'  <link rel="icon".*?<script src="analytics-consent\.js" defer></script>',
        content, re.DOTALL
    )
    if old_head:
        new_head = (
            seo_block(cfg) + '\n' +
            HEAD_ASSETS.format(prefix='') + '\n' +
            ('  <link rel="alternate" type="application/rss+xml" title="FitData Blog" href="feed-de.xml" />\n' if is_de else
             '  <link rel="alternate" type="application/rss+xml" title="FitData Blog" href="feed-en.xml" />\n')
        )
        content = content.replace(old_head.group(0), new_head.rstrip())

    # Remove shared CSS from inline - keep page-specific only
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if style_match:
        css = style_match.group(1)
        # Remove blocks now in site.css
        remove_blocks = [
            r'\s*\*, \*::before, \*::after \{[^}]+\}',
            r'\s*:root \{[^}]+\}',
            r'\s*html \{ scroll-behavior: smooth; \}',
            r'\s*body \{[^}]+overflow-x: hidden;\s*\}',
            r"\s*h1, h2, h3, h4, h5, button, \.btn, \.label-tag, \.eyebrow, nav \.nav-logo span \{[^}]+\}",
            r'\s*/\* ── NAV ── \*/.*?\.nav-lang a\.active, \.nav-lang a:hover \{[^}]+\}',
            r'\s*/\* ── FAQ ── \*/.*?details\.fq \.fqb \{[^}]+\}',
            r'\s*/\* ── CTA ── \*/.*?\.btn-cta-primary img \{[^}]+\}',
            r'\s*/\* ── FOOTER ── \*/.*?\.fbot p \{[^}]+\}',
            r'\s*@media \(max-width: 960px\) \{[^}]*nav \{ padding: 0 32px; \}[^}]+\}',
            r'\s*@media \(max-width: 600px\) \{[^}]*\.nav-links \{ display: none; \}[^}]+\}',
        ]
        for p in remove_blocks:
            css = re.sub(p, '', css, flags=re.DOTALL)

        # Add hero mask fade
        if '.hero-right' in css and 'mask-image' not in css:
            css = css.replace(
                '.hero-right {\n      display: flex; justify-content: center; align-items: center;\n      height: 100%;\n    }',
                '.hero-right {\n      display: flex; justify-content: center; align-items: center;\n      height: 100%;\n      -webkit-mask-image: linear-gradient(to bottom, #000 75%, transparent 100%);\n      mask-image: linear-gradient(to bottom, #000 75%, transparent 100%);\n    }'
            )

        content = content.replace(style_match.group(0), f'<style>{css}</style>')

    # Nav update
    if is_de:
        content = re.sub(
            r'<a href="#features">Funktionen</a>\s*<a href="#faq">Fragen</a>',
            '<a href="#features">Funktionen</a>\n    <a href="blog-de.html">Blog</a>\n    <a href="#faq">Fragen</a>',
            content
        )
        content = re.sub(
            r'(<a href="index-de\.html#features">Funktionen</a>)',
            r'\1<a href="blog-de.html">Blog</a>',
            content,
            count=1
        )
    else:
        content = re.sub(
            r'<a href="#features">Features</a>\s*<a href="#faq">FAQ</a>',
            '<a href="#features">Features</a>\n    <a href="blog-en.html">Blog</a>\n    <a href="#faq">FAQ</a>',
            content
        )
        content = re.sub(
            r'(<a href="index\.html#features">Features</a>)',
            r'\1<a href="blog-en.html">Blog</a>',
            content,
            count=1
        )

    # Logo dimensions
    content = content.replace(
        '<img src="assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" alt="FitData" />',
        '<img src="assets/FitData_AppIcon-iOS-Default-1024x1024@1x.png" alt="FitData" width="36" height="36" />'
    )

    # JSON-LD for homepage
    if 'application/ld+json' not in content:
        json_ld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "FitData",
    "operatingSystem": "iOS",
    "applicationCategory": "HealthApplication",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "url": "https://fitdata.app"
  }
  </script>'''
        content = content.replace('<style>', json_ld + '\n  <style>', 1)

    # FAQ JSON-LD before closing faq section - skip for now, add manually

    # Scripts before </body>
    scripts = '''<script src="assets/nav.js" defer></script>
<script src="assets/scroll-reveal.js" defer></script>
<script src="assets/video-lazy.js" defer></script>'''
    if 'assets/nav.js' not in content:
        content = content.replace('</body>', scripts + '\n</body>')

    path.write_text(content, encoding='utf-8')
    print(f'Updated {filename}')


if __name__ == '__main__':
    for f in ['support-en.html', 'support.html', 'privacy-en.html', 'privacy-de.html',
              'terms-en.html', 'terms-de.html', 'imprint-en.html', 'impressum-de.html']:
        update_subpage(f)
    for f in ['index.html', 'index-de.html']:
        update_index(f)
    print('Done.')
