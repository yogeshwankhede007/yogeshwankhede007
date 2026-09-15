#!/usr/bin/env python3
"""Render a self-hosted GitHub stats card as SVG.

Why this exists: the README deliberately avoids third-party image services
(github-readme-stats, komarev, capsule-render, *.herokuapp.com, ...). Those hosts
can change what they serve at any time and the README has no way to pin them.
This script talks only to api.github.com, and the SVG it produces is committed
into this repository, so every pixel in the README is content we control.

Usage:  python .github/scripts/build_stats_svg.py <username> <output.svg>
Auth:   optional GITHUB_TOKEN env var (raises the API rate limit; public data only).
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from xml.sax.saxutils import escape

API = "https://api.github.com"
TIMEOUT = 20

# Card geometry
W, H = 900, 212
PAD = 28
TILE_W, TILE_GAP = 196, 20
BAR_X, BAR_Y, BAR_W, BAR_H = PAD, 166, W - 2 * PAD, 12

# GitHub Linguist colours, plus a neutral for the tail.
LANG_COLORS = {
    "Python": "#3572A5",
    "Java": "#b07219",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Swift": "#F05138",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Kotlin": "#A97BFF",
    "Go": "#00ADD8",
    "Ruby": "#701516",
    "C#": "#178600",
    "Jupyter Notebook": "#DA5B0B",
    "Dockerfile": "#384d54",
    "Gherkin": "#5B2063",
    "Other": "#6b76a0",
}


def api_get(path: str):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-readme-stats",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def collect(user: str) -> dict:
    profile = api_get(f"/users/{user}")

    repos, page = [], 1
    while page <= 5:  # hard cap: 500 repos is plenty, keeps the job bounded
        batch = api_get(f"/users/{user}/repos?per_page=100&page={page}&type=owner")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    forks = sum(r.get("forks_count", 0) for r in own)

    langs: dict[str, int] = {}
    for r in own:
        lang = r.get("language")
        if lang:
            langs[lang] = langs.get(lang, 0) + 1

    since = (profile.get("created_at") or "")[:4] or "-"

    return {
        "repos": len(own),
        "stars": stars,
        "forks": forks,
        "followers": profile.get("followers", 0),
        "since": since,
        "langs": dict(sorted(langs.items(), key=lambda kv: -kv[1])),
    }


def compact(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000:
        return f"{n / 1_000:.1f}k".replace(".0k", "k")
    return str(n)


def tile(idx: int, value: str, label: str) -> str:
    x = PAD + idx * (TILE_W + TILE_GAP)
    cx = x + TILE_W / 2
    return f"""  <g>
    <rect x="{x}" y="52" width="{TILE_W}" height="82" rx="10" fill="#070a14" fill-opacity="0.66" stroke="#1e2a56"/>
    <text x="{cx}" y="96" text-anchor="middle" font-family="Segoe UI,Helvetica Neue,Ubuntu,Arial,sans-serif" font-size="30" font-weight="700" fill="url(#statGrad)">{escape(value)}</text>
    <text x="{cx}" y="118" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" letter-spacing="1.4" fill="#6b76a0">{escape(label)}</text>
  </g>"""


def language_bar(langs: dict[str, int]) -> str:
    total = sum(langs.values())
    if not total:
        return ""

    top = list(langs.items())[:6]
    tail = total - sum(c for _, c in top)
    if tail > 0:
        top.append(("Other", tail))

    segments, legend = [], []
    x, lx = float(BAR_X), float(PAD)
    for i, (name, count) in enumerate(top):
        pct = count / total
        seg_w = max(BAR_W * pct, 3.0)
        if i == len(top) - 1:  # absorb rounding drift into the last segment
            seg_w = max(BAR_X + BAR_W - x, 3.0)
        color = LANG_COLORS.get(name, "#6b76a0")
        # Leave a hairline gap so adjacent similar hues (Python/TypeScript blue)
        # still read as two separate segments.
        draw_w = max(seg_w - 2, 2.0)
        segments.append(
            f'    <rect x="{x:.1f}" y="{BAR_Y}" width="{draw_w:.1f}" height="{BAR_H}" fill="{color}"/>'
        )
        label = f"{name} {pct * 100:.0f}%"
        legend.append(
            f'    <circle cx="{lx + 4:.1f}" cy="{BAR_Y + 34}" r="4" fill="{color}"/>'
            f'<text x="{lx + 14:.1f}" y="{BAR_Y + 38}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10.5" fill="#8b93b0">{escape(label)}</text>'
        )
        x += seg_w
        lx += 20 + len(label) * 6.3

    return (
        f'  <text x="{PAD}" y="{BAR_Y - 10}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="10.5" letter-spacing="1.2" fill="#6b76a0">LANGUAGE MIX &#183; BY REPOSITORY</text>\n'
        f'  <g clip-path="url(#barClip)">\n' + "\n".join(segments) + "\n  </g>\n" + "\n".join(legend)
    )


def render(user: str, d: dict) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y")
    tiles = "\n".join(
        [
            tile(0, compact(d["repos"]), "ORIGINAL REPOS"),
            tile(1, compact(d["stars"]), "STARS EARNED"),
            tile(2, compact(d["followers"]), "FOLLOWERS"),
            tile(3, d["since"], "BUILDING SINCE"),
        ]
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub statistics for {escape(user)}">
  <title>GitHub statistics for {escape(user)}</title>
  <defs>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1020"/>
      <stop offset="100%" stop-color="#0a0d37"/>
    </linearGradient>
    <linearGradient id="statGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#16f2b3"/>
      <stop offset="100%" stop-color="#a78bfa"/>
    </linearGradient>
    <clipPath id="barClip">
      <rect x="{BAR_X}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" rx="6"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" rx="16" fill="url(#cardGrad)"/>
  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="#1e2a56" stroke-width="1.5"/>

  <circle cx="14" cy="30" r="4" fill="#16f2b3"/>
  <text x="{PAD}" y="34" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="12" letter-spacing="1.8" fill="#c3cbe4">GITHUB SIGNAL</text>
  <text x="{W - PAD}" y="34" text-anchor="end" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="#4c5a86">self-hosted &#183; refreshed {stamp}</text>

{tiles}

{language_bar(d["langs"])}
</svg>
"""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    user, out = sys.argv[1], sys.argv[2]
    try:
        data = collect(user)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError) as exc:
        # Never fail the workflow over a transient API hiccup: the previously
        # committed SVG stays in place and the README keeps rendering.
        print(f"stats: skipping refresh ({exc})", file=sys.stderr)
        return 0

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(user, data))
    print(f"stats: wrote {out} ({data['repos']} repos, {data['stars']} stars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
