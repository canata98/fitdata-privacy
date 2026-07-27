#!/usr/bin/env python3
"""Optimize FitData assets: videos, images, posters."""

import subprocess
import os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'

VIDEO_NAMES = [
    'Create_Workoutplan.MP4',
    'Workout_Performane.MP4',
    'Workout_History.MP4',
    'Workout_History+Performanc.MP4',  # legacy EN
]

IMAGE_EXTENSIONS = {'.png', '.PNG', '.jpg', '.jpeg'}


def run(cmd):
    print(' ', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def optimize_videos():
    for lang in ['en', 'de']:
        lang_dir = ASSETS / lang
        for name in VIDEO_NAMES:
            src = lang_dir / name
            if not src.exists():
                continue
            base = src.stem
            mp4_out = lang_dir / f'{base}-opt.mp4'
            webm_out = lang_dir / f'{base}.webm'
            poster_out = lang_dir / f'{base}-poster.jpg'

            if not mp4_out.exists():
                run([
                    'ffmpeg', '-y', '-i', str(src),
                    '-vf', 'scale=720:-2',
                    '-c:v', 'libx264', '-crf', '28', '-preset', 'slow',
                    '-an', '-movflags', '+faststart',
                    str(mp4_out)
                ])

            if not webm_out.exists():
                run([
                    'ffmpeg', '-y', '-i', str(src),
                    '-vf', 'scale=720:-2',
                    '-c:v', 'libvpx-vp9', '-crf', '35', '-b:v', '0',
                    '-an',
                    str(webm_out)
                ])

            if not poster_out.exists():
                run([
                    'ffmpeg', '-y', '-i', str(src),
                    '-vf', 'scale=720:-2',
                    '-frames:v', '1',
                    str(poster_out)
                ])

            print(f'Video done: {lang}/{base}')


def optimize_images():
    for lang in ['en', 'de']:
        lang_dir = ASSETS / lang
        if not lang_dir.exists():
            continue
        for src in lang_dir.iterdir():
            if src.suffix.lower() not in {'.png', '.jpg', '.jpeg'}:
                continue
            if '-poster' in src.stem or src.stem.endswith('-opt'):
                continue
            webp_out = src.with_suffix('.webp')
            if webp_out.exists():
                continue
            try:
                img = Image.open(src)
                w, h = img.size
                if w > 600:
                    ratio = 600 / w
                    img = img.resize((600, int(h * ratio)), Image.LANCZOS)
                img.save(webp_out, 'WEBP', quality=82)
                print(f'Image: {webp_out.relative_to(ROOT)}')
            except Exception as e:
                print(f'Skip {src}: {e}')


def update_html_videos():
    for html_file in [ROOT / 'index.html', ROOT / 'index-de.html']:
        if not html_file.exists():
            continue
        lang = 'de' if 'de' in html_file.name else 'en'
        text = html_file.read_text()

        for name in VIDEO_NAMES:
            base = name.replace('.MP4', '').replace('.mp4', '')
            old_block = f'''<video autoplay muted loop playsinline>
              <source src="assets/{lang}/{name}" type="video/mp4" />
            </video>'''
            new_block = f'''<video data-lazy-video muted loop playsinline preload="none" poster="assets/{lang}/{base}-poster.jpg">
              <source src="assets/{lang}/{base}.webm" type="video/webm" />
              <source src="assets/{lang}/{base}-opt.mp4" type="video/mp4" />
            </video>'''
            text = text.replace(old_block, new_block)

        html_file.write_text(text)
        print(f'Updated videos in {html_file.name}')


def wrap_images_in_picture(html_path, lang):
    text = html_path.read_text()
    import re

    def replacer(m):
        src = m.group(1)
        alt = m.group(2)
        if not src.startswith(f'assets/{lang}/'):
            return m.group(0)
        if src.endswith('.webp'):
            return m.group(0)
        webp = re.sub(r'\.(png|PNG|jpg|jpeg)$', '.webp', src)
        webp_path = ROOT / webp
        if not webp_path.exists():
            return m.group(0)
        # Get dimensions from image
        try:
            img = Image.open(ROOT / src)
            w, h = img.size
            if w > 600:
                ratio = 600 / w
                w, h = 600, int(h * ratio)
        except Exception:
            w, h = 600, 1200
        loading = 'loading="eager" fetchpriority="high"' if 'Run_RunPlan' in src or 'Workout_Start' in src else 'loading="lazy" decoding="async"'
        return f'''<picture>
              <source srcset="{webp}" type="image/webp" />
              <img src="{src}" alt="{alt}" width="{w}" height="{h}" {loading} />
            </picture>'''

    # Only replace simple img tags inside iphone-inner that aren't already in picture
    pattern = r'<img src="(assets/' + lang + r'/[^"]+\.(?:png|PNG|jpg|jpeg))" alt="([^"]*)" />'
    text_new = re.sub(pattern, replacer, text)
    if text_new != text:
        html_path.write_text(text_new)
        print(f'Wrapped images in {html_path.name}')


if __name__ == '__main__':
    print('=== Optimizing videos ===')
    optimize_videos()
    print('=== Optimizing images ===')
    optimize_images()
    print('=== Updating HTML ===')
    update_html_videos()
    wrap_images_in_picture(ROOT / 'index.html', 'en')
    wrap_images_in_picture(ROOT / 'index-de.html', 'de')
    print('Done.')
