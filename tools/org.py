# DEIMOS · mission control for the age of agents. Builds every SVG on the deimos-hq org profile.
# Standard library only (the daily Action runs it). Real sky: the footer's TONIGHT panel asks NASA JPL Horizons
# where the moon Deimos actually is around Mars today.
import base64, datetime as dt, hashlib, json, math, os, pathlib, random, urllib.request
from xml.sax.saxutils import escape as esc

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / 'profile' / 'assets'
CAST = ROOT / 'cast'
BETA = dt.date(2026, 11, 10)
TODAY = dt.date.fromisoformat(os.environ.get('PROFILE_DAY', dt.date.today().isoformat()))
DAYS = (BETA - TODAY).days
W = 1280
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
VOID, STAR, RUST, PAPER, INKL = '#05040a', '#f2f0ea', '#c1440e', '#fbfaf7', '#141414'
GOLD, GREEN, PINK, CYAN, ORANGE = '#F7CD45', '#39ff88', '#ff2bd6', '#00e5ff', '#ff7a1a'
ACID = ['#ff2bd6', '#7a5cff', '#00e5ff', '#39ff88', '#fff23a', '#ff7a1a', '#ff2bd6']


def uid(*k):
    return hashlib.md5(repr(k).encode()).hexdigest()[:8]


def uri(p):
    p = pathlib.Path(p)
    mime = {'.webp': 'image/webp', '.png': 'image/png', '.svg': 'image/svg+xml'}[p.suffix]
    return f'data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}'


def text(x, y, s, size=16, col=STAR, op=1, font=MONO, weight=400, anchor='start', ls=0, extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" fill-opacity="{op}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{esc(s)}</text>')


DEFS = ('<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="22"/></filter>'
        '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix type="saturate" values="0"/>'
        '<feComponentTransfer><feFuncA type="table" tableValues="0 .06"/></feComponentTransfer></filter>')


def svg(w, h, body, label, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
            f'<defs>{DEFS}{defs}</defs>{body}</svg>')


def frame(h, light=False, rx=22):
    if light:
        marks = ''.join(f'<path d="M{x - 10},{y} h20 M{x},{y - 10} v20" stroke="{INKL}" stroke-opacity=".35"/>' for x, y in ((24, 24), (W - 24, 24), (24, h - 24), (W - 24, h - 24)))
        return f'<rect width="{W}" height="{h}" rx="{rx}" fill="{PAPER}"/><rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="{rx}" fill="none" stroke="{INKL}" stroke-opacity=".15"/>{marks}'
    return (f'<rect width="{W}" height="{h}" rx="{rx}" fill="{VOID}"/><rect width="{W}" height="{h}" rx="{rx}" filter="url(#grain)"/>'
            f'<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".12"/>')


def acid(attr, off=0, dur=9):
    v = ACID[off:] + ACID[1:off + 1] if off else ACID
    return f'<animate attributeName="{attr}" values="{";".join(v)}" dur="{dur}s" repeatCount="indefinite"/>'


def nebula(h, seed=1, op=.32):
    """Acid nebula: soft colour clouds that drift and slowly cycle hue, behind the dark sections."""
    r = random.Random(seed)
    k = uid('neb', h, seed)
    blobs = ''
    for i in range(5):
        x, y, rr = r.uniform(0, W), r.uniform(0, h), r.uniform(h * .45, h * .9)
        blobs += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr * 1.6:.0f}" ry="{rr * .7:.0f}" fill="{ACID[(i + seed) % 6]}">{acid("fill", (i + seed) % 6, 14 + i * 3)}'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;{r.randint(-80, 80)} {r.randint(-30, 30)};0 0" dur="{18 + i * 4}s" repeatCount="indefinite"/></ellipse>')
    return (f'<defs><filter id="nb{k}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
            f'<clipPath id="nc{k}"><rect width="{W}" height="{h}" rx="22"/></clipPath></defs>'
            f'<g clip-path="url(#nc{k})"><g filter="url(#nb{k})" opacity="{op}">{blobs}</g></g>')


def mark(cx, cy, s, col=STAR, node=None):
    node = node or col
    R = 154 * s
    v = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (-90, 150, 30)]
    return (f'<g fill="none" stroke="{col}" stroke-linejoin="round"><circle cx="{cx}" cy="{cy}" r="{R:.1f}" stroke-width="{8 * s:.2f}" stroke-opacity=".8"/>'
            f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in v)}" stroke-width="{7 * s:.2f}"/>'
            + ''.join(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke-width="{6 * s:.2f}"/>' for x, y in v) + '</g>'
            f'<g fill="{node}">' + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{19 * s:.1f}"/>' for x, y in v) + f'<circle cx="{cx}" cy="{cy}" r="{26.5 * s:.1f}"/></g>')


def stars(n, h, seed=7):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.choice((.6, .9, 1.3))}" fill="#fff">'
                   f'<animate attributeName="opacity" values=".15;.8;.15" dur="{r.uniform(3, 8):.1f}s" begin="{r.uniform(0, 5):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(n))


# ================================================================ S2 the missions: five embroidered patches
PATCHES = [('CLOCKFORD', GOLD, 'OVERSIGHT', 'rook'), ('RATCHET', GREEN, 'ONCE', 'gear'), ('CRIMP', PINK, 'ACCOUNTABLE', 'seal'),
           ('MARKLODE', CYAN, 'RECON', 'dossier'), ('M.A.X', ORANGE, 'BASELINE', 'line')]


def patch(i):
    name, col, mission, motif = PATCHES[i]
    S, c = 400, 200
    k = uid('patch', i)
    # satin fill = fine parallel lines at 30°, twill border = short dashes, merrowed edge = a thick wavy ring
    defs = (f'<pattern id="satin{k}" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><rect width="5" height="5" fill="#0e0c18"/><line x1="0" y1="0" x2="0" y2="5" stroke="#211d33" stroke-width="2.4"/></pattern>'
            f'<pattern id="thread{k}" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width="4" height="4" fill="{col}"/><line x1="0" y1="0" x2="0" y2="4" stroke="#000" stroke-opacity=".28" stroke-width="1.2"/></pattern>'
            f'<path id="top{k}" d="M{c - 140},{c} A140,140 0 0 1 {c + 140},{c}"/><path id="bot{k}" d="M{c - 148},{c} A148,148 0 0 0 {c + 148},{c}"/>'
            f'<linearGradient id="sheen{k}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="disc{k}"><circle cx="{c}" cy="{c}" r="186"/></clipPath>'
            f'<filter id="emb{k}" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="3" stdDeviation="2" flood-color="#000" flood-opacity=".6"/></filter>')
    body = (f'<circle cx="{c}" cy="{c}" r="194" fill="#000" opacity=".5" filter="url(#soft)"/>'
            f'<circle cx="{c}" cy="{c}" r="190" fill="url(#thread{k})"/>'                                            # merrowed edge
            f'<circle cx="{c}" cy="{c}" r="190" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="3" stroke-dasharray="2 3"/>'
            f'<circle cx="{c}" cy="{c}" r="194" fill="none" stroke="{ACID[i]}" stroke-width="3" opacity=".9">{acid("stroke", i, 8)}</circle>'
            f'<circle cx="{c}" cy="{c}" r="176" fill="url(#satin{k})"/>'
            f'<circle cx="{c}" cy="{c}" r="176" fill="none" stroke="{col}" stroke-width="6" stroke-dasharray="7 4" opacity=".9"/>'  # twill border
            f'<circle cx="{c}" cy="{c}" r="112" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="3 3" opacity=".6"/>'
            f'<text font-family="{SANS}" font-size="30" font-weight="900" letter-spacing="6" fill="{col}" filter="url(#emb{k})"><textPath href="#top{k}" startOffset="50%" text-anchor="middle">{esc(name)}</textPath></text>'
            f'<text font-family="{MONO}" font-size="17" font-weight="700" letter-spacing="7" fill="{STAR}" fill-opacity=".85"><textPath href="#bot{k}" startOffset="50%" text-anchor="middle" dominant-baseline="hanging">{esc(mission)}</textPath></text>'
            + ''.join(f'<circle cx="{c + 160 * math.cos(math.radians(a))}" cy="{c + 160 * math.sin(math.radians(a))}" r="4" fill="{STAR}"/>' for a in (180, 0)))
    g = f'<g filter="url(#emb{k})" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
    if motif == 'rook':
        img = CAST / 'rook.webp'
        if img.exists():
            defs += (f'<filter id="stitch{k}" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="0"/>'
                     f'<feComponentTransfer><feFuncR type="discrete" tableValues=".05 .55 .95"/><feFuncG type="discrete" tableValues=".05 .55 .95"/><feFuncB type="discrete" tableValues=".07 .6 1"/></feComponentTransfer></filter>')
            body += f'<image href="{uri(img)}" x="{c - 62}" y="{c - 92}" width="124" height="198" filter="url(#stitch{k})" preserveAspectRatio="xMidYMid meet"/>'
        motif_svg = ''
    elif motif == 'gear':
        n, r1, r2 = 12, 70, 54
        pts = ' '.join(f'{c + (r1 if j % 2 == 0 else r2) * math.cos(2 * math.pi * (j // 2 + (.5 if j % 2 else 0)) / n):.1f},{c - 8 + (r1 if j % 2 == 0 else r2) * math.sin(2 * math.pi * (j // 2 + (.5 if j % 2 else 0)) / n):.1f}' for j in range(n * 2))
        motif_svg = g + f'<polygon points="{pts}"/></g>' + text(c, c + 22, '1', 64, col, font=SANS, weight=900, anchor='middle', extra=f'filter="url(#emb{k})"')
    elif motif == 'seal':
        motif_svg = (f'<rect x="{c - 56}" y="{c - 70}" width="112" height="140" rx="6" fill="{STAR}" fill-opacity=".9"/>'
                     + ''.join(f'<line x1="{c - 40}" y1="{c - 46 + j * 18}" x2="{c + 40 - (j * 13) % 30}" y2="{c - 46 + j * 18}" stroke="#9a948a" stroke-width="5"/>' for j in range(5))
                     + f'<circle cx="{c + 34}" cy="{c + 44}" r="30" fill="{col}" filter="url(#emb{k})"/><circle cx="{c + 34}" cy="{c + 44}" r="21" fill="none" stroke="#7a0f57" stroke-width="3"/>')
    elif motif == 'dossier':
        motif_svg = (f'<rect x="{c - 70}" y="{c - 60}" width="140" height="122" rx="8" fill="#14202a" stroke="{col}" stroke-width="5"/>'
                     + ''.join(f'<rect x="{c - 64 + j * 34}" y="{c - 76}" width="30" height="18" rx="4" fill="{col}" opacity="{1 if j == 3 else .45}"/>' for j in range(4))
                     + f'<g transform="rotate(-10 {c} {c + 10})"><rect x="{c - 50}" y="{c - 4}" width="100" height="34" rx="4" fill="none" stroke="{col}" stroke-width="5"/>'
                     + text(c, c + 20, 'VERDICT', 16, col, weight=900, anchor='middle', ls=2) + '</g>')
    else:
        rr = random.Random(5)
        pts = ' '.join(f'{c - 80 + j * 8},{c + rr.uniform(-6, 6) + (-38 if j in (13, 14) else 0):.0f}' for j in range(21))
        motif_svg = (f'<rect x="{c - 86}" y="{c - 16}" width="172" height="32" rx="8" fill="{col}" fill-opacity=".18"/>'
                     + g.replace('stroke-width="7"', 'stroke-width="5"').replace(f'stroke="{col}"', f'stroke="{STAR}"') + f'<polyline points="{pts}"/></g>'
                     + f'<circle cx="{c + 28}" cy="{c - 38}" r="11" fill="none" stroke="{col}" stroke-width="4"/>')
    body += motif_svg
    body += (f'<g clip-path="url(#disc{k})"><rect x="-200" y="0" width="160" height="{S}" fill="url(#sheen{k})" transform="skewX(-18)">'
             f'<animate attributeName="x" values="-260;-260;560;560" keyTimes="0;{i * .12:.2f};{i * .12 + .22:.2f};1" dur="9s" repeatCount="indefinite"/></rect></g>')
    labels = {'CLOCKFORD': 'see, approve and stop your AI agents from your phone. Patent pending; private beta 10 November 2026',
              'RATCHET': 'the effect gate for AI agents: a retried charge, deploy or email happens at most once',
              'CRIMP': 'open-source decision gate: the decision withdraws itself when a fact breaks; patent pending',
              'MARKLODE': 'startup diligence before the pitch, in 24 to 72 hours', 'M.A.X': 'offline-first behavioral analysis against each person’s own baseline'}
    return svg(S, S, body, f'{name.title() if name != "M.A.X" else name} mission patch: {labels[name]}.', defs)


# ================================================================ S3 the mission board (live)
def board():
    H = 380
    rows = [('CLOCKFORD', GOLD, 'PRIVATE BETA', f'T–{DAYS} DAYS · PATENT PENDING' if DAYS > 0 else 'LIFTOFF · PATENT PENDING'),
            ('RATCHET', GREEN, 'LIVE', '1,000 EFFECTS / MONTH FREE · OPENSSF SILVER'),
            ('CRIMP', PINK, 'OPEN SOURCE', 'PATENT PENDING · OPENSSF SILVER'),
            ('MARKLODE', CYAN, 'TAKING IDEAS', '24–72 H'),
            ('M.A.X', ORANGE, 'IN THE LAB', 'OFFLINE-FIRST')]
    body = frame(H) + nebula(H, 2, .22) + text(48, 56, f'MISSION BOARD · {TODAY.strftime("%d %b %Y").upper()} · UTC', 13, STAR, .55, ls=5)
    body += f'<line x1="48" y1="74" x2="{W - 48}" y2="74" stroke="#fff" stroke-opacity=".08"/>'
    for i, (n, col, st, info) in enumerate(rows):
        y = 118 + i * 50
        body += (f'<circle cx="62" cy="{y - 6}" r="7" fill="{col}"><animate attributeName="opacity" values="1;.3;1" dur="{3 + i * .5:.1f}s" repeatCount="indefinite"/></circle>'
                 + text(86, y, n, 20, col, weight=700, ls=3) + text(270, y, '▸ ' + st, 18, STAR, .9, ls=2) + text(476, y, info, 13, STAR, .6, ls=.3))
    # the big countdown, seven-segment style
    big = f'T–{DAYS}' if DAYS > 0 else 'LIFTOFF'
    body += (f'<rect x="{W - 360}" y="96" width="312" height="216" rx="14" fill="#0b0a12" stroke="{RUST}" stroke-opacity=".5"/>'
             + text(W - 204, 132, 'CLOCKFORD · PRIVATE BETA', 12, RUST, .9, anchor='middle', ls=3)
             + text(W - 204, 236, big, 92 if DAYS > 0 else 54, GOLD, font=MONO, weight=900, anchor='middle', extra='filter="url(#glow)"')
             + text(W - 204, 286, 'DAYS TO 10 NOV 2026' if DAYS > 0 else 'BETA IS OPEN', 13, STAR, .6, anchor='middle', ls=3))
    body += (f'<rect x="0" y="80" width="{W}" height="2" fill="{RUST}" opacity=".35"><animate attributeName="y" values="80;{H - 30};80" dur="6s" repeatCount="indefinite"/></rect>')
    return svg(W, H, body, f'Mission board: Clockford private beta {"in " + str(DAYS) + " days" if DAYS > 0 else "is open"}; Ratchet live; Crimp open source; Marklode taking ideas; M.A.X in the lab.')


# ================================================================ S4 flight rules
def rules(light=False):
    H = 560
    ink, paper = (INKL, PAPER) if light else (STAR, '#0d0c14')
    body = frame(H, light)
    px, py, pw, ph = 170, 46, 940, 470
    body += (f'<rect x="{px + 10}" y="{py + 14}" width="{pw}" height="{ph}" rx="6" fill="#000" opacity="{.08 if light else .5}" filter="url(#soft)"/>'
             f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="{"#ffffff" if light else paper}" stroke="{ink}" stroke-opacity=".18"/>'
             f'<rect x="{px}" y="{py}" width="{pw}" height="46" rx="6" fill="{ink}" opacity=".9"/>'
             + text(px + 26, py + 30, 'DEIMOS AI LLC · FLIGHT RULES · REV A', 15, "#ffffff" if light else VOID, weight=700, ls=4)
             + mark(px + pw - 40, py + 23, .08, "#ffffff" if light else VOID))
    rl = [('FR-1', 'People stay in charge of what matters.'), ('FR-2', 'Assume something is already inside.'), ('FR-3', 'If it matters, make it provable.'), ('FR-4', 'Bend, don’t break.')]
    for i, (n, r) in enumerate(rl):
        y = py + 120 + i * 78
        t = .4 + i * 1.0
        body += (f'<line x1="{px + 30}" y1="{y + 22}" x2="{px + pw - 30}" y2="{y + 22}" stroke="{ink}" stroke-opacity=".12"/>'
                 + text(px + 34, y, n, 15, RUST, weight=700, ls=2)
                 + f'<clipPath id="fr{i}{int(light)}"><rect x="{px + 120}" y="{y - 30}" height="40" width="0"><animate attributeName="width" from="0" to="760" begin="{t:.1f}s" dur=".9s" fill="freeze"/></rect></clipPath>'
                 + f'<g clip-path="url(#fr{i}{int(light)})">' + text(px + 120, y, r, 28, ink, font=SANS, weight=900) + '</g>')
    body += text(px + 34, py + ph - 26, 'Written before the launch. Followed during it.', 14, ink, .6, extra='font-style="italic"')
    body += (f'<g opacity="0" transform="rotate(-9 {px + pw - 160} {py + ph - 70})"><animate attributeName="opacity" values="0;1" begin="4.6s" dur=".05s" fill="freeze"/>'
             f'<animateTransform attributeName="transform" type="scale" additive="sum" values="1.35;1" begin="4.6s" dur=".18s" fill="freeze"/>'
             f'<rect x="{px + pw - 270}" y="{py + ph - 100}" width="220" height="60" rx="6" fill="none" stroke="{RUST}" stroke-width="5" opacity=".85"/>'
             + text(px + pw - 160, py + ph - 58, 'APPROVED', 30, RUST, weight=900, anchor='middle', ls=6, op=.85) + '</g>')
    return svg(W, H, body, 'Flight rules: FR-1 people stay in charge of what matters; FR-2 assume something is already inside; FR-3 if it matters, make it provable; FR-4 bend, don’t break.')


# ================================================================ S5 named for dread: the transit
def dread():
    H = 440
    cyc = 12
    defs = (f'<radialGradient id="planet" cx=".35" cy=".25" r=".9"><stop offset="0" stop-color="#e2733a"/><stop offset=".45" stop-color="{RUST}"/><stop offset=".85" stop-color="#3a1206"/><stop offset="1" stop-color="#140603"/></radialGradient>'
            f'<radialGradient id="atmo" cx=".5" cy=".5" r=".5"><stop offset=".86" stop-color="#ff7a3a" stop-opacity="0"/><stop offset=".93" stop-color="#ff7a3a" stop-opacity=".55"/><stop offset="1" stop-color="#ff7a3a" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="pl"><circle cx="{W / 2}" cy="1180" r="900"/></clipPath><clipPath id="dc"><rect width="{W}" height="{H}" rx="22"/></clipPath>')
    moon = (f'<path d="M-26,-4 C-24,-20 -6,-24 8,-20 C24,-16 30,-2 26,10 C20,24 0,26 -12,20 C-24,14 -28,8 -26,-4Z" fill="#2b2622"/>'
            f'<circle cx="-6" cy="-6" r="4" fill="#1b1714"/><circle cx="10" cy="6" r="3" fill="#1b1714"/>')
    body = (f'<g clip-path="url(#dc)"><rect width="{W}" height="{H}" fill="{VOID}"/>{nebula(H, 4, .30)}{stars(110, H, 11)}'
            f'<circle cx="{W / 2}" cy="1180" r="960" fill="url(#atmo)"><animate attributeName="opacity" values="1;1;.7;1;1" keyTimes="0;.35;.5;.65;1" dur="{cyc}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{W / 2}" cy="1180" r="900" fill="url(#planet)"><animate attributeName="opacity" values="1;1;.72;1;1" keyTimes="0;.35;.5;.65;1" dur="{cyc}s" repeatCount="indefinite"/></circle>'
            f'<g clip-path="url(#pl)"><ellipse cx="0" cy="300" rx="60" ry="24" fill="#000" opacity=".45" filter="url(#soft)"><animate attributeName="cx" values="-200;{W + 200}" dur="{cyc}s" repeatCount="indefinite"/></ellipse></g>'
            f'<g><animateMotion path="M-60,250 Q{W / 2},228 {W + 60},262" dur="{cyc}s" repeatCount="indefinite"/><g transform="scale(1.6)">{moon}</g></g>')
    lines = [('DEIMOS.', 54, STAR, 900, SANS, 92), ('Greek: dread.', 16, STAR, 400, MONO, 124), ('We were named for it.', 30, STAR, 900, SANS, 176), ('We build so you never feel it.', 30, RUST, 900, SANS, 216)]
    for j, (s, size, col, wt, font, y) in enumerate(lines):
        a = .66 + j * .06
        body += (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a:.2f};{a + .06:.2f};.97;1" dur="{cyc}s" repeatCount="indefinite"/>'
                 + text(W / 2, y, s, size, col, font=font, weight=wt, anchor='middle', ls=(8 if j == 0 else 1)) + '</g>')
    body += text(W / 2, H - 28, 'Agents never sleep. Something has to keep watch.', 14, STAR, .55, anchor='middle', extra='font-style="italic"')
    body += f'</g><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="#fff" stroke-opacity=".12"/>'
    return svg(W, H, body, 'Named for dread: the moon Deimos crosses Mars. We were named for it. We build so you never feel it.', defs)


# ================================================================ S6 the open hatch (Crimp)
def hatch():
    H, cx, cy = 320, 230, 160
    cyc = 10
    bolts = ''.join(f'<g transform="rotate({a} {cx} {cy})"><rect x="{cx - 9}" y="{cy - 124}" width="18" height="34" rx="4" fill="#3a3646">'
                    f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -14;0 -14;0 0" keyTimes="0;{.05 + i * .04:.2f};{.09 + i * .04:.2f};.9;1" dur="{cyc}s" repeatCount="indefinite"/></rect></g>'
                    for i, a in enumerate((0, 90, 180, 270)))
    door = (f'<g><circle cx="{cx}" cy="{cy}" r="96" fill="#1c1a24" stroke="#4a4558" stroke-width="6"/><circle cx="{cx}" cy="{cy}" r="64" fill="none" stroke="#4a4558" stroke-width="3"/>'
            f'<rect x="{cx - 50}" y="{cy - 6}" width="100" height="12" rx="6" fill="#4a4558"/>'
            f'<animateTransform attributeName="transform" type="scale" values="1 1;1 1;.22 1;.22 1;1 1" keyTimes="0;.3;.42;.9;1" dur="{cyc}s" repeatCount="indefinite" additive="sum"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{cx * .78 - 70} 0;{cx * .78 - 70} 0;0 0" keyTimes="0;.3;.42;.9;1" dur="{cyc}s" repeatCount="indefinite" additive="sum"/></g>')
    light = (f'<circle cx="{cx}" cy="{cy}" r="96" fill="{PINK}" opacity="0" filter="url(#soft)"><animate attributeName="opacity" values="0;0;.75;.75;0" keyTimes="0;.32;.45;.9;1" dur="{cyc}s" repeatCount="indefinite"/></circle>'
             f'<circle cx="{cx}" cy="{cy}" r="92" fill="url(#inside)"/>')
    ring = f'<circle cx="{cx}" cy="{cy}" r="128" fill="none" stroke="#2b2836" stroke-width="22"/>' + bolts
    spill = f'<polygon points="{cx + 90},{cy - 70} {W - 40},40 {W - 40},{H - 40} {cx + 90},{cy + 70}" fill="{PINK}" opacity="0"><animate attributeName="opacity" values="0;0;.07;.07;0" keyTimes="0;.32;.45;.9;1" dur="{cyc}s" repeatCount="indefinite"/></polygon>'
    copy = (text(420, 96, 'CRIMP IS OPEN.', 40, PINK, font=SANS, weight=900, ls=2)
            + text(422, 136, 'An open-source decision gate for AI agents: agents submit the rule and', 16, STAR, .88)
            + text(422, 160, 'the facts, not a conclusion. When a fact breaks, the decision withdraws itself.', 16, STAR, .88)
            + text(422, 192, 'In 2022, 83% of appealed Medicare Advantage prior-auth denials were overturned.', 13, STAR, .55, extra='font-style="italic"'))
    x = 422
    for t in ('OPEN SOURCE', 'PATENT PENDING', 'OPENSSF SILVER'):
        w = 20 + len(t) * 8.4
        copy += f'<rect x="{x}" y="{H - 82}" width="{w:.0f}" height="28" rx="14" fill="none" stroke="{PINK}" stroke-opacity=".6"/>' + text(x + w / 2, H - 63, t, 11, PINK, anchor='middle', ls=1.5)
        x += w + 10
    return svg(W, H, frame(H) + spill + light + door + ring + copy, 'Crimp is open: an open-source decision gate for AI agents; when a fact breaks, the decision withdraws itself.', f'<radialGradient id="inside"><stop offset="0" stop-color="#ffe3f7"/><stop offset=".6" stop-color="{PINK}" stop-opacity=".55"/><stop offset="1" stop-color="#2a0f24"/></radialGradient>')


# ================================================================ S7 boarding: the Clockford beta pass (the one stowaway wolf)
def boarding(light=False):
    H = 360
    ink = INKL if light else STAR
    bg = '#ffffff' if light else '#0c0b14'
    x0, y0, pw, ph, stub = 120, 80, 1040, 230, 270
    body = frame(H, light) + text(W / 2, 48, 'NOW BOARDING.', 22, ink, font=SANS, weight=900, anchor='middle', ls=8)
    body += (f'<rect x="{x0 + 8}" y="{y0 + 12}" width="{pw}" height="{ph}" rx="18" fill="#000" opacity="{.08 if light else .5}" filter="url(#soft)"/>'
             f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" rx="18" fill="{bg}" stroke="{ink}" stroke-opacity=".2"/>'
             f'<rect x="{x0}" y="{y0}" width="{pw - stub}" height="44" rx="18" fill="{GOLD}"/><rect x="{x0}" y="{y0 + 24}" width="{pw - stub}" height="20" fill="{GOLD}"/>'
             + text(x0 + 28, y0 + 30, 'DEIMOS AI · BOARDING PASS', 15, VOID, weight=900, ls=4) + mark(x0 + pw - stub - 30, y0 + 22, .08, VOID))
    fields = [('PASSENGER', 'YOU'), ('FLIGHT', 'CLOCKFORD'), ('DEPARTS', '10 NOV 2026'), ('GATE', 'clockford.com'), ('CLASS', 'PRIVATE BETA'),
              ('BOARDING IN', f'{DAYS} DAYS' if DAYS > 0 else 'NOW')]
    for i, (k, v) in enumerate(fields):
        fx, fy = x0 + 30 + (i % 3) * 250, y0 + 90 + (i // 3) * 74
        body += text(fx, fy, k, 11, ink, .5, ls=3) + text(fx, fy + 30, v, 24, GOLD if k == 'BOARDING IN' else ink, font=SANS, weight=900)
    sx = x0 + pw - stub
    body += (f'<g><line x1="{sx}" y1="{y0 + 10}" x2="{sx}" y2="{y0 + ph - 10}" stroke="{ink}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="2 7"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;1 0;0 0" keyTimes="0;.9;.92;1" dur="8s" repeatCount="indefinite"/></g>')
    # holographic foil strip on the stub
    body += (f'<defs><linearGradient id="foil{int(light)}" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{RUST}"><animate attributeName="stop-color" values="{RUST};{GOLD};{PINK};{CYAN};{RUST}" dur="8s" repeatCount="indefinite"/></stop>'
             f'<stop offset="1" stop-color="{GOLD}"><animate attributeName="stop-color" values="{GOLD};{PINK};{CYAN};{RUST};{GOLD}" dur="8s" repeatCount="indefinite"/></stop></linearGradient></defs>'
             f'<rect x="{sx + 24}" y="{y0 + 24}" width="20" height="{ph - 48}" rx="4" fill="url(#foil{int(light)})" opacity=".85"/>'
             + text(sx + 70, y0 + 60, 'CLOCKFORD', 18, ink, font=SANS, weight=900, ls=2) + text(sx + 70, y0 + 86, '10 NOV 2026', 13, ink, .7, ls=2)
             + text(sx + 70, y0 + 112, 'PRIVATE BETA', 13, GOLD, weight=700, ls=2))
    # the barcode
    r = random.Random(3)
    bx = sx + 70
    while bx < x0 + pw - 30:
        w_ = r.choice((1.5, 2, 3, 4)); body += f'<rect x="{bx:.1f}" y="{y0 + 134}" width="{w_}" height="40" fill="{ink}" opacity=".8"/>'; bx += w_ + r.choice((1.5, 2, 3))
    # the stowaway: one tiny embroidered wolf patch and his crew line
    wimg = CAST / 'wolf-loaf.webp'
    if wimg.exists():
        cx_, cy_ = sx + 100, y0 + ph - 30
        body += (f'<defs><clipPath id="wp{int(light)}"><circle cx="{cx_}" cy="{cy_}" r="20"/></clipPath></defs>'
                 f'<circle cx="{cx_}" cy="{cy_}" r="23" fill="{GOLD}"/><circle cx="{cx_}" cy="{cy_}" r="23" fill="none" stroke="#000" stroke-opacity=".3" stroke-dasharray="2 2"/>'
                 f'<image href="{uri(wimg)}" x="{cx_ - 26}" y="{cy_ - 18}" width="52" height="42" clip-path="url(#wp{int(light)})"/>'
                 + text(cx_ + 32, cy_ + 5, 'CREW: 1 WOLF · CHEESE DECLARED', 10.5, ink, .75, ls=1))
    body += text(W / 2, H - 20, 'See, approve and stop your AI agents from your phone, whichever company built them.', 14, ink, .65, anchor='middle')
    return svg(W, H, body, f'Boarding pass for the Clockford private beta: departs 10 November 2026; boarding in {DAYS} days.')


# ================================================================ S8 mission log + TONIGHT (the real Deimos, from JPL Horizons)
def deimos_angle():
    cache = A / 'tonight.json'
    url = ("https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='402'&CENTER='500@499'&EPHEM_TYPE='VECTORS'"
           f"&START_TIME='{TODAY.isoformat()}'&STOP_TIME='{(TODAY + dt.timedelta(days=1)).isoformat()}'&STEP_SIZE='1%20d'&VEC_TABLE='1'&OUT_UNITS='KM-S'&OBJ_DATA='NO'")
    try:
        r = json.load(urllib.request.urlopen(url, timeout=30))['result']
        seg = r[r.index('$$SOE'):r.index('$$EOE')]
        import re
        x, y = (float(v) for v in re.search(r'X =\s*([-\d.E+]+)\s*Y =\s*([-\d.E+]+)', seg).groups())
        data = {'day': TODAY.isoformat(), 'angle': math.degrees(math.atan2(y, x)), 'x': x, 'y': y}
        cache.write_text(json.dumps(data))
        return data
    except Exception as e:
        print('horizons: keeping yesterday', e)
        return json.loads(cache.read_text()) if cache.exists() else None


def log(light=False):
    H = 260
    ink = INKL if light else STAR
    body = frame(H, light)
    # ground track
    pts = ' '.join(f'{40 + i * 6},{150 + 46 * math.sin(i / 14):.1f}' for i in range(150))
    L = 960
    body += (f'<polyline points="{pts}" fill="none" stroke="{RUST}" stroke-width="2.5" stroke-dasharray="{L}" stroke-dashoffset="{L}" opacity=".85">'
             f'<animate attributeName="stroke-dashoffset" values="{L};0;0" keyTimes="0;.85;1" dur="10s" repeatCount="indefinite"/></polyline>'
             f'<g><animateMotion path="M{pts.replace(" ", " L")}" dur="10s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear"/>{mark(0, 0, .06, ink)}</g>')
    lines = [f'LOG {TODAY.strftime("%d %b %Y").upper()} · board refreshed · all missions nominal', 'FOUNDED BY THE ARCHITECT & PRIMETIME',
             'LINEAGE · co-producer, Gaming Wall St (HBO Max, 2022) · deimoscore.com']
    body += ''.join(text(48, 48 + i * 24, l, 13, ink, .7 if i else .9, ls=1) for i, l in enumerate(lines))
    body += text(48, H - 30, 'DEIMOS AI LLC · KEEPING WATCH.', 26, ink, font=SANS, weight=900, ls=4)
    # TONIGHT: Mars, Deimos's orbit and the moon at its real angle today
    t = deimos_angle()
    ox, oy, orr = W - 170, 140, 66
    body += (f'<rect x="{ox - 130}" y="24" width="260" height="212" rx="14" fill="{"#ffffff" if light else "#0b0a12"}" stroke="{RUST}" stroke-opacity=".4"/>'
             + text(ox, 46, 'TONIGHT', 13, RUST, weight=700, anchor='middle', ls=5)
             + f'<circle cx="{ox}" cy="{oy}" r="{orr}" fill="none" stroke="{ink}" stroke-opacity=".25" stroke-dasharray="3 5"/>'
             f'<circle cx="{ox}" cy="{oy}" r="20" fill="{RUST}"/>' + text(ox, oy + 4, 'MARS', 8, '#fff', weight=700, anchor='middle', ls=1))
    if t:
        a = math.radians(t['angle'])
        mx, my = ox + orr * math.cos(a), oy - orr * math.sin(a)
        body += (f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="7" fill="{ink}"/><circle cx="{mx:.1f}" cy="{my:.1f}" r="7" fill="none" stroke="{ink}" stroke-width="1.5">'
                 f'<animate attributeName="r" values="7;18" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>'
                 + text(ox, 222, f'DEIMOS · {t["angle"] % 360:.0f}° · SOURCE: JPL HORIZONS · {t["day"]}', 8.5, ink, .6, anchor='middle', ls=.5))
    return svg(W, H, body, f'Mission log: Deimos AI LLC, founded by The Architect and PrimeTime. Tonight: the moon Deimos at its real position around Mars, from NASA JPL Horizons.')


# ================================================================ THE AGENCY: a NASA-meatball-style emblem for Deimos
def agency():
    S, c = 560, 280
    r = random.Random(21)
    defs = (f'<radialGradient id="ag"><stop offset="0" stop-color="#14112a"/><stop offset=".75" stop-color="#07060f"/><stop offset="1" stop-color="{VOID}"/></radialGradient>'
            f'<linearGradient id="vec" x1="0" x2="1"><stop offset="0" stop-color="{PINK}">{acid("stop-color", 0, 7)}</stop><stop offset=".5" stop-color="{CYAN}">{acid("stop-color", 2, 7)}</stop><stop offset="1" stop-color="{GOLD}">{acid("stop-color", 4, 7)}</stop></linearGradient>'
            f'<path id="agtop" d="M{c - 222},{c} A222,222 0 0 1 {c + 222},{c}"/><path id="agbot" d="M{c - 236},{c} A236,236 0 0 0 {c + 236},{c}"/>'
            f'<clipPath id="agc"><circle cx="{c}" cy="{c}" r="200"/></clipPath>')
    stars_ = ''.join(f'<circle cx="{c + r.uniform(-190, 190):.0f}" cy="{c + r.uniform(-190, 190):.0f}" r="{r.choice((1, 1.4, 2))}" fill="#fff"><animate attributeName="opacity" values=".2;1;.2" dur="{r.uniform(2, 6):.1f}s" begin="{r.uniform(0, 4):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(60))
    # the vector: an acid chevron sweeping across the disc (NASA's red vector, made psychedelic)
    vec = (f'<path d="M{c - 200},{c + 120} C{c - 60},{c + 40} {c + 40},{c - 60} {c + 230},{c - 150} L{c + 214},{c - 112} C{c + 40},{c - 20} {c - 40},{c + 70} {c - 190},{c + 150} Z" fill="url(#vec)" opacity=".92"/>')
    orbit = (f'<ellipse cx="{c}" cy="{c}" rx="178" ry="62" fill="none" stroke="#fff" stroke-width="3" transform="rotate(-24 {c} {c})"/>'
             f'<g transform="rotate(-24 {c} {c})"><circle r="9" fill="#fff" filter="url(#glow)"><animateMotion dur="7s" repeatCount="indefinite" path="M{c - 178},{c} a178,62 0 1,0 356,0 a178,62 0 1,0 -356,0"/></circle></g>')
    body = (f'<circle cx="{c}" cy="{c}" r="268" fill="#000" opacity=".55" filter="url(#soft)"/>'
            f'<circle cx="{c}" cy="{c}" r="262" fill="{VOID}" stroke="#fff" stroke-opacity=".9" stroke-width="4"/>'
            f'<circle cx="{c}" cy="{c}" r="252" fill="none" stroke="url(#vec)" stroke-width="3"/>'
            f'<circle cx="{c}" cy="{c}" r="200" fill="url(#ag)" stroke="#fff" stroke-width="3"/>'
            f'<g clip-path="url(#agc)">{stars_}{vec}<circle cx="{c + 150}" cy="{c + 190}" r="120" fill="{RUST}"/><circle cx="{c + 150}" cy="{c + 190}" r="120" fill="none" stroke="#ff8a4a" stroke-width="6" opacity=".6"/></g>'
            + orbit + f'<g filter="url(#glow)">{mark(c, c - 6, .52)}</g>'
            f'<text font-family="{SANS}" font-size="40" font-weight="900" letter-spacing="14" fill="#fff"><textPath href="#agtop" startOffset="50%" text-anchor="middle">DEIMOS AI</textPath></text>'
            f'<text font-family="{MONO}" font-size="17" font-weight="700" letter-spacing="9" fill="#fff" fill-opacity=".85"><textPath href="#agbot" startOffset="50%" text-anchor="middle" dominant-baseline="hanging">CUSTODIMUS · WE KEEP WATCH</textPath></text>'
            + ''.join(f'<circle cx="{c + 236 * math.cos(math.radians(a))}" cy="{c + 236 * math.sin(math.radians(a))}" r="5" fill="#fff"/>' for a in (180, 0)))
    return svg(S, S, body, 'The Deimos AI emblem: the Deimos mark in orbit over Mars, an acid vector across a field of stars; motto: Custodimus, we keep watch.', defs)


# ================================================================ GO / NO-GO: the flight director's poll
def poll():
    H, cyc = 360, 16
    stations = [('CLOCKFORD', 'OVERSIGHT', GOLD), ('RATCHET', 'EFFECTS', GREEN), ('CRIMP', 'DECISIONS', PINK), ('MARKLODE', 'RECON', CYAN), ('M.A.X', 'BASELINE', ORANGE)]
    body = frame(H) + nebula(H, 6, .2) + text(48, 54, 'FLIGHT DIRECTOR · GO / NO-GO FOR LAUNCH', 14, STAR, .6, ls=5)
    body += text(W - 48, 54, f'T–{DAYS} · 10 NOV 2026' if DAYS > 0 else 'LIFTOFF', 14, GOLD, .9, anchor='end', ls=4)
    cw, gap, x0, y0 = 220, 20, 50, 90
    for i, (n, role, col) in enumerate(stations):
        x = x0 + i * (cw + gap)
        a = (1.2 + i * 1.6) / cyc
        body += (f'<rect x="{x}" y="{y0}" width="{cw}" height="170" rx="14" fill="#0b0a12" stroke="{col}" stroke-opacity=".4"/>'
                 + text(x + 18, y0 + 34, n, 18, col, weight=700, ls=2) + text(x + 18, y0 + 56, role, 11, STAR, .55, ls=3)
                 # the lamp: amber STANDBY until polled, then GO
                 + f'<rect x="{x + 18}" y="{y0 + 76}" width="{cw - 36}" height="56" rx="10" fill="#3a2a00">'
                 f'<animate attributeName="fill" values="#3a2a00;#3a2a00;#0f5c2c;#0f5c2c;#3a2a00" keyTimes="0;{a:.3f};{a + .01:.3f};.95;1" dur="{cyc}s" repeatCount="indefinite"/></rect>'
                 + f'<g><animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;{a:.3f};{a + .01:.3f};.95;1" dur="{cyc}s" repeatCount="indefinite"/>{text(x + cw / 2, y0 + 112, "STANDBY", 18, "#ffb020", weight=900, anchor="middle", ls=4)}</g>'
                 + f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a:.3f};{a + .01:.3f};.95;1" dur="{cyc}s" repeatCount="indefinite"/>{text(x + cw / 2, y0 + 116, "GO", 34, GREEN, weight=900, anchor="middle", ls=8, extra="filter=\"url(#glow)\"")}</g>'
                 + f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a - .04:.3f};{a - .035:.3f};{a:.3f};{a + .005:.3f}" dur="{cyc}s" repeatCount="indefinite"/>{text(x + cw / 2, y0 + 156, n + "?", 12, STAR, .8, anchor="middle", ls=2)}</g>')
    fin = (1.2 + 5 * 1.6) / cyc
    body += (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{fin:.3f};{fin + .02:.3f};.95;1" dur="{cyc}s" repeatCount="indefinite"/>'
             + text(W / 2, H - 40, 'ALL STATIONS GO.', 30, GREEN, font=SANS, weight=900, anchor='middle', ls=10, extra='filter="url(#glow)"') + '</g>')
    return svg(W, H, body, 'Go / no-go for launch: Clockford, Ratchet, Crimp, Marklode and M.A.X each report GO; all stations go.')


# ================================================================ the telemetry ticker
def ticker():
    H = 54
    tonight = ''
    p = A / 'tonight.json'
    if p.exists():
        tonight = f'TONIGHT: DEIMOS {json.loads(p.read_text())["angle"] % 360:.0f}° AROUND MARS (JPL HORIZONS)  ✦  '
    items = ('DEIMOS AI LLC · DEIMOSCORE.COM  ✦  MISSION CONTROL FOR THE AGE OF AGENTS  ✦  '
             + (f'CLOCKFORD PRIVATE BETA T–{DAYS}  ✦  ' if DAYS > 0 else 'CLOCKFORD BETA: LIFTOFF  ✦  ')
             + 'PATENTS PENDING: CLOCKFORD · CRIMP  ✦  OPENSSF SILVER: RATCHET · CRIMP  ✦  ' + tonight + 'CREW: 1 WOLF  ✦  ')
    L = len(items) * 9.9
    k = uid('tick')
    body = (f'<rect width="{W}" height="{H}" rx="14" fill="{VOID}"/><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="url(#tk{k})" stroke-width="1.5"/>'
            f'<defs><linearGradient id="tk{k}" x1="0" x2="1"><stop offset="0" stop-color="{PINK}">{acid("stop-color", 0, 6)}</stop><stop offset="1" stop-color="{CYAN}">{acid("stop-color", 3, 6)}</stop></linearGradient>'
            f'<clipPath id="tc{k}"><rect x="10" width="{W - 20}" height="{H}"/></clipPath></defs>'
            f'<g clip-path="url(#tc{k})"><g>{text(20, 34, items * 3, 16, STAR, .9, ls=1.2)}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{-L:.0f} 0" dur="{L / 60:.0f}s" repeatCount="indefinite"/></g></g>')
    return svg(W, H, body, 'Telemetry: Deimos AI, mission control for the age of agents; Clockford beta countdown; patents pending; OpenSSF Silver; tonight\'s Deimos.')


def main():
    A.mkdir(parents=True, exist_ok=True)
    out = {'agency.svg': agency(), 'poll.svg': poll(), 'board.svg': board(), 'rules-dark.svg': rules(False), 'rules-light.svg': rules(True), 'dread.svg': dread(), 'hatch.svg': hatch(),
           'boarding-dark.svg': boarding(False), 'boarding-light.svg': boarding(True), 'log-dark.svg': log(False), 'log-light.svg': log(True)}
    for i, p in enumerate(PATCHES):
        out[f'patch-{p[0].lower().replace(".", "")}.svg'] = patch(i)
    out['ticker.svg'] = ticker()
    for n, s in out.items():
        (A / n).write_text(s, encoding='utf-8'); print(f'{n:20} {len(s) // 1024:4d} KB')


if __name__ == '__main__':
    main()
