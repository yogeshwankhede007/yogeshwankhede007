#!/usr/bin/env python3
"""Render the self-hosted "GitHub Signal" card as SVG.

What it shows (lifetime TOTALS only, never a per-repo, per-org or per-year breakdown):
  * Lines of code   - additions authored by the user (max of PR additions and
                      default-branch commit additions, both measured by GitHub)
  * Pull requests   - opened, all time
  * Merged PRs      - plus the merge rate
  * Contributions   - sum of every yearly contribution calendar, private ones
                      included as the anonymous count GitHub already shows publicly
  * Achievements    - scraped from the public achievements tab

Privacy: private and organisation repositories are only ever *summed*. No repository
name, owner, title or per-repo number is written to the SVG or to the cache file.

Baseline + public growth: assets/generated/stats.json stores the lifetime totals
from the last full snapshot, plus the PUBLIC-only part of those totals. The daily
Action runs with nothing but the automatic GITHUB_TOKEN, which only sees public
data, so each run adds the growth in public numbers on top of the snapshot.
Totals therefore keep climbing with new public work and can never go down.
No personal access token or other credential is needed.

Usage:  python .github/scripts/build_stats_svg.py <username> <output.svg>
Auth:   GITHUB_TOKEN env var (the automatic Actions token, public data only).
"""

from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import (AMBER, CYAN, DIM, FAINT, LINE, MONO, MUTED, PINK, SANS, SUB, TEAL, TEXT, TILE,  # noqa: E402
                    VIOLET, esc, frame, header, icon, rise, svg)

API = "https://api.github.com"
TIMEOUT = 25
W = 900

HTTP_ERRORS = (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, KeyError)


# --------------------------------------------------------------------------- API

def _token() -> str:
    return (os.environ.get("GITHUB_TOKEN") or "").strip()


def _request(url: str, data: bytes | None = None, accept: str = "application/vnd.github+json"):
    req = urllib.request.Request(url, data=data, headers={
        "Accept": accept,
        "User-Agent": "profile-readme-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    tok = _token()
    if tok and url.startswith(API):
        req.add_header("Authorization", f"Bearer {tok}")
    return urllib.request.urlopen(req, timeout=TIMEOUT)


def rest(path: str):
    with _request(f"{API}{path}") as resp:
        body = resp.read().decode("utf-8")
        return resp.status, (json.loads(body) if body.strip() else None)


def gql(query: str, **variables):
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    with _request(f"{API}/graphql", data=payload) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    if out.get("errors") and not out.get("data"):
        raise ValueError(out["errors"][0].get("message", "graphql error"))
    return out["data"]


# ----------------------------------------------------------------------- collect

def collect(user: str) -> dict:
    base = gql("""query($u:String!){ user(login:$u){
        createdAt
        pullRequests{ totalCount }
        merged: pullRequests(states:MERGED){ totalCount }
        contributionsCollection{ contributionYears }
    } }""", u=user)["user"]

    years = base["contributionsCollection"]["contributionYears"] or []
    contributions = 0
    repos: set[str] = set()
    for y in years:
        c = gql("""query($u:String!,$f:DateTime!,$t:DateTime!){ user(login:$u){
            contributionsCollection(from:$f, to:$t){
              contributionCalendar{ totalContributions }
              commitContributionsByRepository(maxRepositories:100){ repository{ nameWithOwner } }
              pullRequestContributionsByRepository(maxRepositories:100){ repository{ nameWithOwner } }
            } } }""", u=user, f=f"{y}-01-01T00:00:00Z", t=f"{y}-12-31T23:59:59Z")["user"]["contributionsCollection"]
        contributions += c["contributionCalendar"]["totalContributions"]
        for key in ("commitContributionsByRepository", "pullRequestContributionsByRepository"):
            repos.update(r["repository"]["nameWithOwner"] for r in c[key])

    # Sum PR additions; repo names are collected in memory only to count/measure.
    pr_additions, cursor = 0, None
    pub = {"lines": 0, "prs": 0, "merged": 0}
    for _ in range(50):  # 5,000 PRs is a generous hard stop
        page = gql("""query($u:String!,$c:String){ user(login:$u){
            pullRequests(first:100, after:$c){ pageInfo{ hasNextPage endCursor }
              nodes{ additions merged repository{ nameWithOwner isPrivate } } } } }""", u=user, c=cursor)["user"]["pullRequests"]
        for n in page["nodes"]:
            pr_additions += n["additions"] or 0
            if not n["repository"]["isPrivate"]:
                pub["lines"] += n["additions"] or 0
                pub["prs"] += 1
                pub["merged"] += 1 if n["merged"] else 0
            repos.add(n["repository"]["nameWithOwner"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    page = 1
    while page <= 5:
        _, batch = rest(f"/users/{user}/repos?per_page=100&page={page}&type=owner")
        repos.update(r["full_name"] for r in batch or [] if not r.get("fork"))
        if not batch or len(batch) < 100:
            break
        page += 1

    commit_additions = 0
    for full in sorted(repos):
        commit_additions += _author_additions(full, user)

    return {
        "lines": max(pr_additions, commit_additions),
        "prs": base["pullRequests"]["totalCount"],
        "merged": base["merged"]["totalCount"],
        "public": pub,
        "contributions": contributions,
        "repos": len(repos),
        "since": int((base.get("createdAt") or "0")[:4] or 0),
        "achievements": scrape_achievements(user),
    }


def _author_additions(full: str, user: str) -> int:
    """Additions by `user` on a repo's default branch. GitHub computes this lazily (202)."""
    for attempt in range(4):
        try:
            status, data = rest(f"/repos/{full}/stats/contributors")
        except HTTP_ERRORS:
            return 0
        if status == 200 and isinstance(data, list):
            for c in data:
                if ((c.get("author") or {}).get("login") or "").lower() == user.lower():
                    return sum(w.get("a", 0) for w in c.get("weeks", []))
            return 0
        time.sleep(2 + attempt * 2)
    return 0


def scrape_achievements(user: str) -> dict[str, int]:
    """Public achievements tab -> {name: tier}. There is no API for achievements."""
    try:
        with _request(f"https://github.com/{user}?tab=achievements", accept="text/html") as resp:
            html = resp.read().decode("utf-8", "replace")
    except HTTP_ERRORS:
        return {}
    found: dict[str, int] = {}
    marks = list(re.finditer(r'alt="Achievement: ([^"]+)"', html))
    for i, m in enumerate(marks):
        seg = html[m.end(): marks[i + 1].start() if i + 1 < len(marks) else m.end() + 2000]
        seg = seg.split("</a>", 1)[0]  # the tier label lives inside the same badge link
        tier = re.search(r'achievement-tier-label[^>]*>\s*x(\d+)', seg)
        name = m.group(1).strip()
        found[name] = max(found.get(name, 1), int(tier.group(1)) if tier else 1)
    return found


# ------------------------------------------------------------------------- cache

NUMERIC = ("lines", "prs", "merged", "contributions", "repos")


GROWING = ("lines", "prs", "merged")


def merge(cached: dict, fresh: dict) -> dict:
    """Snapshot totals + growth of the public part since the last run; never decreases."""
    out = dict(cached)
    old_pub = cached.get("public") or {}
    new_pub = fresh.get("public") or {}
    out_pub = dict(old_pub)
    for k in NUMERIC:
        base = int(cached.get(k, 0) or 0)
        grown = base
        if k in GROWING and k in old_pub and k in new_pub:
            grown = base + max(0, int(new_pub[k]) - int(old_pub[k]))
        out[k] = max(grown, int(fresh.get(k, 0) or 0))
    for k in GROWING:
        if k in new_pub:
            out_pub[k] = max(int(old_pub.get(k, 0)), int(new_pub[k]))
    out["public"] = out_pub
    sinces = [v for v in (cached.get("since"), fresh.get("since")) if v]
    out["since"] = min(sinces) if sinces else None
    ach = dict(cached.get("achievements") or {})
    for name, tier in (fresh.get("achievements") or {}).items():
        ach[name] = max(ach.get(name, 1), tier)
    out["achievements"] = ach
    return out


# ------------------------------------------------------------------------ render

def compact(n: int) -> str:
    """Honest rounding: always round DOWN and mark with + when truncated."""
    if n < 1000:
        return str(n)
    if n < 10_000:
        v = math.floor(n / 100) / 10
        s = f"{v:.1f}".rstrip("0").rstrip(".")
        return f"{s}K" + ("+" if n % 1000 else "")
    if n < 1_000_000:
        return f"{n // 1000}K" + ("+" if n % 1000 else "")
    v = math.floor(n / 100_000) / 10
    return f"{v:.1f}".rstrip("0").rstrip(".") + "M+"


def count_up(cx: float, y: float, final: int, delay: float, size: int = 34) -> str:
    """Odometer effect with discrete SMIL frames; the last frame is the static fallback."""
    fracs = [0.04, 0.12, 0.25, 0.42, 0.6, 0.76, 0.88, 0.96, 1.0]
    step, total = 0.11, delay + 0.11 * len(fracs) + 0.1
    style = (f'x="{cx:.1f}" y="{y}" text-anchor="middle" font-family="{SANS}" font-size="{size}" '
             f'font-weight="800" fill="url(#num)"')
    out = []
    for i, f in enumerate(fracs):
        val = compact(int(final * (1 - (1 - f) ** 3))) if f < 1 else compact(final)
        start = (delay + i * step) / total
        if f < 1:
            end = (delay + (i + 1) * step) / total
            out.append(f'<text {style} opacity="0">{esc(val)}<animate attributeName="opacity" values="0;1;0" '
                       f'keyTimes="0;{start:.3f};{end:.3f}" calcMode="discrete" dur="{total:.2f}s" fill="freeze"/></text>')
        else:
            out.append(f'<text {style}>{esc(val)}<animate attributeName="opacity" values="0;1" '
                       f'keyTimes="0;{start:.3f}" calcMode="discrete" dur="{total:.2f}s" fill="freeze"/></text>')
    return "".join(out)


ACH_STYLE = {
    "Pull Shark": ("pr", CYAN, "#1d4ed8"),
    "Pair Extraordinaire": ("users", PINK, "#7c3aed"),
    "Quickdraw": ("zap", AMBER, "#ea580c"),
    "YOLO": ("merge", TEAL, "#0f766e"),
    "Starstruck": ("star", AMBER, "#b45309"),
    "Galaxy Brain": ("bulb", VIOLET, "#4c1d95"),
    "Open Sourcerer": ("code", TEAL, "#155e75"),
    "Arctic Code Vault Contributor": ("shield", CYAN, "#1e3a8a"),
}
TIER_COLORS = {1: None, 2: "#cd7f32", 3: "#c0c7d6", 4: "#fbbf24"}


def medallion(cx: float, cy: float, name: str, tier: int, i: int) -> str:
    ic, a, b = ACH_STYLE.get(name, ("star", VIOLET, "#4c1d95"))
    gid = f"m{i}"
    ring = TIER_COLORS.get(min(tier, 4)) or a
    parts = [
        f'<defs><radialGradient id="{gid}" cx="35%" cy="30%" r="80%">'
        f'<stop offset="0%" stop-color="{a}" stop-opacity="0.55"/><stop offset="100%" stop-color="{b}" stop-opacity="0.35"/>'
        f'</radialGradient></defs>',
        f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{a}" stroke-opacity="0.35" stroke-width="1.5">'
        f'<animate attributeName="r" values="30;40;30" dur="3.2s" begin="{i * 0.4:.1f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values="0.45;0;0.45" dur="3.2s" begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></circle>',
        f'<circle cx="{cx}" cy="{cy}" r="29" fill="url(#{gid})" stroke="{ring}" stroke-width="2.5"/>',
        f'<circle cx="{cx}" cy="{cy}" r="29" fill="none" stroke="#ffffff" stroke-opacity="0.5" stroke-width="2.5" '
        f'stroke-dasharray="14 168" stroke-linecap="round">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
        f'dur="{6 + i}s" repeatCount="indefinite"/></circle>',
        icon(ic, cx - 13, cy - 13, 26, "#ffffff", 2.2),
        f'<text x="{cx}" y="{cy + 54}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="{TEXT}">{esc(name)}</text>',
    ]
    if tier > 1:
        parts.append(
            f'<rect x="{cx + 14}" y="{cy + 12}" width="28" height="18" rx="9" fill="#0b1020" stroke="{ring}" stroke-width="1.5"/>'
            f'<text x="{cx + 28}" y="{cy + 25}" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{ring}">x{tier}</text>')
    return f'<g>{rise(1.3 + i * 0.12)}{"".join(parts)}</g>'


def render(user: str, d: dict) -> str:
    pad, gap = 28, 16
    tw = (W - 2 * pad - 3 * gap) / 4
    ty, th = 58, 118
    ach = sorted((d.get("achievements") or {}).items(), key=lambda kv: (-kv[1], kv[0]))
    ach_top = ty + th + 64
    H = ach_top + (132 if ach else 0) + 18

    defs, body = frame(W, H, TEAL, VIOLET, PINK, glow=VIOLET, glow_xy=(W * 0.9, H * 0.15))
    defs += f"""
    <linearGradient id="num" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{TEAL}"/><stop offset="60%" stop-color="{CYAN}"/><stop offset="100%" stop-color="{VIOLET}"/>
    </linearGradient>"""

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y")
    parts = [body, header(pad, 36, "GITHUB SIGNAL", f"lifetime totals · refreshed {stamp}", W)]

    merged, prs = d.get("merged", 0), d.get("prs", 0)
    rate = round(100 * merged / prs) if prs else 0
    tiles = [
        ("code", "LINES OF CODE", d.get("lines", 0), "written and shipped", TEAL),
        ("pr", "PULL REQUESTS", prs, "opened, all time", CYAN),
        ("merge", "MERGED PRS", merged, f"{rate}% merge rate", VIOLET),
        ("pulse", "CONTRIBUTIONS", d.get("contributions", 0), f"since {d.get('since') or '-'}", PINK),
    ]
    for i, (ic, label, value, caption, col) in enumerate(tiles):
        x = pad + i * (tw + gap)
        cx = x + tw / 2
        bar = ""
        if label == "MERGED PRS":
            bw = tw - 48
            fill = bw * rate / 100
            bar = (f'<rect x="{x + 24:.1f}" y="{ty + th - 16}" width="{bw:.1f}" height="4" rx="2" fill="{LINE}"/>'
                   f'<rect x="{x + 24:.1f}" y="{ty + th - 16}" width="{fill:.1f}" height="4" rx="2" fill="{col}">'
                   f'<animate attributeName="width" values="0;0;{fill:.1f}" keyTimes="0;0.35;1" dur="1.8s" '
                   f'calcMode="spline" keySplines="0 0 1 1;0.2 0.8 0.2 1" fill="freeze"/></rect>')
        parts.append(
            f'\n  <g>{rise(0.1 + i * 0.1)}'
            f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="12" fill="{TILE}" fill-opacity="0.66" stroke="{LINE}"/>'
            f'<rect x="{x + 16:.1f}" y="{ty}" width="{tw - 32:.1f}" height="2" rx="1" fill="{col}" fill-opacity="0.9"/>'
            f'{icon(ic, cx - 58, ty + 17, 13, col)}'
            f'<text x="{cx + 9:.1f}" y="{ty + 28}" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="{DIM}">{esc(label)}</text>'
            f'{count_up(cx, ty + 72, int(value), 0.35 + i * 0.12)}'
            f'<text x="{cx:.1f}" y="{ty + 94}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTED}">{esc(caption)}</text>'
            f'{bar}</g>')

    strip_y = ty + th + 30
    strip = (f'{d.get("repos", 0)} repositories touched   ·   {len(ach)} achievements unlocked   ·   '
             f'private work counted, never exposed')
    parts.append(f'\n  <g>{rise(0.9)}<line x1="{pad}" y1="{strip_y - 14}" x2="{W - pad}" y2="{strip_y - 14}" stroke="{LINE}"/>'
                 f'<text x="{W / 2}" y="{strip_y + 2}" text-anchor="middle" font-family="{MONO}" font-size="11" '
                 f'letter-spacing="0.4" fill="{FAINT}">{esc(strip)}</text></g>')

    if ach:
        parts.append(f'\n  <text x="{pad}" y="{ach_top + 8}" font-family="{MONO}" font-size="10.5" letter-spacing="1.4" fill="{DIM}">ACHIEVEMENTS</text>')
        n = len(ach)
        slot = (W - 2 * pad) / n
        for i, (name, tier) in enumerate(ach):
            parts.append("\n  " + medallion(round(pad + slot * (i + 0.5), 1), ach_top + 52, name, tier, i))

    return svg(W, int(H), (f"GitHub signal for {user}: {compact(d.get('lines', 0))} lines of code, "
                           f"{prs} pull requests, {merged} merged, {compact(d.get('contributions', 0))} contributions"),
               defs, "".join(parts))


# -------------------------------------------------------------------------- main

def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    user, out = sys.argv[1], sys.argv[2]
    cache_path = os.path.join(os.path.dirname(out) or ".", "stats.json")

    cached = {}
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as fh:
            cached = json.load(fh)

    try:
        fresh = collect(user)
    except HTTP_ERRORS as exc:
        # Never fail the workflow over a transient API hiccup: re-render from cache.
        print(f"stats: API unavailable, rendering from cache ({exc})", file=sys.stderr)
        fresh = {}

    data = merge(cached, fresh)
    if not any(data.get(k) for k in NUMERIC):
        print("stats: no data and no cache; leaving existing SVG untouched", file=sys.stderr)
        return 0

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(cache_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(user, data))
    print(f"stats: wrote {out} (lines={data['lines']}, prs={data['prs']}, merged={data['merged']}, "
          f"contributions={data['contributions']}, achievements={len(data['achievements'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
