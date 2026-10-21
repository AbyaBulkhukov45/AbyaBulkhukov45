from pathlib import Path
import math, random

ROOT = Path(__file__).resolve().parents[1]
TAU = math.tau
random.seed(45)

def curve(v, phase=0):
    points = []
    for i in range(145):
        u = i / 144 * TAU
        # Twisted toroidal surface, orthographically projected.
        w = v + .85 * math.sin(u * 3 + phase)
        radius = 192 + 68 * math.cos(w)
        x = radius * math.cos(u)
        y = radius * math.sin(u)
        z = 83 * math.sin(w) + 20 * math.sin(u * 2 + phase)
        yy = y * .62 - z * .785
        zz = y * .785 + z * .62
        xx = x * .94 + zz * .342
        # Slight diagonal tilt.
        points.append((600 + 1.4 * (xx * .97 - yy * .243), 370 + 1.4 * (xx * .243 + yy * .97)))
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x,y in points) + 'Z'

parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="t d">
<title id="t">Field 00</title><desc id="d">A slowly evolving iridescent mathematical surface suspended in a dark field.</desc>
<defs>
 <radialGradient id="back"><stop stop-color="#121221"/><stop offset=".62" stop-color="#0b0c13"/><stop offset="1" stop-color="#07080c"/></radialGradient>
 <linearGradient id="spectrum" x1=".1" y1="0" x2=".9" y2="1"><stop stop-color="#78e7ef"/><stop offset=".35" stop-color="#bbbcff"/><stop offset=".65" stop-color="#a18aff"/><stop offset="1" stop-color="#e8bbef"/></linearGradient>
 <radialGradient id="haze"><stop stop-color="#8977fa" stop-opacity=".19"/><stop offset="1" stop-color="#8977fa" stop-opacity="0"/></radialGradient>
 <filter id="blur" x="-.3" y="-.3" width="1.6" height="1.6"><feGaussianBlur stdDeviation="5"/></filter>
 <pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="#9196c0" opacity=".15"/></pattern>
 <style>
 .breathe{animation:breathe 9s ease-in-out infinite}
 .dash{animation:flow 30s linear infinite}
 .pulse{animation:pulse 6s ease-in-out infinite}
 @keyframes breathe{0%,100%{opacity:.6}50%{opacity:1}}
 @keyframes flow{to{stroke-dashoffset:-400}}
 @keyframes pulse{0%,100%{opacity:.22}50%{opacity:.7}}
 @media(prefers-reduced-motion:reduce){*{animation:none!important} .surface{display:none}.still{display:inline!important}}
 </style>
</defs>
<rect width="1200" height="760" rx="12" fill="url(#back)"/>
<rect x="1" y="1" width="1198" height="758" rx="11" fill="none" stroke="#252735"/>
<rect x="28" y="28" width="1144" height="704" fill="url(#dots)"/>
<ellipse class="breathe" cx="600" cy="370" rx="430" ry="330" fill="url(#haze)"/>
<g stroke="#53546d" fill="none" opacity=".55" stroke-width="1">
 <path d="M50 85V50H85M1115 50h35v35M1150 675v35h-35M85 710H50v-35"/>
 <path d="M590 50h20M600 40v20M590 710h20M600 700v20M40 370h20M50 360v20M1140 370h20M1150 360v20"/>
</g>
<g fill="none" stroke="#5c6580" stroke-width=".65" opacity=".26">
 <ellipse cx="600" cy="370" rx="459" ry="268" transform="rotate(-18 600 370)"/>
 <ellipse cx="600" cy="370" rx="468" ry="277" transform="rotate(-18 600 370)" stroke-dasharray="1 13"/>
 <circle cx="600" cy="370" r="302" stroke-dasharray="2 14"/>
</g>
<g stroke="#8197bb" opacity=".2" stroke-width=".7"><path d="M95 370h120M985 370h120M600 90v50M600 600v50"/></g>
''']

# Sparse, deterministic points. Decoration has no relationship to user data.
for i in range(58):
    x,y = random.uniform(90,1110),random.uniform(95,650)
    if ((x-600)/430)**2 + ((y-370)/245)**2 < 1: continue
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(.5,1.3):.1f}" fill="#a1aecf" opacity="{random.uniform(.18,.6):.2f}"/>')

# Low-cost glow uses only six paths; detail remains crisp and lightweight.
parts.append('<g fill="none" stroke="url(#spectrum)" stroke-width="3" opacity=".2" filter="url(#blur)">')
for n in range(6): parts.append(f'<path d="{curve(n/6*TAU)}"/>')
parts.append('</g>')

for n in range(52):
    v = n / 52 * TAU
    start = curve(v)
    frames = ';'.join(curve(v,p) for p in [0,TAU/4,TAU/2,TAU*3/4,TAU])
    opacity = .26 + .46 * (.5+.5*math.sin(v))
    parts.append(f'<path class="surface" d="{start}" fill="none" stroke="url(#spectrum)" stroke-width=".95" opacity="{opacity:.2f}"><animate attributeName="d" values="{frames}" dur="24s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/></path>')
    parts.append(f'<path class="still" style="display:none" d="{start}" fill="none" stroke="url(#spectrum)" stroke-width=".95" opacity="{opacity:.2f}"/>')

# Traveling highlights add a separate slow motion layer.
for v in [0.3,2.7,4.5]:
    parts.append(f'<path class="dash" d="{curve(v)}" fill="none" stroke="#deebff" stroke-width="1.2" stroke-dasharray="1 199" opacity=".55"/>')
parts.append('''
<g fill="#858aab" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="3">
 <text x="95" y="74">F / 00</text><text x="1105" y="74" text-anchor="end">∞</text>
 <text x="95" y="698">∅</text><text x="1105" y="698" text-anchor="end">0 1 0</text>
</g>
<path d="M460 687h280" stroke="#282a3c"/><path class="pulse" d="M550 687h100" stroke="url(#spectrum)"/>
</svg>''')

(ROOT/'assets'/'field.svg').write_text('\n'.join(parts), encoding='utf-8')
(ROOT/'README.md').write_text('''<p align="center">
  <a href="https://raw.githubusercontent.com/AbyaBulkhukov45/AbyaBulkhukov45/main/assets/field.svg">
    <img src="./assets/field.svg" width="100%" alt="Animated generative geometry" />
  </a>
</p>
''', encoding='utf-8')
print(f'Created field.svg: {(ROOT/"assets"/"field.svg").stat().st_size:,} bytes')
