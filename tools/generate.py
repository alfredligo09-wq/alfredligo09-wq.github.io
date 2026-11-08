import math, random, pathlib

ROOT = pathlib.Path('.')
random.seed(7)

# ---------- contour (topographic) lines ----------
def loop(cx, cy, r, wob, seed, n=90):
    rnd = random.Random(seed)
    k = [(rnd.uniform(0, 6.28), rnd.uniform(.4, 1)) for _ in range(4)]
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        d = r * (1 + wob * sum(m * math.sin((j + 2) * a + p) for j, (p, m) in enumerate(k)) / 3)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a) * .72))
    s = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        s += f' Q{p1[0]:.1f},{p1[1]:.1f} {(p1[0]+p2[0])/2:.1f},{(p1[1]+p2[1])/2:.1f}'
    return s + 'Z'

paths = []
for (cx, cy, seed, rings) in [(380, 330, 1, 13), (1180, 640, 2, 16), (1500, 120, 3, 9)]:
    for i in range(1, rings + 1):
        paths.append(loop(cx, cy, 34 * i, .18 + i * .006, seed))
topo = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">'
        '<g fill="none" stroke="#f6f8f5" stroke-opacity=".28" stroke-width="1.2">'
        + ''.join(f'<path d="{p}"/>' for p in paths) + '</g></svg>')
(ROOT / 'assets/topo.svg').write_text(topo)

# ---------- hero mountain ridges ----------
def ridge(base, amp, peaks, seed, w=1600, h=1000):
    rnd = random.Random(seed)
    xs = list(range(0, w + 1, 20))
    ph = [(rnd.uniform(0, 6.28), rnd.uniform(.5, 1), f) for f in (1, 2.3, 5.1, 11)]
    pts = []
    for x in xs:
        t = x / w
        y = base - amp * sum(m / (i + 1) ** .9 * (0.5 + 0.5 * math.sin(f * peaks * t * 3.14 + p)) for i, (p, m, f) in enumerate(ph))
        pts.append((x, y))
    d = f'M0,{h} ' + ' '.join(f'L{x},{y:.1f}' for x, y in pts) + f' L{w},{h} Z'
    return d

layers = [
    (520, 260, 1.1, 11, '#5d8a92', .9),
    (610, 230, 1.6, 12, '#3f6f6c', 1),
    (720, 200, 2.2, 13, '#2a5249', 1),
    (850, 150, 2.8, 14, '#17332b', 1),
]
ridges = ''.join(f'<path d="{ridge(b, a, pk, s)}" fill="{c}" fill-opacity="{o}"/>' for b, a, pk, s, c, o in layers)
# snow caps on the farthest ridge: lighter thin stroke along the top
hero_svg = f'''<svg class="hero-art" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1d3b44"/>
      <stop offset=".45" stop-color="#5f8c8f"/>
      <stop offset=".78" stop-color="#e9c48a"/>
      <stop offset="1" stop-color="#f2d6a4"/>
    </linearGradient>
    <radialGradient id="sunglow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#ffe3a8" stop-opacity=".9"/>
      <stop offset="1" stop-color="#ffe3a8" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1600" height="1000" fill="url(#sky)"/>
  <circle cx="1120" cy="520" r="260" fill="url(#sunglow)"/>
  <circle cx="1120" cy="520" r="64" fill="#ffe7b5"/>
  <image href="assets/topo.svg" x="0" y="0" width="1600" height="1000" preserveAspectRatio="xMidYMid slice" opacity=".9"/>
  {ridges}
  <path d="M120,940 C340,900 420,820 610,830 S900,760 1010,700 S1220,640 1290,600" fill="none" stroke="#e8a33d" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>
  <circle cx="1290" cy="600" r="7" fill="#e8a33d"/>
  <rect width="1600" height="1000" fill="#0d1f1a" fill-opacity=".18"/>
</svg>'''

# ---------- shared pieces ----------
LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 29 L15 15 L20 22 L25 13 L34 29 Z" fill="currentColor"/><path d="M23 16.2 L25 13 L27 16.2 L25 15.2 Z" fill="#e8a33d"/></svg>'''
IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
INSTAGRAM_URL = 'https://www.instagram.com/'

NAV = [('Home', ''), ('Blog', 'blog/'), ('Tips', 'tips/'), ('Moments', 'moments/'), ('Gallery', 'gallery/'), ('About', 'about/')]

def head(title, desc, base):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>'''

def header(active, base, solid):
    links = ''.join(
        f'<a href="{base}{href}"' + (' aria-current="page"' if name == active else '') + f'>{name}</a>'
        for name, href in NAV)
    return f'''
<header class="site-header{' solid' if solid else ''}">
  <div class="wrap header-row">
    <a class="brand" href="{base}">{LOGO}<span class="brand-name">Miles &amp; Mountains</span></a>
    <nav class="nav-pill" aria-label="Main">{links}</nav>
    <button class="menu-btn" aria-expanded="false" aria-label="Open menu">Menu</button>
    <a class="ig-link" href="{INSTAGRAM_URL}" rel="noopener" target="_blank">{IG}<span>Instagram</span></a>
  </div>
</header>'''

def footer(base):
    return f'''
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="brand" href="{base}">{LOGO}<span class="brand-name">Miles &amp; Mountains</span></a>
      <p>Travel stories, practical tips and small moments from the road.</p>
    </div>
    <div>
      <h4>Read</h4>
      <ul><li><a href="{base}blog/">Blog</a></li><li><a href="{base}tips/">Tips</a></li><li><a href="{base}moments/">Moments</a></li></ul>
    </div>
    <div>
      <h4>More</h4>
      <ul><li><a href="{base}gallery/">Gallery</a></li><li><a href="{base}about/">About</a></li><li><a href="{INSTAGRAM_URL}" rel="noopener" target="_blank">Instagram</a></li></ul>
    </div>
  </div>
  <div class="wrap footer-bottom"><span>© <span data-year>2026</span> Miles &amp; Mountains</span><span>Made by hand, one trip at a time.</span></div>
</footer>
<script src="{base}assets/site.js"></script>
</body>
</html>
'''

EMPTY_ICON = '<svg viewBox="0 0 72 72" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M8 56 L28 26 L38 40 L46 30 L64 56 Z" stroke-linejoin="round"/><path d="M14 64 C26 60 34 64 46 60 S60 62 66 60" stroke-dasharray="2 6" stroke-linecap="round"/></svg>'

# ---------- home ----------
home = head('Miles & Mountains | Travel stories, tips and moments',
            'A personal travel journal: stories from the road, practical tips, small moments and photos.', '') + header('Home', '', False) + f'''
<main id="main">
  <section class="hero" style="padding:0">
    {hero_svg}
    <div class="hero-content">
      <p class="hero-kicker">A travel journal by Alfred</p>
      <h1>Miles <span class="amp">&amp;</span> Mountains</h1>
      <p class="hero-sub">Stories from the road, tips that actually help, and the small moments in between.</p>
      <a class="btn" href="blog/">Read the journal {ARROW}</a>
    </div>
    <div class="wrap hero-meta"><span class="odometer">0 miles logged, the first trip is loading</span><span>Scroll to explore</span></div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <h2>Where to next</h2>
        <p>Trips will be sorted by region here. Pick one to see what's on the list.</p>
      </div>
      <div class="tabs" role="tablist" aria-label="Regions">
        <button class="tab" role="tab" aria-selected="true" data-region="asia">Asia <span class="count">0</span></button>
        <button class="tab" role="tab" aria-selected="false" data-region="europe">Europe <span class="count">0</span></button>
        <button class="tab" role="tab" aria-selected="false" data-region="africa">Africa <span class="count">0</span></button>
        <button class="tab" role="tab" aria-selected="false" data-region="americas">Americas <span class="count">0</span></button>
        <button class="tab" role="tab" aria-selected="false" data-region="oceania">Oceania <span class="count">0</span></button>
      </div>
      <div class="region-panel" role="tabpanel">
        <img class="topo" src="assets/topo.svg" alt="">
        <div>
          <h3 id="region-title">No Asia trips yet</h3>
          <p>The first stories from this part of the map are on their way.</p>
          <p class="places" id="region-places">On the wish list: Japan, Nepal, Vietnam, Indonesia, the Philippines</p>
        </div>
      </div>
    </div>
  </section>

  <section class="journal">
    <div class="wrap">
      <div class="section-head">
        <h2>The journal</h2>
        <p>Three ways to follow along: long reads, quick tips, and snapshots.</p>
      </div>
      <div class="journal-grid">
        <a class="entry entry-blog" href="blog/">
          <img class="topo" src="assets/topo.svg" alt="">
          <div style="position:relative"><h3>Blog</h3><p>Full stories from each trip: the routes, the people, the wrong turns worth taking.</p></div>
          <span class="status" style="position:relative">First story coming soon</span>
        </a>
        <a class="entry entry-tips" href="tips/">
          <div><h3>Tips</h3><p>Packing lists, budgets, visas and the things I wish I'd known.</p></div>
          <span class="status">First tip coming soon</span>
        </a>
        <a class="entry entry-moments" href="moments/">
          <div><h3>Moments</h3><p>One photo, a few words. The small stuff from the road.</p></div>
          <span class="status">First moment coming soon</span>
        </a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <h2>Gallery</h2>
        <a class="btn ghost" href="gallery/">Open the gallery {ARROW}</a>
      </div>
      <div class="frames">
        <div class="frame">Photos from the first trip land here</div>
        <div class="frame"></div>
        <div class="frame"></div>
        <div class="frame"></div>
      </div>
    </div>
  </section>

  <section class="follow">
    <div class="wrap follow-grid">
      <div class="follow-card main">
        <h3>Follow the trip live</h3>
        <p>Daily stories and behind-the-scenes go up on Instagram first. The best of it ends up here.</p>
        <a class="btn" href="{INSTAGRAM_URL}" rel="noopener" target="_blank">Follow on Instagram {ARROW}</a>
      </div>
      <div class="follow-card alt">
        <div><h3>Say hello</h3><p>Got a tip, a question or a trail I should hike? Send me a message on Instagram.</p></div>
        <a class="btn ghost" href="about/">About me {ARROW}</a>
      </div>
    </div>
  </section>
</main>''' + footer('')
(ROOT / 'index.html').write_text(home)

# ---------- inner pages ----------
pages = {
    'blog': ('Blog', 'Full stories from the road, one trip at a time.',
             'No stories yet', 'The first full travel story is being written. Check back soon, or follow along on Instagram in the meantime.'),
    'tips': ('Tips', 'Practical, tested advice: packing, budgets, visas, getting around.',
             'No tips yet', 'Useful, tested advice will show up here after the first trip.'),
    'moments': ('Moments', 'One photo, a few words. The small stuff from the road.',
                'No moments yet', 'Short snapshots from the road will collect here.'),
    'gallery': ('Gallery', 'Photos from every trip, sorted by place.',
                'The gallery is empty', 'Photos will appear here, grouped by destination.'),
}
for slug, (name, intro, etitle, etext) in pages.items():
    html = head(f'{name} | Miles & Mountains', intro, '../') + header(name, '../', True) + f'''
<main id="main">
  <div class="page-hero"><img class="topo" src="../assets/topo.svg" alt=""><div class="wrap"><h1>{name}</h1><p>{intro}</p></div></div>
  <section>
    <div class="wrap">
      <div class="empty">
        {EMPTY_ICON}
        <h2>{etitle}</h2>
        <p>{etext}</p>
        <a class="btn" href="{INSTAGRAM_URL}" rel="noopener" target="_blank">Follow on Instagram {ARROW}</a>
      </div>
    </div>
  </section>
</main>''' + footer('../')
    (ROOT / slug / 'index.html').write_text(html)

about = head('About | Miles & Mountains', 'Who is behind Miles & Mountains.', '../') + header('About', '../', True) + f'''
<main id="main">
  <div class="page-hero"><img class="topo" src="../assets/topo.svg" alt=""><div class="wrap"><h1>About</h1><p>The person behind the miles.</p></div></div>
  <section>
    <div class="wrap prose">
      <p>Hi, I'm Alfred. Miles &amp; Mountains is my travel journal: a place for the long stories, the useful tips and the small moments that don't fit in an Instagram caption.</p>
      <p>This page will grow with a proper introduction, a photo and the places I've been. For now, the best way to say hello is on Instagram.</p>
      <p style="margin-top:28px"><a class="btn" href="{INSTAGRAM_URL}" rel="noopener" target="_blank">Say hi on Instagram {ARROW}</a></p>
    </div>
  </section>
</main>''' + footer('../')
(ROOT / 'about/index.html').write_text(about)

(ROOT / 'assets/favicon.svg').write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="20" fill="#17332b"/>'
    '<path d="M6 29 L15 15 L20 22 L25 13 L34 29 Z" fill="#f6f8f5"/><path d="M23 16.2 L25 13 L27 16.2 L25 15.2 Z" fill="#e8a33d"/></svg>')

(ROOT / '404.html').write_text(head('Page not found | Miles & Mountains', 'Page not found.', '/') + header('', '/', True) + f'''
<main id="main"><section><div class="wrap"><div class="empty">{EMPTY_ICON}<h2>This trail doesn't exist</h2><p>The page you're looking for isn't here. Head back to the start.</p><a class="btn" href="/">Back to home {ARROW}</a></div></div></section></main>''' + footer('/'))
print('done')
