"""Generate the Tensor Rails org banner (dark and light) as animated SVG.

Usage: python3 scripts/make_banner.py profile/assets
"""
import sys
from pathlib import Path

W, H = 1280, 360
CX = 980            # axis between the purple and blue rail families
GAP = 10            # half gap between the two innermost verticals
N, STEP, RMIN = 6, 20, 28
RMAX = RMIN + (N - 1) * STEP
AY = 60 + RMAX      # arc centre y: the topmost rail runs at y=60
PURPLE_AX = CX - GAP - RMAX
BLUE_AX = CX + GAP + RMAX
SPAN = W - BLUE_AX  # horizontal run length, same on both sides

THEMES = {
    "dark": dict(
        bg="#06070c", border="none", title="#f4f5fa", tagline="#9aa3b8",
        grid="#ffffff", grid_op=0.07, glow_op=0.22,
        purple=("#e29bff", "#9b4dff", "#5b21b6"),
        blue=("#6fdcff", "#1e9bff", "#1d4ed8"),
        node_p="#f3e8ff", node_b="#e0f4ff", node_stroke="none",
        rail_op=0.95, halo_op=0.18,
    ),
    "light": dict(
        bg="#f7f8fb", border="#e3e6ee", title="#0b0d14", tagline="#586176",
        grid="#0b0d14", grid_op=0.07, glow_op=0.10,
        purple=("#c084fc", "#8b3dff", "#5b21b6"),
        blue=("#38bdf8", "#0b84ff", "#1d4ed8"),
        node_p="#ffffff", node_b="#ffffff", node_stroke="currentColor",
        rail_op=1.0, halo_op=0.10,
    ),
}


def rails():
    out = []
    for i in range(N):
        r = RMAX - i * STEP
        y = AY - r
        p = (f"M {PURPLE_AX - SPAN} {y} H {PURPLE_AX} "
             f"A {r} {r} 0 0 1 {PURPLE_AX + r} {AY} V {H + 10}")
        b = (f"M {W} {y} H {BLUE_AX} "
             f"A {r} {r} 0 0 0 {BLUE_AX - r} {AY} V {H + 10}")
        out.append((i, p, b))
    return out


def svg(t):
    p0, p1, p2 = t["purple"]
    b0, b1, b2 = t["blue"]
    left = PURPLE_AX - SPAN
    border = (f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" '
              f'fill="none" stroke="{t["border"]}"/>') if t["border"] != "none" else ""

    paths_p, paths_b, nodes = [], [], []
    for i, p, b in rails():
        paths_p.append(f'<path d="{p}"/>')
        paths_b.append(f'<path d="{b}"/>')
        # one node per rail; durations and phases differ so they never march in step
        dur = 7.5 + i * 0.9
        for side, d, fill, col in (("p", p, t["node_p"], p1), ("b", b, t["node_b"], b1)):
            phase = -((i * 1.7 + (0.8 if side == "b" else 0)) % dur)
            stroke = (f' stroke="{col}" stroke-width="2"' if t["node_stroke"] != "none" else "")
            nodes.append(
                f'<circle r="4.5" fill="{fill}"{stroke} filter="url(#glow)">'
                f'<animateMotion dur="{dur:.1f}s" begin="{phase:.1f}s" repeatCount="indefinite" '
                f'path="{d}"/></circle>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Tensor Rails</title>
<desc id="desc">Open-source tools and services for running inference and training workloads.</desc>
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="12" cy="12" r="1.2" fill="{t["grid"]}" fill-opacity="{t["grid_op"]}"/>
  </pattern>
  <radialGradient id="gridfade" cx="{CX}" cy="{AY}" r="420" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#gridfade)"/></mask>
  <radialGradient id="glowp" cx="{PURPLE_AX + 40}" cy="{AY - 40}" r="240" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{p1}" stop-opacity="{t["glow_op"]}"/><stop offset="1" stop-color="{p1}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowb" cx="{BLUE_AX - 40}" cy="{AY - 40}" r="240" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{b1}" stop-opacity="{t["glow_op"]}"/><stop offset="1" stop-color="{b1}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="railp" x1="{left}" y1="40" x2="{CX}" y2="{H}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{p0}"/><stop offset=".55" stop-color="{p1}"/><stop offset="1" stop-color="{p2}"/>
  </linearGradient>
  <linearGradient id="railb" x1="{W}" y1="40" x2="{CX}" y2="{H}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{b0}"/><stop offset=".55" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/>
  </linearGradient>
  <linearGradient id="fadex" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="{left / W:.3f}" stop-color="#fff" stop-opacity="0"/>
    <stop offset="{(left + 110) / W:.3f}" stop-color="#fff"/>
    <stop offset="{(W - 110) / W:.3f}" stop-color="#fff"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="fadey" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
    <stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity=".12"/>
  </linearGradient>
  <mask id="fx"><rect width="{W}" height="{H}" fill="url(#fadex)"/></mask>
  <mask id="fy"><rect width="{W}" height="{H}" fill="url(#fadey)"/></mask>
  <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
    <feGaussianBlur stdDeviation="3.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="halo" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#gridmask)"/>
  <rect width="{W}" height="{H}" fill="url(#glowp)"/>
  <rect width="{W}" height="{H}" fill="url(#glowb)"/>
  <g mask="url(#fx)"><g mask="url(#fy)">
    <g fill="none" stroke-linecap="round" stroke-width="10" opacity="{t["halo_op"]}" filter="url(#halo)">
      <g stroke="url(#railp)">{"".join(paths_p)}</g>
      <g stroke="url(#railb)">{"".join(paths_b)}</g>
    </g>
    <g fill="none" stroke-linecap="round" stroke-width="3" opacity="{t["rail_op"]}">
      <g stroke="url(#railp)">{"".join(paths_p)}</g>
      <g stroke="url(#railb)">{"".join(paths_b)}</g>
    </g>
    <g color="{p1}">{"".join(n for n in nodes[0::2])}</g>
    <g color="{b1}">{"".join(n for n in nodes[1::2])}</g>
  </g></g>
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif">
    <text x="80" y="166" font-size="68" font-weight="700" letter-spacing="-1.6" fill="{t["title"]}">Tensor Rails</text>
    <text x="82" y="222" font-size="24" fill="{t["tagline"]}">Open-source tools and services</text>
    <text x="82" y="254" font-size="24" fill="{t["tagline"]}">for running inference and training workloads.</text>
  </g>
  {border}
</g>
</svg>
'''


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, t in THEMES.items():
        (out / f"banner-{name}.svg").write_text(svg(t))


if __name__ == "__main__":
    main()
