"""Shared design tokens and SVG helpers for every card in this profile.

All cards are rendered to static SVG files that are committed to the repo.
Motion uses SMIL only (it survives GitHub's <img> sandbox, JavaScript does not),
and every animated element degrades to its final, fully visible state when a
renderer ignores SMIL.
"""

from __future__ import annotations

from xml.sax.saxutils import escape

SANS = "Segoe UI,Helvetica Neue,Ubuntu,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

BG_A, BG_B = "#0b1020", "#0a0d37"
TILE = "#070a14"
LINE = "#1e2a56"
TEXT = "#e6ebff"
SUB = "#c3cbe4"
MUTED = "#8b93b0"
DIM = "#6b76a0"
FAINT = "#4c5a86"

TEAL, CYAN, VIOLET, PINK, AMBER = "#16f2b3", "#6ee7f9", "#a78bfa", "#ec4899", "#fbbf24"

# Lucide-style 24x24 stroke icons: a list of SVG child elements.
ICONS = {
    "bulb": ['<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>',
             '<path d="M9 18h6"/>', '<path d="M10 22h4"/>'],
    "branch": ['<path d="M6 3v12"/>', '<circle cx="18" cy="6" r="3"/>', '<circle cx="6" cy="18" r="3"/>',
               '<path d="M18 9a9 9 0 0 1-9 9"/>'],
    "chat": ['<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
             '<path d="M8 9h8"/>', '<path d="M8 13h5"/>'],
    "flag": ['<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>', '<path d="M4 22v-7"/>'],
    "screen": ['<path d="M2 3h20"/>', '<path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/>',
               '<path d="m7 21 5-5 5 5"/>', '<path d="M8 12l3-3 2 2 3-3"/>'],
    "target": ['<circle cx="12" cy="12" r="10"/>', '<circle cx="12" cy="12" r="6"/>', '<circle cx="12" cy="12" r="2"/>'],
    "users": ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>', '<circle cx="9" cy="7" r="4"/>',
              '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>', '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'],
    "refresh": ['<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>', '<path d="M21 3v5h-5"/>',
                '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>', '<path d="M8 16H3v5"/>'],
    "shield": ['<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>', '<path d="m9 12 2 2 4-4"/>'],
    "pulse": ['<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'],
    "check": ['<circle cx="12" cy="12" r="10"/>', '<path d="m9 12 2 2 4-4"/>'],
    "zap": ['<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>'],
    "phone": ['<rect x="5" y="2" width="14" height="20" rx="2"/>', '<path d="M12 18h.01"/>'],
    "rain": ['<path d="M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2"/>', '<path d="M16 14v6"/>',
             '<path d="M8 14v6"/>', '<path d="M12 16v6"/>'],
    "workflow": ['<rect x="3" y="3" width="8" height="8" rx="2"/>', '<path d="M7 11v4a2 2 0 0 0 2 2h4"/>',
                 '<rect x="13" y="13" width="8" height="8" rx="2"/>'],
    "code": ['<path d="m16 18 6-6-6-6"/>', '<path d="m8 6-6 6 6 6"/>'],
    "merge": ['<circle cx="18" cy="18" r="3"/>', '<circle cx="6" cy="6" r="3"/>', '<path d="M6 21V9a9 9 0 0 0 9 9"/>'],
    "pr": ['<circle cx="18" cy="18" r="3"/>', '<circle cx="6" cy="6" r="3"/>', '<path d="M13 6h3a2 2 0 0 1 2 2v7"/>',
           '<path d="M6 9v12"/>'],
    "grid": ['<rect x="3" y="3" width="7" height="7" rx="1"/>', '<rect x="14" y="3" width="7" height="7" rx="1"/>',
             '<rect x="14" y="14" width="7" height="7" rx="1"/>', '<rect x="3" y="14" width="7" height="7" rx="1"/>'],
    "star": ['<path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>'],
}


def esc(s) -> str:
    return escape(str(s))


def icon(name: str, x: float, y: float, size: float, color: str, width: float = 2) -> str:
    s = size / 24
    body = "".join(ICONS.get(name, ICONS["star"]))
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="{width / s:.2f}" stroke-linecap="round" stroke-linejoin="round">{body}</g>')


def rise(delay: float, dur: float = 0.7, dy: float = 12) -> str:
    """Fade + slide-up entrance that freezes on the final (visible) frame.

    Put it inside a <g> that has no transform attribute of its own.
    """
    total = delay + dur
    k = delay / total
    return (
        f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{k:.3f};1" dur="{total:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" '
        f'keyTimes="0;{k:.3f};1" dur="{total:.2f}s" fill="freeze" calcMode="spline" '
        f'keySplines="0 0 1 1;0.2 0.8 0.2 1"/>'
    )


def frame(w: int, h: int, a: str = TEAL, b: str = VIOLET, c: str = PINK, glow: str = VIOLET,
          glow_xy=None, grid: bool = True, radius: int = 16) -> tuple[str, str]:
    """Return (defs, body) for the shared card chrome: gradient, grid, glow, animated border."""
    gx, gy = glow_xy or (w * 0.85, h * 0.9)
    grid_rect = f'<rect width="{w}" height="{h}" fill="url(#grid)"/>' if grid else ""
    defs = f"""
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG_A}"/><stop offset="100%" stop-color="{BG_B}"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{a}" stop-opacity="0.9"/>
      <stop offset="30%" stop-color="{LINE}"/>
      <stop offset="70%" stop-color="{LINE}"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0.9"/>
      <animate attributeName="x1" values="0;1;0" dur="10s" repeatCount="indefinite"/>
      <animate attributeName="y2" values="1;0;1" dur="10s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{a}"/><stop offset="55%" stop-color="{b}"/><stop offset="100%" stop-color="{c}"/>
      <animate attributeName="x1" values="0;-0.6;0" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="1;1.6;1" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="glow">
      <stop offset="0%" stop-color="{glow}" stop-opacity="0.32"/><stop offset="100%" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0 L0 0 0 28" fill="none" stroke="{TEAL}" stroke-opacity="0.045" stroke-width="1"/>
    </pattern>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>"""
    body = f"""
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    {grid_rect}
    <circle cx="{gx:.0f}" cy="{gy:.0f}" r="{max(w, h) * 0.32:.0f}" fill="url(#glow)">
      <animate attributeName="cx" values="{gx:.0f};{gx - w * 0.08:.0f};{gx:.0f}" dur="12s" repeatCount="indefinite"/>
    </circle>
  </g>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{radius}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>"""
    return defs, body


def header(x: float, y: float, label: str, right: str | None = None, w: int = 900, color: str = TEAL) -> str:
    out = (f'\n  <circle cx="{x + 4}" cy="{y - 4}" r="4" fill="{color}">'
           f'<animate attributeName="fill-opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>'
           f'\n  <text x="{x + 16}" y="{y}" font-family="{MONO}" font-size="12" letter-spacing="1.8" fill="{SUB}">{esc(label)}</text>')
    if right:
        out += (f'\n  <text x="{w - x}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="10.5" '
                f'letter-spacing="0.6" fill="{FAINT}">{esc(right)}</text>')
    return out


def svg(w: int, h: int, title: str, defs: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}">\n  <title>{esc(title)}</title>\n  <defs>{defs}\n  </defs>'
            f'{body}\n</svg>\n')


def chip_width(text: str, size: float = 10.5) -> float:
    """Approximate width of a monospace chip; monospace keeps this estimate honest."""
    return len(text) * size * 0.61 + 18
