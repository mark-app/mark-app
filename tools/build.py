#!/usr/bin/env python3
"""Generates the MARK-APP profile artwork (light and dark) into ../assets.

Run: python3 tools/build.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'assets'
ORANGE = '#F6A548'
FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    'dark': {
        'bg': '#111111', 'panel': '#1A1A19', 'line': '#2C2C2A', 'ink': '#F4F4F2',
        'muted': '#A3A39E', 'dot': '#262624', 'term': '#0B0B0B',
    },
    'light': {
        'bg': '#FAFAF7', 'panel': '#FFFFFF', 'line': '#E6E4DD', 'ink': '#1D1D1B',
        'muted': '#6B6B66', 'dot': '#E9E7E0', 'term': '#1D1D1B',
    },
}

REDUCED_MOTION = '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }'


def logo_mark(x, y, size):
    """The round MARK-APP mark: orange circle with the white double lambda, traced from logo.png (693px)."""
    s = size / 693.0
    first = [(60, 488), (172, 180), (234, 180), (346, 488), (292, 488), (203, 236), (113, 488)]
    second = [(px + 286, py) for px, py in first]

    def poly(points):
        return ' '.join('%.1f,%.1f' % (x + px * s, y + py * s) for px, py in points)

    r = size / 2
    return (
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x + r, y + r, r, ORANGE)
        + '<polygon points="%s" fill="#FFFFFF"/>' % poly(first)
        + '<polygon points="%s" fill="#FFFFFF"/>' % poly(second)
    )


def wordmark(x, y, size, ink):
    """MARK-APP with the orange lambda A's of the logo."""
    o = '<tspan fill="%s">&#923;</tspan>' % ORANGE
    return (
        '<text x="%d" y="%d" font-family="%s" font-size="%d" font-weight="800" letter-spacing="2" fill="%s">'
        'M%sRK-%sPP</text>' % (x, y, FONT, size, ink, o, o)
    )


def svg(width, height, title, body, style=''):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="%s">\n'
        '<title>%s</title>\n<style>%s %s</style>\n%s\n</svg>\n'
        % (width, height, width, height, title, title, style, REDUCED_MOTION, body)
    )


def dot_grid(t, width, height):
    return (
        '<defs><pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="2" cy="2" r="1.3" fill="%s"/></pattern></defs>'
        '<rect width="%d" height="%d" rx="18" fill="%s"/>'
        '<rect width="%d" height="%d" rx="18" fill="url(#grid)"/>'
        % (t['dot'], width, height, t['bg'], width, height)
    )


def header(t):
    w, h = 1200, 380
    lines = [
        ('$ bin/console prestashop:module install macustombanner', '#F4F4F2'),
        ('&#10004; Install action on module macustombanner succeeded.', ORANGE),
        ('$ ./upgrade --from 1.6 --to 9.0 --zero-downtime', '#F4F4F2'),
        ('&#10004; Shop upgraded. SEO intact. Customers happy.', ORANGE),
    ]
    term = ''
    for i, (text, colour) in enumerate(lines):
        term += (
            '<text class="ln" style="animation-delay:%.1fs" x="740" y="%d" font-family="%s" font-size="12.5" fill="%s">%s</text>'
            % (0.6 + i * 0.9, 205 + i * 26, MONO, colour, text)
        )
    style = (
        '.ln { opacity: 0; animation: show .5s ease forwards; }'
        '@keyframes show { to { opacity: 1; } }'
        '.cursor { animation: blink 1s steps(1) infinite; }'
        '@keyframes blink { 50% { opacity: 0; } }'
        '.pulse { transform-origin: 150px 190px; animation: pulse 3.2s ease-in-out infinite; }'
        '@keyframes pulse { 0%, 100% { opacity: .0; transform: scale(1); } 50% { opacity: .35; transform: scale(1.18); } }'
        '.rise { opacity: 0; animation: rise .8s ease forwards; }'
        '@keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }'
    )
    body = (
        dot_grid(t, w, h)
        + '<circle class="pulse" cx="150" cy="190" r="96" fill="%s"/>' % ORANGE
        + logo_mark(70, 110, 160)
        + '<g class="rise">' + wordmark(270, 178, 64, t['ink']) + '</g>'
        + '<text class="rise" style="animation-delay:.2s" x="273" y="214" font-family="%s" font-size="17" font-weight="700" letter-spacing="6.5" fill="%s">EXPERTS IN PRESTASHOP</text>' % (FONT, t['muted'])
        + '<rect class="rise" style="animation-delay:.35s" x="273" y="240" width="56" height="5" rx="2.5" fill="%s"/>' % ORANGE
        + '<text class="rise" style="animation-delay:.45s" x="273" y="282" font-family="%s" font-size="16" fill="%s">Support &#183; Custom modules &#183; Webshops &#183; Upgrades &#183; SEO</text>' % (FONT, t['ink'])
        + '<text class="rise" style="animation-delay:.55s" x="273" y="308" font-family="%s" font-size="14" fill="%s">Since 2005 &#183; Beverwijk, the Netherlands</text>' % (FONT, t['muted'])
        # Terminal card
        + '<rect x="718" y="140" width="456" height="190" rx="12" fill="%s"/>' % t['term']
        + ''.join('<circle cx="%d" cy="162" r="5.5" fill="%s"/>' % (740 + i * 18, c) for i, c in enumerate(['#FF5F57', '#FEBC2E', ORANGE]))
        + '<text x="946" y="166" font-family="%s" font-size="11" fill="#77776F" text-anchor="middle">~/mark-app</text>' % MONO
        + term
        + '<rect class="cursor" x="740" y="298" width="8" height="15" fill="%s"/>' % ORANGE
    )
    return svg(w, h, 'MARK-APP, experts in PrestaShop', body, style)


def stats(t):
    w, h = 1200, 180
    cards = [
        ('20+', 'years of e-commerce', 'building and running webshops'),
        ('10+', 'years PrestaShop Expert', 'certified by PrestaShop'),
        ('1.6 &#8594; 9', 'upgrade path', 'zero downtime, SEO protected'),
    ]
    body = '<rect width="%d" height="%d" rx="18" fill="%s"/>' % (w, h, t['bg'])
    for i, (big, label, sub) in enumerate(cards):
        x = 24 + i * 392
        body += (
            '<g class="card" style="animation-delay:%.2fs">' % (i * 0.15)
            + '<rect x="%d" y="24" width="368" height="132" rx="14" fill="%s" stroke="%s"/>' % (x, t['panel'], t['line'])
            + '<rect x="%d" y="24" width="6" height="132" rx="3" fill="%s"/>' % (x, ORANGE)
            + '<text x="%d" y="88" font-family="%s" font-size="44" font-weight="800" fill="%s">%s</text>' % (x + 32, FONT, ORANGE, big)
            + '<text x="%d" y="116" font-family="%s" font-size="17" font-weight="700" fill="%s">%s</text>' % (x + 32, FONT, t['ink'], label)
            + '<text x="%d" y="138" font-family="%s" font-size="13.5" fill="%s">%s</text>' % (x + 32, FONT, t['muted'], sub)
            + '</g>'
        )
    style = '.card { opacity: 0; animation: up .7s ease forwards; } @keyframes up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }'
    return svg(w, h, '20+ years of e-commerce, 10+ years certified PrestaShop Expert, upgrades from 1.6 to 9', body, style)


def icon(kind, cx, cy, colour):
    """Simple line icons, 40px."""
    a = 'fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"' % colour
    x, y = cx - 20, cy - 20
    shapes = {
        'support': '<circle cx="%d" cy="%d" r="17" %s/><circle cx="%d" cy="%d" r="7" %s/>'
                   '<path d="M%d %d l7 7 M%d %d l-7 7 M%d %d l7 -7 M%d %d l-7 -7" %s/>'
                   % (cx, cy, a, cx, cy, a, x + 8, y + 8, x + 32, y + 8, x + 8, y + 32, x + 32, y + 32, a),
        'modules': '<path d="M%d %d l16 -9 l16 9 v18 l-16 9 l-16 -9 z M%d %d l16 9 l16 -9 M%d %d v18" %s/>'
                   % (x + 4, y + 11, x + 4, y + 11, cx, y + 20, a),
        'webshop': '<path d="M%d %d h6 l5 20 h18 l4 -14 h-25" %s/><circle cx="%d" cy="%d" r="2.6" %s/><circle cx="%d" cy="%d" r="2.6" %s/>'
                   % (x + 2, y + 6, a, x + 15, y + 33, a, x + 30, y + 33, a),
        'seo': '<circle cx="%d" cy="%d" r="11" %s/><path d="M%d %d l10 10 M%d %d l4 -5 l4 3 l5 -7" %s/>'
               % (x + 17, y + 17, a, x + 25, y + 25, x + 11, y + 20, a),
        'upgrade': '<circle cx="%d" cy="%d" r="17" %s/><path d="M%d %d v-18 M%d %d l8 -8 l8 8" %s/>'
                   % (cx, cy, a, cx, cy + 9, cx - 8, cy - 1, a),
        'migration': '<path d="M%d %d h26 l-6 -6 M%d %d h-26 l6 6" %s/>' % (x + 6, y + 14, x + 34, y + 26, a),
    }
    return shapes[kind]


def services(t):
    w, h = 1200, 300
    tiles = [
        ('support', 'PrestaShop support', 'Updates, errors and speed issues'),
        ('modules', 'Custom modules', 'Integrations, automation, features'),
        ('webshop', 'Webshops', 'Fast, usable and search friendly'),
        ('seo', 'SEO', 'Technical, content and loading speed'),
        ('upgrade', 'Upgrades &amp; updates', 'Safe and fully controlled'),
        ('migration', 'Webshop migration', 'Move to PrestaShop without losses'),
    ]
    body = '<rect width="%d" height="%d" rx="18" fill="%s"/>' % (w, h, t['bg'])
    for i, (kind, title, sub) in enumerate(tiles):
        col, row = i % 3, i // 3
        x, y = 24 + col * 392, 24 + row * 136
        body += (
            '<g class="tile" style="animation-delay:%.2fs">' % (i * 0.1)
            + '<rect x="%d" y="%d" width="368" height="116" rx="14" fill="%s" stroke="%s"/>' % (x, y, t['panel'], t['line'])
            + '<circle cx="%d" cy="%d" r="30" fill="%s" fill-opacity=".14"/>' % (x + 58, y + 58, ORANGE)
            + icon(kind, x + 58, y + 58, ORANGE)
            + '<text x="%d" y="%d" font-family="%s" font-size="18" font-weight="700" fill="%s">%s</text>' % (x + 108, y + 52, FONT, t['ink'], title)
            + '<text x="%d" y="%d" font-family="%s" font-size="13.5" fill="%s">%s</text>' % (x + 108, y + 76, FONT, t['muted'], sub)
            + '</g>'
        )
    style = '.tile { opacity: 0; animation: up .6s ease forwards; } @keyframes up { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }'
    return svg(w, h, 'Services: PrestaShop support, custom modules, webshops, SEO, upgrades and migration', body, style)


def upgrade_path(t):
    w, h = 1200, 220
    nodes = [('1.6', 150), ('1.7', 450), ('8', 750), ('9', 1050)]
    body = (
        '<rect width="%d" height="%d" rx="18" fill="%s"/>' % (w, h, t['bg'])
        + '<text x="60" y="52" font-family="%s" font-size="20" font-weight="800" fill="%s">The upgrade path</text>' % (FONT, t['ink'])
        + '<text x="60" y="78" font-family="%s" font-size="14" fill="%s">Step by step through every major PrestaShop version, with zero downtime and full SEO protection.</text>' % (FONT, t['muted'])
        + '<line x1="150" y1="140" x2="1050" y2="140" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % ORANGE
        # Drawn below the nodes so it passes behind each version like a train through stations.
        + '<circle class="runner" cx="150" cy="140" r="9" fill="%s" stroke="%s" stroke-width="4"/>' % (t['panel'], ORANGE)
    )
    for i, (label, x) in enumerate(nodes):
        body += (
            '<circle class="glow" style="animation-delay:%.2fs" cx="%d" cy="140" r="22" fill="%s"/>' % (i * 1.0, x, ORANGE)
            + '<circle cx="%d" cy="140" r="22" fill="%s"/>' % (x, ORANGE)
            + '<text x="%d" y="146" font-family="%s" font-size="16" font-weight="800" fill="#1D1D1B" text-anchor="middle">%s</text>' % (x, FONT, label)
            + '<text x="%d" y="190" font-family="%s" font-size="12.5" fill="%s" text-anchor="middle">PrestaShop %s</text>' % (x, FONT, t['muted'], label)
        )
    style = (
        '.runner { animation: run 4s ease-in-out infinite; }'
        '@keyframes run { 0% { transform: translateX(0); } 75%, 100% { transform: translateX(900px); } }'
        '.glow { opacity: 0; transform-box: fill-box; transform-origin: center; animation: glow 4s ease-out infinite; }'
        '@keyframes glow { 0% { opacity: .45; transform: scale(1); } 25%, 100% { opacity: 0; transform: scale(1.8); } }'
    )
    return svg(w, h, 'Upgrade path: PrestaShop 1.6 to 1.7 to 8 to 9', body, style)


def footer(t):
    w, h = 1200, 140
    body = (
        '<rect width="%d" height="%d" rx="18" fill="%s"/>' % (w, h, ORANGE)
        + '<path class="wave" d="M0 110 Q 150 80 300 110 T 600 110 T 900 110 T 1200 110 T 1500 110 T 1800 110 V140 H0 Z" fill="#FFFFFF" fill-opacity=".16"/>'
        + logo_mark(40, 30, 80).replace('fill="%s"' % ORANGE, 'fill="#1D1D1B"', 1)
        + '<text x="146" y="68" font-family="%s" font-size="26" font-weight="800" fill="#1D1D1B">Any questions? Please contact MARK-APP.</text>' % FONT
        + '<text x="146" y="98" font-family="%s" font-size="15" fill="#1D1D1B">mark-app.com &#183; info@mark-app.com &#183; Monday to Friday 09:00&#8211;17:30</text>' % FONT
        + '<g transform="translate(1100 70)"><circle r="30" fill="#1D1D1B"/><path d="M-9 -1 h18 M2 -9 l8 8 l-8 8" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>' % ORANGE
    )
    style = '.wave { animation: drift 8s linear infinite; } @keyframes drift { to { transform: translateX(-600px); } }'
    return svg(w, h, 'Any questions? Please contact MARK-APP.', body, style)


def main():
    OUT.mkdir(exist_ok=True)
    for name, build in [('header', header), ('stats', stats), ('services', services), ('upgrade-path', upgrade_path)]:
        for theme, colours in THEMES.items():
            (OUT / ('%s-%s.svg' % (name, theme))).write_text(build(colours), encoding='utf-8')
    # The footer is orange in both themes.
    (OUT / 'footer.svg').write_text(footer(THEMES['light']), encoding='utf-8')
    print('written to', OUT)


if __name__ == '__main__':
    main()
