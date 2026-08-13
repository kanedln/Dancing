#!/usr/bin/env python3
"""Generate the before/after room artwork used by the Results slider.

Each room is drawn once as shared geometry, then rendered twice — 'before'
(grimy, cluttered) and 'after' (spotless). Because both states come from the
same drawing code, the two frames line up pixel-for-pixel, which is what makes
the comparison wipe read correctly.

Output: assets/img/ba-<room>-before.svg / ba-<room>-after.svg

Run from the repo root:  python3 tools/generate-room-art.py
"""
import pathlib

W, H = 1600, 900
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'img'

# ----------------------------------------------------------------- palette
INK      = '#2A2327'
GRIME    = '#6E5A3A'
PINK     = '#DB044C'
GOLD     = '#C89439'


def defs(extra=''):
    """Gradients and filters shared by every scene."""
    return f'''<defs>
  <linearGradient id="dayLight" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFF8E7" stop-opacity=".85"/>
    <stop offset="1" stop-color="#FFF8E7" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="glassG" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#DFF1FA"/><stop offset="1" stop-color="#B8DCEC"/>
  </linearGradient>
  <radialGradient id="vign" cx="50%" cy="45%" r="75%">
    <stop offset="55%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity=".20"/>
  </radialGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="10"/></filter>
  <filter id="soft3"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  {extra}
</defs>'''


def grime_layer(seed_spots, opacity=.5):
    """Yellow-brown splotches — the visual shorthand for 'not cleaned in a while'."""
    parts = [f'<g opacity="{opacity}">']
    for (cx, cy, rx, ry, o) in seed_spots:
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
                     f'fill="{GRIME}" opacity="{o}" filter="url(#soft)"/>')
    parts.append('</g>')
    return ''.join(parts)


def sparkles(points):
    """Four-point stars — the 'it gleams' cue on the after frames."""
    out = []
    for (x, y, s, o) in points:
        out.append(
            f'<path d="M{x} {y-s} Q{x+s*.18} {y-s*.18} {x+s} {y} '
            f'Q{x+s*.18} {y+s*.18} {x} {y+s} Q{x-s*.18} {y+s*.18} {x-s} {y} '
            f'Q{x-s*.18} {y-s*.18} {x} {y-s} Z" fill="#FFFFFF" opacity="{o}"/>')
    return ''.join(out)


def wrap(body, state):
    """Shared colour grade: before is dim and yellowed, after is bright and clean."""
    # Keep the grade light — the before/after difference should come from the
    # scene content (clutter, grime, shine), not from washing the whole frame out.
    if state == 'before':
        grade = ('<rect width="1600" height="900" fill="#4A3510" opacity=".11"/>'
                 '<rect width="1600" height="900" fill="#120C04" opacity=".07"/>'
                 '<rect width="1600" height="900" filter="url(#grain)" opacity=".09"/>')
    else:
        grade = ('<rect width="1600" height="900" fill="url(#dayLight)" opacity=".20"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">{defs()}{body}{grade}'
            f'<rect width="1600" height="900" fill="url(#vign)"/></svg>')


# ================================================================= KITCHEN
def kitchen(state):
    before = state == 'before'
    cab_face   = '#B5A88C' if before else '#F4F1EA'
    cab_edge   = '#8B7D5F' if before else '#CFC7B6'
    counter    = '#5D5449' if before else '#8E877A'
    wall       = '#C0B49C' if before else '#EFEADE'
    splash     = '#A9B6AF' if before else '#DDEDE6'
    floor_a    = '#8A7A61' if before else '#C4B49A'
    floor_b    = '#79694F' if before else '#B2A085'

    s = [f'<rect width="1600" height="900" fill="{wall}"/>']

    # ---- floor (simple two-tone tiling, foreground) ----
    s.append(f'<rect y="680" width="1600" height="220" fill="{floor_a}"/>')
    for i in range(-1, 12):
        x = i * 150 - 60
        s.append(f'<path d="M{x} 900 L{x+95} 680 L{x+170} 680 L{x+75} 900 Z" fill="{floor_b}" opacity=".55"/>')
    s.append('<rect y="672" width="1600" height="12" fill="#000" opacity=".18"/>')

    # ---- window, left ----
    s.append(f'<rect x="70" y="140" width="300" height="290" rx="6" fill="#FFFFFF" opacity=".9"/>')
    s.append(f'<rect x="84" y="154" width="272" height="262" fill="url(#glassG)"/>')
    if before:
        s.append('<rect x="84" y="154" width="272" height="262" fill="#7A6A45" opacity=".34"/>')
        s.append('<path d="M84 300 q60 40 130 8 t142 20 L356 416 L84 416 Z" fill="#6E5A3A" opacity=".2"/>')
    s.append('<rect x="214" y="154" width="12" height="262" fill="#FFFFFF" opacity=".9"/>')
    s.append('<rect x="84" y="278" width="272" height="12" fill="#FFFFFF" opacity=".9"/>')
    s.append(f'<rect x="70" y="140" width="300" height="290" rx="6" fill="none" stroke="{cab_edge}" stroke-width="10"/>')

    # ---- upper cabinets ----
    for x in (470, 700):
        s.append(f'<rect x="{x}" y="140" width="215" height="215" rx="5" fill="{cab_face}" stroke="{cab_edge}" stroke-width="6"/>')
        s.append(f'<rect x="{x+22}" y="162" width="171" height="171" rx="3" fill="none" stroke="{cab_edge}" stroke-width="5" opacity=".8"/>')
        s.append(f'<rect x="{x+96}" y="330" width="24" height="9" rx="4" fill="#8C8578"/>')
    s.append(f'<rect x="1160" y="140" width="270" height="215" rx="5" fill="{cab_face}" stroke="{cab_edge}" stroke-width="6"/>')
    s.append(f'<rect x="1182" y="162" width="226" height="171" rx="3" fill="none" stroke="{cab_edge}" stroke-width="5" opacity=".8"/>')

    # ---- backsplash + counter ----
    s.append(f'<rect x="430" y="400" width="1000" height="140" fill="{splash}"/>')
    for gx in range(430, 1430, 50):
        s.append(f'<line x1="{gx}" y1="400" x2="{gx}" y2="540" stroke="#FFF" stroke-opacity=".35" stroke-width="3"/>')
    for gy in (445, 490):
        s.append(f'<line x1="430" y1="{gy}" x2="1430" y2="{gy}" stroke="#FFF" stroke-opacity=".35" stroke-width="3"/>')
    s.append(f'<rect x="60" y="540" width="1380" height="34" rx="4" fill="{counter}"/>')
    s.append(f'<rect x="60" y="540" width="1380" height="9" rx="4" fill="#FFF" opacity="{".10" if before else ".38"}"/>')

    # ---- base cabinets ----
    s.append(f'<rect x="60" y="574" width="1380" height="112" fill="{cab_face}"/>')
    for x in range(60, 1440, 172):
        s.append(f'<rect x="{x+6}" y="580" width="160" height="100" rx="4" fill="none" stroke="{cab_edge}" stroke-width="5"/>')
        s.append(f'<rect x="{x+66}" y="596" width="42" height="8" rx="4" fill="#8C8578"/>')

    # ---- sink under the window ----
    s.append(f'<rect x="130" y="548" width="210" height="20" rx="6" fill="#9AA0A2"/>')
    s.append(f'<rect x="142" y="556" width="186" height="14" rx="5" fill="{"#6E6A5A" if before else "#C3CACD"}"/>')
    s.append('<path d="M228 470 q0 -46 34 -46 q34 0 34 40 v42" fill="none" stroke="#AEB4B6" stroke-width="13" stroke-linecap="round"/>')

    # ---- stovetop ----
    s.append(f'<rect x="640" y="542" width="240" height="30" rx="5" fill="{"#3B3730" if before else "#4A4640"}"/>')
    for cx in (700, 820):
        s.append(f'<ellipse cx="{cx}" cy="557" rx="38" ry="11" fill="none" stroke="{"#6B5A33" if before else "#8E8A82"}" stroke-width="5"/>')

    # ---- fridge, right ----
    s.append(f'<rect x="1396" y="200" width="180" height="486" rx="10" fill="{"#B9B3A8" if before else "#DCD8D2"}" stroke="{cab_edge}" stroke-width="6"/>')
    s.append(f'<line x1="1396" y1="360" x2="1576" y2="360" stroke="{cab_edge}" stroke-width="6"/>')
    s.append(f'<rect x="1416" y="300" width="12" height="46" rx="6" fill="#8C8578"/>')
    s.append(f'<rect x="1416" y="382" width="12" height="46" rx="6" fill="#8C8578"/>')

    # ------------------------------------------------------- state details
    if before:
        # dishes heaped in the sink
        s.append('<g>')
        s.append('<ellipse cx="196" cy="548" rx="62" ry="15" fill="#8E8574"/>')
        s.append('<ellipse cx="220" cy="530" rx="68" ry="16" fill="#A9A08C"/>')
        s.append('<ellipse cx="184" cy="512" rx="54" ry="14" fill="#7E7565"/>')
        s.append('<ellipse cx="228" cy="496" rx="44" ry="12" fill="#9A9180"/>')
        s.append('<rect x="256" y="480" width="42" height="52" rx="6" fill="#6E6656"/>')
        s.append('<rect x="300" y="492" width="32" height="40" rx="5" fill="#877E6C"/>')
        s.append('<path d="M138 512 l20 -46 l14 6 l-18 46 Z" fill="#5E5646"/>')
        s.append('<path d="M310 468 l30 -18 l8 12 l-30 18 Z" fill="#6E6656"/>')
        s.append('</g>')
        # counter clutter
        s.append('<rect x="900" y="488" width="50" height="54" rx="4" fill="#6B4A2E"/>')
        s.append('<rect x="958" y="472" width="34" height="70" rx="4" fill="#47552F"/>')
        s.append('<rect x="1000" y="500" width="66" height="42" rx="4" fill="#7A6A44"/>')
        s.append('<circle cx="1100" cy="520" r="24" fill="#54452A"/>')
        s.append('<rect x="1140" y="486" width="38" height="56" rx="3" fill="#63563A"/>')
        s.append('<path d="M1060 496 l44 -22 l6 12 l-44 22 Z" fill="#4E4230"/>')
        # drips running down the backsplash
        s.append('<g opacity=".5" fill="#4A3A1E">'
                 '<path d="M690 400 q8 60 -2 96 q-6 24 6 44 h14 q-10 -70 0 -140 Z"/>'
                 '<path d="M820 400 q10 44 0 74 q-6 20 4 66 h12 q-12 -78 -2 -140 Z"/>'
                 '<path d="M1240 400 q6 50 -4 84 q-4 22 4 56 h12 q-8 -74 2 -140 Z"/></g>')
        # crumbs
        for (cx, cy) in ((470, 536), (492, 531), (520, 537), (560, 533), (600, 536),
                         (1200, 535), (1240, 531), (1280, 536), (1320, 532)):
            s.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#6B5836" opacity=".8"/>')
        # overflowing bin on the floor
        s.append('<path d="M1180 700 l16 168 h128 l16 -168 Z" fill="#5E5A52"/>')
        s.append('<path d="M1186 700 h164 v-14 h-164 Z" fill="#6E6A62"/>')
        s.append('<ellipse cx="1268" cy="694" rx="58" ry="18" fill="#8A8478"/>')
        s.append('<path d="M1220 690 q22 -34 54 -12 q30 -26 44 6 q-52 20 -98 6 Z" fill="#9B9488"/>')
        s.append('<rect x="1330" y="806" width="70" height="46" rx="6" fill="#7A7468" opacity=".9"/>')
        # grease + floor stains
        s.append(grime_layer([
            (760, 470, 120, 60, .5), (700, 556, 90, 26, .55), (250, 560, 110, 30, .45),
            (1000, 520, 130, 40, .35), (520, 250, 90, 70, .3), (1300, 250, 110, 70, .28),
            (420, 800, 150, 46, .5), (900, 840, 190, 54, .45), (1480, 790, 120, 40, .4),
        ], .55))
        # cobweb, top-left corner
        s.append('<path d="M0 0 L150 0 M0 0 L0 150 M0 0 L110 110 M28 0 q40 40 0 84 M62 0 q60 58 0 122" '
                 'fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".22"/>')
        # smudges on the cabinet faces
        s.append('<g opacity=".3">'
                 '<path d="M520 610 q30 -18 56 4" stroke="#5A4A2A" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 '<path d="M880 618 q34 -16 62 2" stroke="#5A4A2A" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 '</g>')
    else:
        # clean sink, empty and bright
        s.append('<ellipse cx="235" cy="560" rx="70" ry="9" fill="#FFFFFF" opacity=".45"/>')
        # tidy, deliberate styling: fruit bowl, plant, branded spray bottle
        s.append('<ellipse cx="930" cy="528" rx="52" ry="16" fill="#DDD6C6"/>')
        s.append('<circle cx="912" cy="516" r="15" fill="#C5473F"/>')
        s.append('<circle cx="940" cy="513" r="14" fill="#D98A2B"/>')
        s.append('<circle cx="926" cy="502" r="13" fill="#7FA23C"/>')
        s.append('<rect x="1050" y="486" width="46" height="56" rx="6" fill="#5E7A4A"/>')
        s.append('<path d="M1073 486 q-34 -44 -6 -66 q30 20 6 66 Z" fill="#6F9455"/>')
        s.append('<path d="M1073 486 q36 -38 8 -62 q-30 22 -8 62 Z" fill="#83A968"/>')
        s.append(f'<rect x="1160" y="490" width="36" height="52" rx="6" fill="{PINK}"/>')
        s.append(f'<rect x="1170" y="474" width="16" height="18" fill="{PINK}"/>')
        s.append('<path d="M1186 478 l26 -12 v10 l-26 8 Z" fill="#FFFFFF" opacity=".85"/>')
        # neatly folded towel on the counter
        s.append(f'<rect x="470" y="512" width="86" height="30" rx="6" fill="{PINK}" opacity=".85"/>')
        s.append('<rect x="470" y="522" width="86" height="4" fill="#FFFFFF" opacity=".5"/>')
        # shine
        s.append(sparkles([(250, 520, 26, .95), (720, 452, 20, .8), (1268, 470, 22, .85),
                           (980, 596, 16, .7), (1470, 300, 18, .75), (560, 604, 14, .6)]))
        s.append('<path d="M60 549 h1380" stroke="#FFFFFF" stroke-width="4" opacity=".55"/>')
        s.append('<ellipse cx="800" cy="800" rx="420" ry="70" fill="#FFFFFF" opacity=".10"/>')

    return wrap(''.join(s), state)


# ============================================================ LIVING ROOM
def living(state):
    before = state == 'before'
    wall    = '#B9AC98' if before else '#ECE4D6'
    sofa_a  = '#6E7883' if before else '#93A3B5'
    sofa_b  = '#5A636D' if before else '#7C8CA0'
    rug     = '#93805F' if before else '#DCCDB4'
    wood    = '#6B5336' if before else '#9C7B52'
    floor   = '#7E6A4E' if before else '#B4926C'

    s = [f'<rect width="1600" height="900" fill="{wall}"/>']
    s.append(f'<rect y="600" width="1600" height="300" fill="{floor}"/>')
    for i in range(0, 14):
        s.append(f'<rect x="{i*120}" y="600" width="4" height="300" fill="#000" opacity=".07"/>')
    s.append('<rect y="594" width="1600" height="10" fill="#000" opacity=".15"/>')

    # ---- window, right, with blinds ----
    s.append('<rect x="1120" y="120" width="380" height="330" rx="5" fill="#FFFFFF" opacity=".92"/>')
    s.append('<rect x="1136" y="136" width="348" height="298" fill="url(#glassG)"/>')
    if before:
        s.append('<rect x="1136" y="136" width="348" height="298" fill="#7A6A45" opacity=".3"/>')
    for by in range(150, 300, 26):
        s.append(f'<rect x="1136" y="{by}" width="348" height="12" rx="3" fill="#FFFFFF" opacity=".72"/>')
    s.append('<rect x="1120" y="120" width="380" height="330" rx="5" fill="none" stroke="#D8D2C6" stroke-width="12"/>')

    # ---- shelf, left ----
    s.append(f'<rect x="90" y="250" width="300" height="16" rx="4" fill="{wood}"/>')
    s.append(f'<rect x="90" y="400" width="300" height="16" rx="4" fill="{wood}"/>')
    for bx, bw, bc in ((110, 22, '#8A5A4A'), (138, 18, '#5A6E7A'), (162, 24, '#7A6A4A'),
                       (192, 16, '#6A7A5A'), (214, 20, '#8A7A5A')):
        s.append(f'<rect x="{bx}" y="{250-58}" width="{bw}" height="58" rx="2" fill="{bc}"/>')

    # ---- framed pictures ----
    tilt = 'rotate(-6 700 210)' if before else ''
    s.append(f'<g transform="{tilt}"><rect x="640" y="150" width="130" height="120" rx="4" '
             f'fill="#DCD4C4" stroke="{wood}" stroke-width="9"/>'
             f'<path d="M652 258 l38 -52 l30 32 l26 -32 l32 52 Z" fill="#8FA57E"/></g>')
    s.append(f'<rect x="800" y="176" width="104" height="94" rx="4" fill="#DCD4C4" stroke="{wood}" stroke-width="9"/>')
    s.append('<circle cx="852" cy="216" r="22" fill="#C7A05A"/>')

    # ---- rug ----
    s.append(f'<ellipse cx="720" cy="778" rx="470" ry="104" fill="{rug}"/>')
    s.append(f'<ellipse cx="720" cy="778" rx="400" ry="82" fill="none" stroke="#FFF" stroke-opacity=".28" stroke-width="7"/>')

    # ---- sofa ----
    s.append(f'<rect x="330" y="420" width="600" height="140" rx="26" fill="{sofa_b}"/>')
    s.append(f'<rect x="352" y="536" width="556" height="104" rx="20" fill="{sofa_a}"/>')
    s.append(f'<rect x="306" y="470" width="66" height="176" rx="24" fill="{sofa_b}"/>')
    s.append(f'<rect x="888" y="470" width="66" height="176" rx="24" fill="{sofa_b}"/>')
    for cx in (470, 630, 790):
        rot = f' transform="rotate({-7 if before else 0} {cx} 500)"' if before else ''
        s.append(f'<rect x="{cx-72}" y="446" width="144" height="104" rx="16" fill="{sofa_a}"{rot}/>')
    s.append(f'<rect x="366" y="640" width="30" height="30" rx="6" fill="{wood}"/>')
    s.append(f'<rect x="864" y="640" width="30" height="30" rx="6" fill="{wood}"/>')

    # ---- coffee table ----
    s.append(f'<rect x="540" y="700" width="380" height="22" rx="8" fill="{wood}"/>')
    s.append(f'<rect x="566" y="722" width="20" height="70" rx="6" fill="{wood}"/>')
    s.append(f'<rect x="874" y="722" width="20" height="70" rx="6" fill="{wood}"/>')

    # ---- floor lamp, right ----
    s.append(f'<rect x="1040" y="470" width="12" height="190" fill="{wood}"/>')
    s.append(f'<path d="M996 470 l16 -84 h72 l16 84 Z" fill="{"#B6A886" if before else "#EFE4C8"}"/>')
    s.append(f'<ellipse cx="1046" cy="662" rx="46" ry="12" fill="{wood}"/>')

    # ------------------------------------------------------- state details
    if before:
        # clothes and a blanket slung over the sofa
        s.append('<path d="M360 448 q80 -40 150 12 q60 44 -20 66 q-90 22 -130 -20 Z" fill="#7A3F43"/>')
        s.append('<path d="M700 460 q90 -34 150 20 q40 42 -40 56 q-96 12 -110 -76 Z" fill="#3E4E6C"/>')
        s.append('<path d="M566 556 q120 -26 210 22 q-100 40 -210 -22 Z" fill="#5C4A70" opacity=".95"/>')
        # table clutter
        s.append('<rect x="588" y="656" width="94" height="46" rx="4" fill="#C2A06A"/>')
        s.append('<path d="M588 656 h94 v-10 h-94 Z" fill="#D8BA86"/>')
        s.append('<rect x="700" y="668" width="34" height="34" rx="4" fill="#DCD4C4"/>')
        s.append('<rect x="746" y="662" width="28" height="40" rx="4" fill="#B6AEA0"/>')
        s.append('<ellipse cx="830" cy="694" rx="30" ry="9" fill="#9A9286"/>')
        s.append('<rect x="806" y="674" width="48" height="22" rx="3" fill="#AEA69A"/>')
        # scattered on the floor
        s.append('<path d="M420 828 l70 -16 l10 26 l-70 16 Z" fill="#C9C1B1"/>')
        s.append('<path d="M448 856 l66 -12 l8 24 l-66 12 Z" fill="#D3CBBB"/>')
        s.append('<path d="M980 812 q40 -22 78 2 q-30 30 -78 -2 Z" fill="#6E5F4A"/>')
        s.append('<path d="M1024 846 q42 -20 76 6 q-34 26 -76 -6 Z" fill="#7C6C54"/>')
        s.append('<circle cx="330" cy="852" r="20" fill="#8A6A4A"/>')
        # stains and dust
        s.append(grime_layer([
            (700, 790, 150, 40, .5), (520, 812, 110, 32, .45), (900, 806, 130, 36, .4),
            (240, 330, 120, 80, .3), (1300, 560, 140, 50, .3), (760, 210, 130, 70, .25),
        ], .55))
        s.append('<path d="M1600 0 L1450 0 M1600 0 L1600 150 M1600 0 L1494 106 M1572 0 q-42 42 0 86" '
                 'fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".2"/>')
    else:
        # styled: books, vase, tray
        s.append('<rect x="606" y="672" width="92" height="14" rx="3" fill="#8A5F62"/>')
        s.append('<rect x="614" y="660" width="76" height="12" rx="3" fill="#5F6E8A"/>')
        s.append(f'<rect x="770" y="654" width="40" height="46" rx="8" fill="{PINK}" opacity=".85"/>')
        s.append('<path d="M790 654 q-26 -40 -4 -60 q24 18 4 60 Z" fill="#6F9455"/>')
        s.append('<path d="M790 654 q28 -34 6 -56 q-26 20 -6 56 Z" fill="#83A968"/>')
        # plumped, aligned cushions get a highlight
        s.append('<g opacity=".5">'
                 '<path d="M410 466 q60 -14 120 0" stroke="#FFF" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 '<path d="M570 466 q60 -14 120 0" stroke="#FFF" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 '<path d="M730 466 q60 -14 120 0" stroke="#FFF" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 '</g>')
        # vacuum tracks in the rug
        s.append('<g opacity=".35" stroke="#FFFFFF" stroke-width="6" fill="none">'
                 '<path d="M370 800 q350 -46 700 0"/><path d="M380 828 q340 -44 680 0"/>'
                 '<path d="M400 852 q320 -40 640 0"/></g>')
        s.append(sparkles([(1180, 300, 24, .9), (500, 430, 20, .8), (880, 664, 18, .8),
                           (300, 258, 18, .7), (1046, 396, 20, .75), (700, 742, 15, .65)]))
        s.append('<ellipse cx="760" cy="820" rx="440" ry="72" fill="#FFFFFF" opacity=".10"/>')

    return wrap(''.join(s), state)


# =============================================================== BATHROOM
def bathroom(state):
    before = state == 'before'
    tile    = '#A6B0A8' if before else '#E9F1ED'
    grout   = '#6B6748' if before else '#C6D2CB'
    vanity  = '#A0967C' if before else '#F1ECE1'
    porcelain = '#C2BBA6' if before else '#FFFFFF'
    floor   = '#8D8B79' if before else '#D8DED8'

    s = [f'<rect width="1600" height="900" fill="{tile}"/>']
    # wall tiles
    for gy in range(0, 700, 78):
        s.append(f'<line x1="0" y1="{gy}" x2="1600" y2="{gy}" stroke="{grout}" stroke-width="6"/>')
    for gx in range(0, 1660, 78):
        s.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="700" stroke="{grout}" stroke-width="6"/>')
    s.append(f'<rect y="700" width="1600" height="200" fill="{floor}"/>')
    for gx in range(-40, 1700, 96):
        s.append(f'<path d="M{gx} 900 L{gx+60} 700 L{gx+70} 700 L{gx+10} 900 Z" fill="{grout}" opacity=".5"/>')
    s.append('<rect y="694" width="1600" height="10" fill="#000" opacity=".16"/>')

    # ---- vanity + mirror, left ----
    s.append(f'<rect x="120" y="520" width="460" height="180" rx="8" fill="{vanity}"/>')
    s.append(f'<rect x="110" y="498" width="480" height="30" rx="8" fill="{"#8E8676" if before else "#D9D3C7"}"/>')
    s.append(f'<rect x="150" y="548" width="180" height="130" rx="6" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="5"/>')
    s.append(f'<rect x="370" y="548" width="180" height="130" rx="6" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="5"/>')
    s.append(f'<ellipse cx="350" cy="508" rx="96" ry="26" fill="{porcelain}"/>')
    s.append('<path d="M330 442 q0 -44 30 -44 q30 0 30 40 v26" fill="none" stroke="#AEB4B6" stroke-width="12" stroke-linecap="round"/>')
    # mirror
    s.append(f'<rect x="170" y="150" width="360" height="270" rx="8" fill="{"#9FAAA8" if before else "#CFE6EE"}" stroke="{vanity}" stroke-width="14"/>')
    s.append('<path d="M186 400 L340 166 L420 166 L206 416 Z" fill="#FFFFFF" opacity=".22"/>')

    # ---- shower with glass, right ----
    s.append(f'<rect x="900" y="120" width="600" height="580" rx="6" fill="{"#A9B2AC" if before else "#DCE9E4"}" opacity=".5"/>')
    s.append(f'<rect x="900" y="120" width="600" height="580" rx="6" fill="none" stroke="{"#8E9A94" if before else "#BFD2CB"}" stroke-width="14"/>')
    s.append(f'<line x1="1200" y1="120" x2="1200" y2="700" stroke="{"#8E9A94" if before else "#BFD2CB"}" stroke-width="12"/>')
    s.append('<path d="M1246 160 q0 -34 40 -34 h60" fill="none" stroke="#AEB4B6" stroke-width="12" stroke-linecap="round"/>')
    s.append('<ellipse cx="1246" cy="176" rx="30" ry="12" fill="#B8BEC0"/>')

    # ---- toilet, centre ----
    s.append(f'<rect x="654" y="470" width="120" height="150" rx="10" fill="{porcelain}"/>')
    s.append(f'<ellipse cx="714" cy="640" rx="76" ry="34" fill="{porcelain}"/>')
    s.append(f'<ellipse cx="714" cy="636" rx="52" ry="20" fill="{"#9E9884" if before else "#E9EEF0"}"/>')
    s.append(f'<rect x="686" y="620" width="56" height="70" rx="8" fill="{porcelain}"/>')

    # ------------------------------------------------------- state details
    if before:
        # soap scum / limescale streaks on the glass
        s.append('<g opacity=".55">')
        for gx in range(930, 1490, 46):
            s.append(f'<path d="M{gx} 150 q14 140 -6 300 q-10 90 4 220" stroke="#D8CFA8" '
                     f'stroke-width="{10 if gx % 92 else 16}" fill="none" opacity=".55"/>')
        s.append('</g>')
        s.append('<ellipse cx="1180" cy="470" rx="200" ry="170" fill="#A8996A" opacity=".45" filter="url(#soft)"/>')
        # cluttered vanity
        s.append('<rect x="150" y="446" width="34" height="56" rx="5" fill="#6E7A55"/>')
        s.append('<rect x="192" y="458" width="26" height="44" rx="5" fill="#8A5F62"/>')
        s.append('<rect x="226" y="440" width="22" height="62" rx="4" fill="#5F6E8A"/>')
        s.append('<rect x="452" y="452" width="40" height="50" rx="6" fill="#9A8E6E"/>')
        s.append('<rect x="500" y="466" width="24" height="36" rx="4" fill="#7E8A6A"/>')
        s.append('<path d="M410 500 q30 -16 58 -2 l-4 6 q-26 -12 -54 2 Z" fill="#B0A896"/>')
        # towels dumped on the floor
        s.append('<path d="M330 806 q70 -56 168 -20 q70 26 6 60 q-100 32 -174 -40 Z" fill="#5E6672"/>')
        s.append('<path d="M600 850 q56 -40 130 -14 q52 20 2 44 q-78 24 -132 -30 Z" fill="#767E8C"/>')
        # water spots on the mirror
        s.append('<g opacity=".5" fill="#CFC6A2">'
                 '<circle cx="250" cy="220" r="9"/><circle cx="300" cy="266" r="6"/>'
                 '<circle cx="356" cy="212" r="8"/><circle cx="420" cy="288" r="7"/>'
                 '<circle cx="286" cy="340" r="10"/><circle cx="452" cy="196" r="6"/></g>')
        # grime in the grout + around the toilet base
        s.append(grime_layer([
            (714, 682, 130, 34, .6), (350, 700, 180, 40, .45), (1200, 690, 220, 40, .5),
            (1000, 400, 150, 130, .3), (120, 120, 130, 100, .3), (860, 820, 200, 50, .4),
        ], .6))
        s.append('<g opacity=".35" stroke="#6E5A3A" stroke-width="7" fill="none">'
                 '<path d="M0 234 h1600"/><path d="M0 546 h900"/><path d="M546 0 v700"/></g>')
    else:
        # clear glass, with a clean highlight sweep
        s.append('<path d="M950 160 L1130 160 L960 690 L900 690 Z" fill="#FFFFFF" opacity=".28"/>')
        s.append('<path d="M1240 160 L1330 160 L1180 690 L1110 690 Z" fill="#FFFFFF" opacity=".18"/>')
        # tidy vanity: folded towels, soap, branded bottle
        s.append(f'<rect x="160" y="454" width="96" height="20" rx="5" fill="{PINK}" opacity=".85"/>')
        s.append(f'<rect x="166" y="436" width="84" height="18" rx="5" fill="#FFFFFF" opacity=".9"/>')
        s.append(f'<rect x="470" y="452" width="34" height="50" rx="6" fill="{PINK}"/>')
        s.append(f'<rect x="479" y="438" width="16" height="16" fill="{PINK}"/>')
        s.append('<path d="M495 442 l24 -10 v9 l-24 7 Z" fill="#FFFFFF" opacity=".85"/>')
        s.append('<rect x="516" y="474" width="44" height="28" rx="8" fill="#FFFFFF" opacity=".95"/>')
        # rolled towels on a rail
        s.append(f'<rect x="640" y="360" width="180" height="10" rx="5" fill="#B8BEC0"/>')
        s.append(f'<rect x="656" y="370" width="70" height="86" rx="10" fill="#FFFFFF" opacity=".92"/>')
        s.append(f'<rect x="736" y="370" width="70" height="86" rx="10" fill="{PINK}" opacity=".55"/>')
        # bath mat, squared up
        s.append(f'<rect x="360" y="782" width="260" height="70" rx="12" fill="{PINK}" opacity=".35"/>')
        s.append(sparkles([(1160, 260, 28, .95), (1330, 500, 22, .85), (300, 226, 24, .9),
                           (714, 606, 18, .8), (500, 494, 16, .7), (980, 640, 18, .7)]))
        s.append('<ellipse cx="800" cy="820" rx="500" ry="70" fill="#FFFFFF" opacity=".12"/>')

    return wrap(''.join(s), state)


# ==================================================================== main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rooms = {'kitchen': kitchen, 'living': living, 'bath': bathroom}
    for name, fn in rooms.items():
        for state in ('before', 'after'):
            path = OUT / f'ba-{name}-{state}.svg'
            path.write_text(fn(state))
            print(f'{path.relative_to(OUT.parent.parent)}  {path.stat().st_size/1024:.1f} KB')


if __name__ == '__main__':
    main()
