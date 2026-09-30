#!/usr/bin/env python3
"""Render the static profile cards (projects, core strengths, principles).

These cards replace markdown tables: GitHub sizes tables to their content, so
side-by-side cells never lined up. Fixed-size SVGs placed at 49%/100% width
align perfectly at every viewport width.

Usage: python .github/scripts/build_cards.py      (writes into assets/cards/)
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from svgkit import (AMBER, CYAN, DIM, FAINT, LINE, MONO, MUTED, PINK, SANS, SUB, TEAL, TEXT, TILE,  # noqa: E402
                    VIOLET, chip_width, esc, frame, header, icon, rise, svg)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "cards")

PROJECTS = [
    {
        "slug": "mobix-ai", "name": "Mobix-AI", "tag": "AI AGENT · MOBILE", "icon": "phone",
        "colors": (TEAL, CYAN, VIOLET),
        "lines": ["Autonomous mobile testing at the speed of thought.",
                  "An MCP-powered agent that drives real devices",
                  "instead of following hardcoded scripts."],
        "chips": ["TypeScript", "MCP", "WebdriverIO"],
    },
    {
        "slug": "kisan-mausam-alert", "name": "kisan-mausam-alert", "tag": "GENAI · SOCIAL IMPACT", "icon": "rain",
        "colors": (CYAN, TEAL, AMBER),
        "lines": ["AI-powered weather alerts for Indian farmers.",
                  "Watches IMD forecasts and pushes crop-specific",
                  "advisories in the farmer's own language."],
        "chips": ["Python", "GenAI", "Scheduled Jobs"],
    },
    {
        "slug": "websec-ai", "name": "WebSec-AI", "tag": "AI · APPLICATION SECURITY", "icon": "shield",
        "colors": (PINK, VIOLET, TEAL),
        "lines": ["Fuses AI with offensive security technique to",
                  "detect and prevent web app vulnerabilities, with",
                  "OWASP coverage and prompt-engineered analysis."],
        "chips": ["Python", "OWASP", "AppSec"],
    },
    {
        "slug": "python-pro-with-cicd", "name": "python-pro-with-cicd", "tag": "DEVOPS · CI/CD", "icon": "workflow",
        "colors": (VIOLET, CYAN, TEAL),
        "lines": ["Production-grade Python CI/CD template: quality",
                  "gates, security scanning and multi-stage deploys,",
                  "wired end to end with GitHub Actions."],
        "chips": ["Python", "Bandit", "GitHub Actions"],
    },
    {
        "slug": "chaos-test-framework", "name": "chaos-test-framework", "tag": "RESILIENCE · CHAOS", "icon": "zap",
        "colors": (AMBER, PINK, VIOLET),
        "lines": ["Simulate, disrupt, fortify. A BDD-driven Java",
                  "framework that uses ToxiProxy to prove resilience",
                  "under latency, jitter and network partitions."],
        "chips": ["Java", "ToxiProxy", "BDD"],
    },
    {
        "slug": "performance-test-k6", "name": "PerformanceTestWithK6", "tag": "PERFORMANCE · OBSERVABILITY",
        "icon": "pulse", "colors": (TEAL, VIOLET, PINK),
        "lines": ["Modern load testing with k6, InfluxDB and Grafana,",
                  "wired into CI so performance regressions are",
                  "caught by a pipeline, not by a customer."],
        "chips": ["k6", "Grafana", "InfluxDB"],
    },
]

STRENGTHS = [
    ("bulb", "Critical Thinking", ["Question the problem", "before solving it"]),
    ("branch", "Logical Mindset", ["Chaos into clear,", "ordered, testable steps"]),
    ("chat", "Communication", ["Tech detail turned into", "decisions people act on"]),
    ("flag", "Leadership", ["Mentor, unblock and", "own outcomes end to end"]),
    ("screen", "Presentation", ["Demos and design talks", "that land in any room"]),
    ("target", "Problem Solving", ["Root cause over quick", "fix, every single time"]),
    ("users", "Collaboration", ["Dev, product and QA", "moving as one team"]),
    ("refresh", "Adaptability", ["Tester to builder,", "learning at full speed"]),
]

PRINCIPLES = [
    ("check", "Tests Shape Design", ["Hard-to-test code is", "telling you something."]),
    ("pulse", "Built Observable", ["Logs, metrics, traces", "ship with the feature."]),
    ("shield", "Secure by Default", ["The safe path should", "be the easy path too."]),
    ("zap", "Obsess Over Edges", ["Automate the boring;", "bugs hide at the edge."]),
]

TILE_COLORS = [TEAL, CYAN, VIOLET, PINK, AMBER, TEAL, VIOLET, CYAN]


def project_card(p: dict) -> str:
    w, h = 440, 220
    a, b, c = p["colors"]
    defs, body = frame(w, h, a, b, c, glow=a, glow_xy=(w * 0.92, h * 0.05))
    parts = [body]
    parts.append(f'\n  <rect x="0" y="0" width="{w}" height="3" fill="url(#accent)" clip-path="url(#clip)"/>')

    parts.append(f'\n  <g>{rise(0.05)}'
                 f'<rect x="24" y="24" width="44" height="44" rx="12" fill="{a}" fill-opacity="0.10" stroke="{a}" stroke-opacity="0.45"/>'
                 f'{icon(p["icon"], 34, 34, 24, a)}'
                 f'<text x="84" y="44" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">{esc(p["name"])}</text>'
                 f'<text x="84" y="63" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="{a}">{esc(p["tag"])}</text>'
                 f'</g>')
    parts.append(f'\n  <circle cx="{w - 30}" cy="34" r="4" fill="{a}">'
                 f'<animate attributeName="fill-opacity" values="1;0.2;1" dur="2.2s" repeatCount="indefinite"/></circle>')

    bold = ' font-weight="600"'
    lines = "".join(
        f'<text x="24" y="{104 + i * 21}" font-family="{SANS}" font-size="13.5" fill="{SUB if i == 0 else MUTED}"'
        f'{bold if i == 0 else ""}>{esc(t)}</text>'
        for i, t in enumerate(p["lines"])
    )
    parts.append(f'\n  <g>{rise(0.2)}{lines}</g>')

    x = 24.0
    chips = []
    for i, t in enumerate(p["chips"]):
        cw = chip_width(t)
        col = (a, b, c)[i % 3]
        chips.append(f'<rect x="{x:.1f}" y="172" width="{cw:.1f}" height="24" rx="12" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-opacity="0.35"/>'
                     f'<text x="{x + cw / 2:.1f}" y="188" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{SUB}">{esc(t)}</text>')
        x += cw + 8
    parts.append(f'\n  <g>{rise(0.35)}{"".join(chips)}</g>')
    parts.append(f'\n  <text x="{w - 24}" y="188" text-anchor="end" font-family="{MONO}" font-size="10" fill="{FAINT}">view repo ↗</text>')
    return svg(w, h, f'{p["name"]}: {" ".join(p["lines"])}', defs, "".join(parts))


def tile_grid(items, title_label: str, right: str, aria: str, cols: int = 4) -> str:
    w, pad, gap = 900, 28, 16
    tw = (w - 2 * pad - (cols - 1) * gap) / cols
    th = 124
    rows = (len(items) + cols - 1) // cols
    top = 58
    h = top + rows * th + (rows - 1) * gap + 26
    defs, body = frame(w, h, TEAL, VIOLET, PINK, glow=VIOLET, glow_xy=(w * 0.12, h * 0.95))
    parts = [body, header(pad, 36, title_label, right, w)]
    for i, (ic, name, desc) in enumerate(items):
        r, cidx = divmod(i, cols)
        x = pad + cidx * (tw + gap)
        y = top + r * (th + gap)
        col = TILE_COLORS[i % len(TILE_COLORS)]
        desc_svg = "".join(
            f'<text x="{x + 18:.1f}" y="{y + 98 + j * 15}" font-family="{MONO}" font-size="10.5" fill="{MUTED}">{esc(t)}</text>'
            for j, t in enumerate(desc)
        )
        delay = 0.1 + i * 0.09
        parts.append(
            f'\n  <g>{rise(delay)}'
            f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" rx="12" fill="{TILE}" fill-opacity="0.66" stroke="{LINE}"/>'
            f'<rect x="{x + 18:.1f}" y="{y + 16}" width="34" height="34" rx="10" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-opacity="0.4"/>'
            f'{icon(ic, x + 25, y + 23, 20, col)}'
            f'<text x="{x + 18:.1f}" y="{y + 72}" font-family="{SANS}" font-size="15" font-weight="700" fill="{TEXT}">{esc(name)}</text>'
            f'{desc_svg}'
            f'<rect x="{x + 18:.1f}" y="{y + 79}" width="36" height="2" rx="1" fill="{col}" fill-opacity="0.85">'
            f'<animate attributeName="width" values="12;48;12" dur="{3.2 + (i % 4) * 0.4:.1f}s" repeatCount="indefinite"/></rect>'
            f'</g>'
        )
    return svg(w, int(h), aria, defs, "".join(parts))


def write(name: str, content: str) -> None:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print(f"cards: wrote {os.path.relpath(path, ROOT)}")


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    for p in PROJECTS:
        write(f"project-{p['slug']}.svg", project_card(p))
    write("strengths.svg", tile_grid(
        STRENGTHS, "CORE STRENGTHS", "the skills that make the code matter",
        "Core strengths: " + ", ".join(n for _, n, _ in STRENGTHS)))
    write("principles.svg", tile_grid(
        PRINCIPLES, "ENGINEERING PRINCIPLES", "four rules, zero exceptions",
        "Engineering principles: " + ", ".join(n for _, n, _ in PRINCIPLES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
