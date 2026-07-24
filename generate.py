#!/usr/bin/env python3
"""Save Godzilla — site generator.
Reads data.json, picks a rotating subset of content, writes index.html.
"""

import json, os, random
from datetime import date, datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')
OUT_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)

def pick_rotating(items, count, seed):
    """Deterministic rotating selection from a pool."""
    rng = random.Random(seed)
    pool = list(items)
    rng.shuffle(pool)
    return pool[:count]

def generate():
    data = load_data()
    week_seed = date.today().isocalendar()[1]  # ISO week number

    # Rotate content
    featured_incidents = pick_rotating(data['incidents'], 5, week_seed)
    featured_testimonials = pick_rotating(data['testimonials'], 3, week_seed + 1)
    featured_press = pick_rotating(data['press_releases'], 4, week_seed + 2)

    # Metrics — subtly increment over time
    weeks_since_launch = max(0, (date.today() - date(2026, 7, 24)).days // 7)
    cities = data['metrics']['cities_protected'] + weeks_since_launch
    threats = data['metrics']['threats_neutralized'] + weeks_since_launch

    # Build incident cards
    incidents_html = ''
    for i, inc in enumerate(featured_incidents):
        full = ' card-full' if i == len(featured_incidents) - 1 and len(featured_incidents) % 2 == 1 else ''
        incidents_html += f'''
      <div class="card{full}">
        <div class="card-label"><span>CASE FILE {inc['id']}</span><span>RECLASSIFIED</span></div>
        <div class="card-title">{inc['title']}</div>
        <div class="card-text">{inc['text']}</div>
      </div>'''

    # Build testimonial cards
    testimonials_html = ''
    for t in featured_testimonials:
        testimonials_html += f'''
      <div class="testimonial-card">
        <div class="testimonial-header">Public Comment Card</div>
        <div class="testimonial-body">
          <p>"{t['text']}"</p>
          <div class="testimonial-name">{t['name']}</div>
          <div class="testimonial-org">{t['org']}</div>
        </div>
      </div>'''

    # Build press bulletin cards
    rotations = [-0.6, 0.5, 0.3, -0.4]
    press_html = ''
    for i, p in enumerate(featured_press):
        rot = rotations[i] if i < len(rotations) else 0
        press_html += f'''
      <div class="bulletin-card" style="transform:rotate({rot}deg);">
        <div class="bulletin-date">{p['date']}</div>
        <div class="bulletin-title">{p['title']}</div>
        <div class="bulletin-text">{p['text']}</div>
      </div>'''

    # Main badge (rotate between a few options)
    badges = [
        'Official Notice &middot; Form GZ-1',
        'Public Advisory &middot; Form GZ-2A',
        'Bureau Statement &middot; Form GZ-4',
        'Community Notice &middot; Form GZ-3',
    ]
    badge = badges[week_seed % len(badges)]

    # CTA subtitle (rotate weekly)
    cta_lines = [
        'The next hearing is Thursday at 7 PM in the Community Room. Public comment is limited to three minutes per resident. Refreshments will be provided.',
        'A special session of the Kaiju Affairs Committee convenes Friday at 6 PM. Written comments may be submitted in advance. Childcare available.',
        'The Bureau will hold open hearings every Tuesday this month. Sign up for public comment at the front desk. Light refreshments will be served.',
        'Quarterly town hall: Saturday at 10 AM at the Municipal Annex. All residents are encouraged to attend. Interpreters will be available.',
    ]
    cta_text = cta_lines[week_seed % len(cta_lines)]

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  body {{ margin: 0; background: #ece3cd; font-family:'Nunito',Verdana,Arial,sans-serif; }}
  * {{ box-sizing: border-box; }}
  a {{ color: #2f4d3a; text-decoration: underline; }}
  a:hover {{ color: #52704e; }}
  ::selection {{ background: #b8943f; color: #2b2b23; }}
  .stripe {{ height:8px; background:repeating-linear-gradient(45deg, #2f4d3a, #2f4d3a 12px, #b8943f 12px, #b8943f 24px); }}
  .nav {{ display:flex; align-items:center; justify-content:space-between; padding:16px 44px; background:#f4efe0; border-bottom:3px solid #2f4d3a; }}
  .logo {{ display:flex; align-items:center; gap:14px; }}
  .logo-icon {{ width:52px; height:52px; border-radius:50%; border:2px solid #2f4d3a; background:#f4efe0; display:flex; align-items:center; justify-content:center; flex-shrink:0; position:relative; }}
  .logo-icon-inner {{ position:absolute; inset:3px; border-radius:50%; border:1px dashed #b8943f; }}
  .org-name {{ font-size:19px; font-weight:700; color:#2f4d3a; line-height:1.1; }}
  .org-sub {{ font-family:'Nunito',Verdana,Arial,sans-serif; font-size:10px; letter-spacing:0.08em; text-transform:uppercase; color:#6b4f36; }}
  .nav-links {{ display:flex; gap:26px; font-size:13px; color:#3a3a2e; }}
  .nav-links a {{ text-decoration:none; color:#3a3a2e; }}
  .nav-links a:hover {{ color:#2f4d3a; font-weight:600; }}
  .btn-primary {{ padding:13px 26px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:13px; border:2px solid #22392a; display:inline-block; cursor:pointer; }}
  .btn-primary:hover {{ background:#3a5e48; }}
  .btn-secondary {{ padding:13px 26px; background:#f4efe0; color:#2f4d3a; font-weight:700; font-size:13px; border:2px solid #2f4d3a; display:inline-block; cursor:pointer; }}
  .btn-secondary:hover {{ background:#e8e0c8; }}
  .section-title {{ display:flex; align-items:baseline; gap:12px; margin-bottom:18px; }}
  .section-title h2 {{ font-size:26px; color:#2f4d3a; margin:0; font-family:'Nunito',Verdana,Arial,sans-serif; }}
  .section-sub {{ font-size:11px; color:#6b4f36; }}
  .container {{ max-width:920px; margin:0 auto; }}
  .page-section {{ padding:0 44px 64px; }}
  .data-table {{ border:2px solid #6b4f36; }}
  .data-table-header {{ display:grid; grid-template-columns:1fr 1fr; }}
  .data-table-header div {{ padding:12px 20px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:12px; text-transform:uppercase; }}
  .data-table-header div:first-child {{ border-right:1px solid #f4efe0; }}
  .data-table-body {{ display:grid; grid-template-columns:1fr 1fr; background:#f4efe0; }}
  .data-table-body div {{ padding:20px; font-size:13px; line-height:1.6; border-bottom:1px solid #d8cba8; }}
  .data-table-body div:nth-child(odd) {{ border-right:1px solid #d8cba8; }}
  .data-table-body div:last-child, .data-table-body div:nth-last-child(2) {{ border-bottom:none; }}
  .card-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }}
  .card {{ background:#f4efe0; border:2px solid #6b4f36; padding:18px 20px; }}
  .card-full {{ grid-column:1 / -1; }}
  .card-label {{ display:flex; justify-content:space-between; font-size:11px; color:#6b4f36; margin-bottom:10px; }}
  .card-title {{ font-weight:700; font-size:16px; color:#2f4d3a; margin-bottom:6px; }}
  .card-text {{ font-size:13px; line-height:1.6; color:#3a3a2e; }}
  .testimonial-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
  .testimonial-card {{ background:#f4efe0; border:2px solid #6b4f36; }}
  .testimonial-header {{ background:#b8943f; color:#2b2b23; font-size:10px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; padding:6px 14px; }}
  .testimonial-body {{ padding:18px 20px; }}
  .testimonial-body p {{ font-size:14px; font-style:italic; line-height:1.6; margin:0 0 14px; color:#2b2b23; }}
  .testimonial-name {{ font-size:12px; font-weight:700; color:#2f4d3a; }}
  .testimonial-org {{ font-size:11px; color:#6b4f36; }}
  .bulletin-board {{ background:#d9cba3; border:2px solid #6b4f36; padding:22px; display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }}
  .bulletin-card {{ background:#f8f4e8; padding:16px 18px; border:1px solid #b8943f; box-shadow:2px 2px 0 rgba(107,79,54,0.2); }}
  .bulletin-date {{ font-size:10px; color:#6b4f36; margin-bottom:6px; }}
  .bulletin-title {{ font-weight:700; font-size:14px; color:#2f4d3a; margin-bottom:6px; }}
  .bulletin-text {{ font-size:12px; color:#3a3a2e; line-height:1.5; }}
  .cta-box {{ background:#2f4d3a; color:#f4efe0; padding:48px 56px; text-align:center; border:2px solid #22392a; }}
  .cta-label {{ font-size:11px; letter-spacing:0.1em; text-transform:uppercase; color:#d8c98a; margin-bottom:14px; }}
  .cta-title {{ font-size:30px; margin:0 0 16px; }}
  .cta-text {{ font-size:14px; color:#d8dbd4; max-width:540px; margin:0 auto 28px; line-height:1.7; }}
  .footer {{ padding:26px 44px; background:#dcd0ac; border-top:3px solid #2f4d3a; font-size:11px; color:#5c4a35; }}
  .footer-inner {{ max-width:920px; margin:0 auto; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
  @media (max-width:768px) {{
    .nav {{ flex-direction:column; gap:12px; padding:16px 20px; }}
    .nav-links {{ flex-wrap:wrap; justify-content:center; gap:16px; }}
    .card-grid {{ grid-template-columns:1fr; }}
    .testimonial-grid {{ grid-template-columns:1fr; }}
    .bulletin-board {{ grid-template-columns:1fr; }}
    .data-table-body {{ grid-template-columns:1fr; }}
    .data-table-body div:nth-child(odd) {{ border-right:none; }}
    .page-section {{ padding:0 20px 44px; }}
    .cta-box {{ padding:32px 24px; }}
    .cta-title {{ font-size:24px; }}
  }}
</style>
</head>
<body>

<div class="stripe"></div>

<!-- NAV -->
<div class="nav">
  <div class="logo">
    <div class="logo-icon">
      <div class="logo-icon-inner"></div>
      <div class="logo-icon-g">
        <div style="position:absolute;top:0;left:0;width:2px;height:2px;background:transparent;transform:scale(0.44);transform-origin:top left;box-shadow:28px 0px 0 0 #2f4d3a,20px 4px 0 0 #2f4d3a,28px 4px 0 0 #2f4d3a,36px 4px 0 0 #2f4d3a,12px 8px 0 0 #2f4d3a,20px 8px 0 0 #2f4d3a,24px 8px 0 0 #2f4d3a,28px 8px 0 0 #2f4d3a,32px 8px 0 0 #2f4d3a,36px 8px 0 0 #2f4d3a,8px 12px 0 0 #2f4d3a,12px 12px 0 0 #2f4d3a,16px 12px 0 0 #2f4d3a,20px 12px 0 0 #2f4d3a,24px 12px 0 0 #2f4d3a,28px 12px 0 0 #2f4d3a,32px 12px 0 0 #2f4d3a,36px 12px 0 0 #2f4d3a,40px 12px 0 0 #2f4d3a,4px 16px 0 0 #2f4d3a,8px 16px 0 0 #2f4d3a,12px 16px 0 0 #2f4d3a,16px 16px 0 0 #2f4d3a,20px 16px 0 0 #2f4d3a,24px 16px 0 0 #2f4d3a,28px 16px 0 0 #2f4d3a,32px 16px 0 0 #2f4d3a,36px 16px 0 0 #2f4d3a,40px 16px 0 0 #2f4d3a,44px 16px 0 0 #2f4d3a,0px 20px 0 0 #2f4d3a,4px 20px 0 0 #2f4d3a,8px 20px 0 0 #2f4d3a,12px 20px 0 0 #2f4d3a,16px 20px 0 0 #2f4d3a,20px 20px 0 0 #2f4d3a,24px 20px 0 0 #2f4d3a,28px 20px 0 0 #2f4d3a,32px 20px 0 0 #2f4d3a,36px 20px 0 0 #2f4d3a,40px 20px 0 0 #2f4d3a,4px 24px 0 0 #2f4d3a,8px 24px 0 0 #2f4d3a,12px 24px 0 0 #2f4d3a,16px 24px 0 0 #2f4d3a,20px 24px 0 0 #2f4d3a,24px 24px 0 0 #2f4d3a,28px 24px 0 0 #2f4d3a,32px 24px 0 0 #2f4d3a,36px 24px 0 0 #2f4d3a,8px 28px 0 0 #2f4d3a,12px 28px 0 0 #2f4d3a,16px 28px 0 0 #2f4d3a,20px 28px 0 0 #2f4d3a,24px 28px 0 0 #2f4d3a,28px 28px 0 0 #2f4d3a,32px 28px 0 0 #2f4d3a,12px 32px 0 0 #2f4d3a,16px 32px 0 0 #2f4d3a,28px 32px 0 0 #2f4d3a,32px 32px 0 0 #2f4d3a,12px 36px 0 0 #2f4d3a,16px 36px 0 0 #2f4d3a,28px 36px 0 0 #2f4d3a,32px 36px 0 0 #2f4d3a,12px 40px 0 0 #2f4d3a,16px 40px 0 0 #2f4d3a,28px 40px 0 0 #2f4d3a,32px 40px 0 0 #2f4d3a,12px 44px 0 0 #2f4d3a,16px 44px 0 0 #2f4d3a,28px 44px 0 0 #2f4d3a,32px 44px 0 0 #2f4d3a,8px 48px 0 0 #2f4d3a,12px 48px 0 0 #2f4d3a,16px 48px 0 0 #2f4d3a,28px 48px 0 0 #2f4d3a,32px 48px 0 0 #2f4d3a,36px 48px 0 0 #2f4d3a;"></div>
      </div>
    </div>
    <div>
      <div class="org-name">Save Godzilla</div>
      <div class="org-sub">Municipal Bureau of Kaiju Affairs</div>
    </div>
  </div>
  <div class="nav-links">
    <a href="#myths">Myths &amp; Facts</a>
    <a href="#incidents">Incident Tracker</a>
    <a href="#testimonials">Testimonials</a>
    <a href="#press">Press Room</a>
  </div>
  <div>
    <span class="btn-primary">ATTEND A HEARING</span>
  </div>
</div>

<!-- HERO -->
<div style="padding:64px 44px; background:#ece3cd;">
  <div class="container" style="background:#f4efe0; border:2px solid #6b4f36; padding:48px 56px; box-shadow:6px 6px 0 rgba(107,79,54,0.15);">
    <div style="display:inline-block; padding:5px 14px; background:#b8943f; color:#2b2b23; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:22px;">{badge}</div>
    <h1 style="font-size:44px; line-height:1.25; font-weight:700; color:#2f4d3a; margin:0 0 20px;">Godzilla is not a monster. He's a sovereign ecological force.</h1>
    <p style="font-size:15px; line-height:1.75; color:#3a3a2e; margin:0 0 28px; max-width:640px;">For decades, media conglomerates and military interests have slandered a being who has repeatedly saved our planet from existential threats. The Municipal Bureau of Kaiju Affairs hereby affirms its commitment to the evidence-based reconsideration of Godzilla's public standing. One hearing at a time.</p>
    <div style="display:flex; gap:14px; flex-wrap:wrap;">
      <span class="btn-primary">Submit a Public Comment</span>
      <span class="btn-secondary">Download the Impact Packet (PDF)</span>
    </div>
  </div>
</div>

<!-- METRICS -->
<div class="page-section">
  <div class="container" style="border:2px solid #6b4f36;">
    <div style="background:#2f4d3a; color:#f4efe0; font-size:12px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; padding:10px 18px;">Bureau Statistics &middot; Fiscal Year 2026</div>
    <div style="display:grid; grid-template-columns:repeat(4,1fr); background:#f4efe0;">
      <div style="padding:24px 16px; text-align:center; border-right:1px solid #d8cba8;">
        <div style="font-size:32px; font-weight:700; color:#2f4d3a;">{cities}</div>
        <div style="font-size:11px; color:#6b4f36; margin-top:6px;">Cities Protected</div>
      </div>
      <div style="padding:24px 16px; text-align:center; border-right:1px solid #d8cba8;">
        <div style="font-size:32px; font-weight:700; color:#2f4d3a;">{threats}</div>
        <div style="font-size:11px; color:#6b4f36; margin-top:6px;">Threats Neutralized</div>
      </div>
      <div style="padding:24px 16px; text-align:center; border-right:1px solid #d8cba8;">
        <div style="font-size:32px; font-weight:700; color:#2f4d3a;">0</div>
        <div style="font-size:11px; color:#6b4f36; margin-top:6px;">Unprovoked Attacks</div>
      </div>
      <div style="padding:24px 16px; text-align:center;">
        <div style="font-size:32px; font-weight:700; color:#2f4d3a;">{data['metrics']['years_of_service']}</div>
        <div style="font-size:11px; color:#6b4f36; margin-top:6px;">Years of Service</div>
      </div>
    </div>
  </div>
</div>

<!-- MYTHS VS FACTS -->
<div id="myths" class="page-section">
  <div class="container">
    <div class="section-title">
      <h2>Myths &amp; Facts</h2>
      <span class="section-sub">(Fact Sheet 3-B)</span>
    </div>
    <div class="data-table">
      <div class="data-table-header">
        <div>Common Misconception</div>
        <div>Bureau Finding</div>
      </div>
      <div class="data-table-body">
{''.join(f'        <div>{m["myth"]}</div>\n        <div>{m["fact"]}</div>' for m in data['myths'])}
      </div>
    </div>
  </div>
</div>

<!-- INCIDENT TRACKER -->
<div id="incidents" class="page-section">
  <div class="container">
    <div class="section-title">
      <h2>Incident Tracker</h2>
      <span class="section-sub">({len(featured_incidents)} cases on file, reclassified)</span>
    </div>
    <div class="card-grid">
{incidents_html}
    </div>
  </div>
</div>

<!-- TESTIMONIALS -->
<div id="testimonials" class="page-section">
  <div class="container">
    <div class="section-title">
      <h2>Public Comment Cards</h2>
      <span class="section-sub">(Submitted at open hearings)</span>
    </div>
    <div class="testimonial-grid">
{testimonials_html}
    </div>
  </div>
</div>

<!-- PRESS ROOM -->
<div id="press" class="page-section">
  <div class="container">
    <div class="section-title">
      <h2>Press Room</h2>
      <span class="section-sub">(Bulletin board, updated monthly)</span>
    </div>
    <div class="bulletin-board">
{press_html}
    </div>
  </div>
</div>

<!-- CTA -->
<div class="page-section">
  <div class="container">
    <div class="cta-box">
      <div class="cta-label">Notice of Public Hearing</div>
      <h2 class="cta-title">Godzilla can't speak for himself.<br>That's why we're here.</h2>
      <p class="cta-text">{cta_text}</p>
      <div style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap;">
        <span class="btn-primary" style="background:#b8943f; color:#2b2b23; border:2px solid #8a6f30;">RSVP for the Hearing</span>
        <span class="btn-secondary" style="color:#f4efe0; border-color:#f4efe0; background:transparent;">Sign the Petition</span>
      </div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<div class="footer">
  <div class="footer-inner">
    <div>Municipal Bureau of Kaiju Affairs &middot; Est. 1954 &middot; Office Hours: Mon&ndash;Fri, 8 AM&ndash;4:30 PM</div>
    <div>Form GZ-1 (Rev. 2026) &middot; Godzilla is a trademark of Toho Co., Ltd. This is an independent advocacy group.</div>
  </div>
</div>

</body>
</html>'''

    with open(OUT_PATH, 'w') as f:
        f.write(html)

    print(f'Generated {OUT_PATH}')
    print(f'  Incidents: {len(featured_incidents)}')
    print(f'  Testimonials: {len(featured_testimonials)}')
    print(f'  Press items: {len(featured_press)}')
    print(f'  Cities: {cities}, Threats: {threats}')

if __name__ == '__main__':
    generate()
