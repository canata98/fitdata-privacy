# Blog schreiben (Markdown)

Neue Artikel erstellst du als **Markdown-Dateien** in diesem Ordner. Ein Build-Skript erzeugt daraus die HTML-Seiten, Sitemap und RSS-Feeds.

## Schnellstart

1. **Vorlage kopieren**
   - Deutsch: `_example.de.md` → `mein-artikel.de.md`
   - Englisch: `_example.en.md` → `mein-artikel.en.md`
   - Gleicher `slug` in beiden Dateien (z. B. `mein-artikel`)

2. **Frontmatter ausfüllen** (YAML-Block oben)
   - `published: true` setzen, wenn der Artikel live gehen soll
   - `published: false` = Entwurf (erscheint nirgends auf der Website)

3. **Bilder ablegen** in `assets/blog/`:
   - `{slug}-thumb.webp` + `{slug}-thumb.jpg` (800×450, Karten-Vorschau)
   - `{slug}-hero.webp` + `{slug}-hero.jpg` (1200×675, Artikel-Header)

4. **Build ausführen**
   ```bash
   python3 scripts/build_blog.py
   ```

5. **Committen & pushen** — GitHub Pages aktualisiert die Website automatisch.

## Markdown-Syntax

Unterstützt werden:

- Absätze (Leerzeile dazwischen)
- `## Überschrift` → `<h2>`
- `- Bullet` → Liste

Beispiel siehe `first-workout-plan.de.md` / `first-workout-plan.en.md`.

## Frontmatter-Felder

| Feld | Pflicht | Beschreibung |
|------|---------|--------------|
| `slug` | ja | URL-Teil, z. B. `first-workout-plan` |
| `lang` | ja | `de` oder `en` |
| `title` | ja | Artikel-Titel |
| `description` | ja | SEO-Beschreibung (~160 Zeichen) |
| `date` | ja | `YYYY-MM-DD` |
| `category` | ja | Kategorie-Chip auf der Karte |
| `readTime` | ja | Minuten (Zahl) |
| `thumbnail` | ja | WebP-Pfad zur Karten-Vorschau |
| `thumbnailFallback` | ja | JPG-Fallback |
| `hero` | ja | WebP Hero-Bild |
| `heroFallback` | ja | JPG Hero-Fallback |
| `heroAlt` | ja | Alt-Text fürs Hero-Bild |
| `published` | ja | `true` / `false` |
| `author` | nein | z. B. „Verfasst vom FitData-Team“ |
| `cardTeaser` | nein | Kurztext auf der Blog-Karte |

## Generierte Dateien (nicht manuell editieren)

- `blog/{slug}-de.html` / `blog/{slug}-en.html`
- Bereich in `blog-de.html` / `blog-en.html` zwischen `<!-- BLOG-GENERATED-START -->` und `<!-- BLOG-GENERATED-END -->`
- `sitemap.xml` (Blog-Abschnitt)
- `feed-de.xml` / `feed-en.xml`

## Workflow-Tipp

- Entwurf: `published: false` → nur Markdown committen, Build optional lokal testen
- Veröffentlichen: `published: true` → Build → alles committen & pushen
