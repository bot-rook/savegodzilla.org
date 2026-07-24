#!/usr/bin/env python3
"""Save Godzilla — multi-page site generator.
Produces: index.html, about.html, incidents.html, press.html, contact.html
"""
import json, os, random
from datetime import date

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')
OUT_DIR = os.path.dirname(__file__)

def load():
    with open(DATA_PATH) as f:
        return json.load(f)

def pick(items, count, seed):
    r = random.Random(seed)
    pool = list(items)
    r.shuffle(pool)
    return pool[:count]

def fmt_date(d):
    return d.strftime('%b %d, %Y').upper()

def nav(page, logo='Save Godzilla', sub='Municipal Bureau of Kaiju Affairs'):
    links = [
        ('index.html', 'Home'),
        ('petition.html', 'Petition'),
        ('about.html', 'About'),
        ('incidents.html', 'Incidents'),
        ('press.html', 'Press'),
        ('contact.html', 'Contact'),
    ]
    ls = ''.join(f'<a href="{u}"{" style=font-weight:700;color:#2f4d3a" if u==page else ""} onclick="closeNav()">{l}</a>' for u, l in links)
    return f'''<div class="nav">
  <div class="logo" onclick="window.location='index.html'" style="cursor:pointer">
    <div class="logo-icon">
      <svg viewBox="0 0 120 120" style="width:52px;height:52px;">
        <!-- Outer ring -->
        <circle cx="60" cy="60" r="56" fill="#f4efe0" stroke="#2f4d3a" stroke-width="3"/>
        <circle cx="60" cy="60" r="52" fill="none" stroke="#2f4d3a" stroke-width="0.5"/>
        <!-- Dashed inner ring -->
        <circle cx="60" cy="60" r="49" fill="none" stroke="#b8943f" stroke-width="1.5" stroke-dasharray="3 3"/>
        <!-- Text top -->
        <path id="toparc" d="M 20 60 A 40 40 0 0 1 100 60" fill="none"/>
        <text font-size="6.5" font-weight="800" fill="#2f4d3a" font-family="Nunito" letter-spacing="2">
          <textPath href="#toparc" startOffset="50%" text-anchor="middle">MUNICIPAL BUREAU</textPath>
        </text>
        <!-- Text bottom -->
        <path id="botarc" d="M 100 60 A 40 40 0 0 1 20 60" fill="none"/>
        <text font-size="6.5" font-weight="800" fill="#2f4d3a" font-family="Nunito" letter-spacing="1.5">
          <textPath href="#botarc" startOffset="50%" text-anchor="middle">KAIJU AFFAIRS</textPath>
        </text>
        <!-- Year -->
        <text x="60" y="113" text-anchor="middle" font-size="5" font-weight="700" fill="#6b4f36" font-family="Nunito" letter-spacing="1">EST. 1954</text>
        <!-- Inner circle background -->
        <circle cx="60" cy="58" r="24" fill="#f4efe0" stroke="#2f4d3a" stroke-width="1"/>
        <!-- Godzilla silhouette - detailed -->
        <g transform="translate(60,56)" fill="#2f4d3a">
          <!-- Body -->
          <path d="M-14 4 L-10 -2 L-6 -4 L-4 -10 L0 -14 L4 -14 L8 -10 L12 -8 L14 -4 L16 0 L16 6 L12 8 L10 10 L8 14 L4 16 L0 18 L-4 18 L-8 16 L-12 14 L-14 10 L-16 6 L-14 4 Z"/>
          <!-- Tail -->
          <path d="M-14 4 L-18 0 L-16 -4 L-14 -2 Z"/>
          <!-- Left leg -->
          <path d="M-8 16 L-10 20 L-6 20 L-4 16 Z"/>
          <!-- Right leg -->
          <path d="M4 16 L6 20 L10 20 L8 16 Z"/>
          <!-- Dorsal fins -->
          <path d="M-2 -12 L0 -18 L2 -12 Z" fill="#b8943f"/>
          <path d="M2 -10 L4 -15 L6 -10 Z" fill="#b8943f"/>
          <path d="M6 -8 L8 -12 L10 -8 Z" fill="#b8943f"/>
          <!-- Eye -->
          <circle cx="10" cy="-6" r="1.5" fill="#b8943f"/>
          <!-- Atomic breath line -->
          <line x1="12" y1="-4" x2="18" y2="-8" stroke="#b8943f" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="13" y1="-3" x2="17" y2="-6" stroke="#b8943f" stroke-width="0.5" stroke-linecap="round" opacity="0.6"/>
        </g>
        <!-- Stars -->
        <circle cx="30" cy="30" r="1.5" fill="#b8943f" opacity="0.5"/>
        <circle cx="90" cy="30" r="1.5" fill="#b8943f" opacity="0.5"/>
        <circle cx="30" cy="86" r="1.5" fill="#b8943f" opacity="0.5"/>
        <circle cx="90" cy="86" r="1.5" fill="#b8943f" opacity="0.5"/>
      </svg>
    </div>
    <div>
      <div class="org-name">{logo}</div>
      <div class="org-sub">{sub}</div>
    </div>
  </div>
  <div class="nav-links">{ls}</div>
  <div><a href="index.html#support" class="btn-primary" style="text-decoration:none">DONATE</a></div>
  <button class="hamburger" id="hamburger" onclick="toggleNav()" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</div>
<div class="nav-overlay" id="navOverlay">
  <button class="close-btn" onclick="closeNav()" aria-label="Close menu">&times;</button>
  {ls}
  <a href="petition.html" class="donate-btn" onclick="closeNav()" style="margin-bottom:12px">SIGN THE PETITION</a>
  <a href="index.html#support" class="donate-btn" onclick="closeNav()">DONATE</a>
</div>
<script>
var overlay = document.getElementById('navOverlay');
var ham = document.getElementById('hamburger');
function toggleNav() {{
  var o = overlay.classList.toggle('open');
  ham.classList.toggle('open');
  document.body.style.overflow = o ? 'hidden' : '';
}}
function closeNav() {{
  overlay.classList.remove('open');
  ham.classList.remove('open');
  document.body.style.overflow = '';
}}
</script>'''

FOOTER = '''<footer><div class="footer-inner">
    <div>Municipal Bureau of Kaiju Affairs &middot; Est. 1954 &middot; Office Hours: Mon&ndash;Fri, 8 AM&ndash;4:30 PM</div>
    <div>Form GZ-1 (Rev. 2026) &middot; Godzilla is a trademark of Toho Co., Ltd. This is an independent advocacy group.</div>
  </div>
</footer>'''

CSS = '''body { margin:0; background:#ece3cd; font-family:'Nunito',Verdana,Arial,sans-serif; }
* { box-sizing:border-box; }
a { color:#2f4d3a; }
::selection { background:#b8943f; color:#2b2b23; }
.stripe { height:8px; background:repeating-linear-gradient(45deg,#2f4d3a,#2f4d3a 12px,#b8943f 12px,#b8943f 24px); }
.nav { display:flex; align-items:center; justify-content:space-between; padding:16px 44px; background:#f4efe0; border-bottom:3px solid #2f4d3a; flex-wrap:wrap; gap:12px; }
.logo { display:flex; align-items:center; gap:14px; }
.logo-icon { width:52px; height:52px; border-radius:50%; border:2px solid #2f4d3a; background:#f4efe0; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.org-name { font-size:19px; font-weight:700; color:#2f4d3a; line-height:1.1; }
.org-sub { font-size:10px; letter-spacing:0.08em; text-transform:uppercase; color:#6b4f36; }
.nav-links { display:flex; gap:26px; font-size:13px; color:#3a3a2e; flex-wrap:wrap; }
.nav-links a { text-decoration:none; color:#3a3a2e; }
.nav-links a:hover { color:#2f4d3a; }
.hamburger { display:none; flex-direction:column; justify-content:center; gap:5px; cursor:pointer; padding:6px; background:none; border:2px solid #2f4d3a; border-radius:4px; min-width:44px; min-height:44px; align-items:center; }
.hamburger span { display:block; width:22px; height:2.5px; background:#2f4d3a; border-radius:2px; transition:transform 0.3s,opacity 0.3s; }
.hamburger.open span:nth-child(1) { transform:translateY(7.5px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity:0; }
.hamburger.open span:nth-child(3) { transform:translateY(-7.5px) rotate(-45deg); }
.nav-overlay { display:none; }
@media (max-width:768px) {
  .nav { flex-direction:row; flex-wrap:wrap; align-items:center; padding:12px 16px; gap:8px; }
  .hamburger { display:flex; }
  .nav-links { display:none; }
  .nav .btn-primary { display:none; }
  .nav-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#f4efe0; z-index:1000; flex-direction:column; padding:80px 24px 24px; overflow-y:auto; }
  .nav-overlay.open { display:flex; }
  .nav-overlay .close-btn { position:absolute; top:16px; right:16px; background:none; border:2px solid #2f4d3a; border-radius:4px; min-width:44px; min-height:44px; display:flex; align-items:center; justify-content:center; font-size:24px; color:#2f4d3a; cursor:pointer; }
  .nav-overlay a { display:block; padding:16px 0; font-size:18px; font-weight:700; color:#2f4d3a; text-decoration:none; border-bottom:1px solid #d8cba8; }
  .nav-overlay a:hover { color:#b8943f; }
  .nav-overlay .donate-btn { margin-top:24px; padding:16px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:16px; text-align:center; border:2px solid #22392a; text-decoration:none; border-radius:4px; }
}
.btn-primary { padding:13px 26px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:13px; border:2px solid #22392a; display:inline-block; cursor:pointer; }
.btn-primary:hover { background:#3a5e48; }
.btn-gold { padding:13px 26px; background:#b8943f; color:#2b2b23; font-weight:700; font-size:13px; border:2px solid #8a6f30; display:inline-block; cursor:pointer; }
.btn-gold:hover { background:#c8a44f; }
.btn-secondary { padding:13px 26px; background:transparent; color:#2f4d3a; font-weight:700; font-size:13px; border:2px solid #2f4d3a; display:inline-block; cursor:pointer; }
.btn-secondary:hover { background:#e8e0c8; }
.container { max-width:920px; margin:0 auto; }
.page-section { padding:0 44px 64px; }
.section-title { display:flex; align-items:baseline; gap:12px; margin-bottom:18px; }
.section-title h2 { font-size:26px; color:#2f4d3a; margin:0; }
.section-sub { font-size:11px; color:#6b4f36; }
.data-table { border:2px solid #6b4f36; }
.data-table-header { display:grid; grid-template-columns:1fr 1fr; }
.data-table-header div { padding:12px 20px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:12px; text-transform:uppercase; }
.data-table-header div:first-child { border-right:1px solid #f4efe0; }
.data-table-body { display:grid; grid-template-columns:1fr 1fr; background:#f4efe0; }
.data-table-body div { padding:20px; font-size:13px; line-height:1.6; border-bottom:1px solid #d8cba8; }
.data-table-body div:nth-child(odd) { border-right:1px solid #d8cba8; }
.data-table-body div:last-child,.data-table-body div:nth-last-child(2) { border-bottom:none; }
.card-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }
.card { background:#f4efe0; border:2px solid #6b4f36; padding:18px 20px; }
.card-full { grid-column:1/-1; }
.card-label { display:flex; justify-content:space-between; font-size:11px; color:#6b4f36; margin-bottom:10px; }
.card-title { font-weight:700; font-size:16px; color:#2f4d3a; margin-bottom:6px; }
.card-text { font-size:13px; line-height:1.6; color:#3a3a2e; }
.card-grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.team-card { background:#f4efe0; border:2px solid #6b4f36; padding:18px 20px; }
.team-name { font-weight:700; font-size:15px; color:#2f4d3a; }
.team-title { font-size:11px; color:#6b4f36; margin-bottom:8px; }
.team-bio { font-size:13px; line-height:1.6; color:#3a3a2e; }
.timeline { border-left:3px solid #2f4d3a; padding-left:20px; }
.timeline-item { margin-bottom:20px; position:relative; }
.timeline-item::before { content:''; position:absolute; left:-26px; top:6px; width:10px; height:10px; background:#b8943f; border:2px solid #2f4d3a; border-radius:50%; }
.timeline-year { font-weight:700; font-size:14px; color:#2f4d3a; }
.timeline-text { font-size:13px; line-height:1.6; color:#3a3a2e; }
.testimonial-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.testimonial-card { background:#f4efe0; border:2px solid #6b4f36; }
.testimonial-header { background:#b8943f; color:#2b2b23; font-size:10px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; padding:6px 14px; }
.testimonial-body { padding:18px 20px; }
.testimonial-body p { font-size:14px; font-style:italic; line-height:1.6; margin:0 0 14px; color:#2b2b23; }
.testimonial-name { font-size:12px; font-weight:700; color:#2f4d3a; }
.testimonial-org { font-size:11px; color:#6b4f36; }
.bulletin-board { background:#d9cba3; border:2px solid #6b4f36; padding:22px; display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }
.bulletin-card { background:#f8f4e8; padding:16px 18px; border:1px solid #b8943f; box-shadow:2px 2px 0 rgba(107,79,54,0.2); }
.bulletin-date { font-size:10px; color:#6b4f36; margin-bottom:6px; }
.bulletin-title { font-weight:700; font-size:14px; color:#2f4d3a; margin-bottom:6px; }
.bulletin-text { font-size:12px; color:#3a3a2e; line-height:1.5; }
.cta-box { background:#2f4d3a; color:#f4efe0; padding:48px 56px; text-align:center; border:2px solid #22392a; }
.cta-label { font-size:11px; letter-spacing:0.1em; text-transform:uppercase; color:#d8c98a; margin-bottom:14px; }
.cta-title { font-size:30px; margin:0 0 16px; }
.cta-text { font-size:14px; color:#d8dbd4; max-width:540px; margin:0 auto 28px; line-height:1.7; }
.footer { padding:26px 44px; background:#dcd0ac; border-top:3px solid #2f4d3a; font-size:11px; color:#5c4a35; }
.footer-inner { max-width:920px; margin:0 auto; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }
.tier-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
.tier-card { background:#f4efe0; border:2px solid #6b4f36; padding:24px 20px; text-align:center; }
.tier-name { font-weight:700; font-size:16px; color:#2f4d3a; margin-bottom:4px; }
.tier-amount { font-size:28px; font-weight:800; color:#b8943f; margin-bottom:4px; }
.tier-interval { font-size:11px; color:#6b4f36; margin-bottom:12px; }
.tier-perks { font-size:12px; color:#3a3a2e; line-height:1.6; }
.impact-list { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }
.impact-item { background:#f4efe0; border:1px solid #d8cba8; padding:14px 18px; font-size:13px; color:#3a3a2e; }
.impact-item strong { color:#2f4d3a; }
.signer-item { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #d8cba8; font-size:13px; }
.signer-item:last-child { border-bottom:none; }
.signer-name { font-weight:600; color:#2f4d3a; }
.signer-muni { font-size:11px; color:#6b4f36; }
.petition-bar { background:#f4efe0; border:2px solid #6b4f36; padding:24px; text-align:center; }
.petition-bar .progress { height:24px; background:#d8cba8; border:1px solid #6b4f36; margin:12px 0; position:relative; overflow:hidden; }
.petition-bar .progress-fill { height:100%; background:#2f4d3a; transition:width 0.5s; }
.petition-bar .stats { display:flex; justify-content:space-between; font-size:13px; color:#3a3a2e; }
@media (max-width:768px) {
  .logo-icon { width:40px; height:40px; }
  .org-name { font-size:16px; }
  .org-sub { font-size:9px; }
  .btn-primary,.btn-secondary,.btn-gold { padding:12px 20px; font-size:13px; min-height:44px; display:flex; align-items:center; justify-content:center; }
  .page-section { padding:0 16px 36px; }
  .section-title h2 { font-size:22px; }
  .container { max-width:100%; }
  .card-grid,.card-grid-3,.tier-grid,.impact-list { grid-template-columns:1fr; }
  .testimonial-grid { grid-template-columns:1fr; }
  .bulletin-board { grid-template-columns:1fr; }
  .data-table-body { grid-template-columns:1fr; }
  .data-table-body div:nth-child(odd) { border-right:none; }
  .data-table { font-size:12px; }
  .data-table-header div { padding:10px 14px; font-size:11px; }
  .data-table-body div { padding:14px; font-size:12px; }
  .cta-box { padding:28px 20px; }
  .cta-title { font-size:22px; }
  .cta-text { font-size:13px; }
  .footer { padding:20px 16px; font-size:10px; }
  .footer-inner { flex-direction:column; text-align:center; }
  .petition-bar { padding:18px; }
  .petition-bar .stats { flex-direction:column; gap:4px; font-size:12px; }
  .petition-bar .progress { height:20px; }
  .tier-card { padding:18px 16px; }
  .tier-amount { font-size:24px; }
  .impact-item { padding:12px 14px; font-size:12px; }
  .card { padding:14px 16px; }
  .card-title { font-size:15px; }
  .card-text { font-size:12px; }
  .team-card { padding:14px 16px; }
  .timeline { padding-left:16px; }
  .timeline-item::before { left:-22px; width:8px; height:8px; }
  .stripe { height:6px; }
  .bulletin-card { padding:12px 14px; }
  .bulletin-title { font-size:13px; }
  .bulletin-text { font-size:11px; }
  div[style*="padding:60px 44px"] { padding:32px 16px !important; }
  div[style*="padding:48px 56px"] { padding:28px 20px !important; }
  div[style*="padding:40px 48px"] { padding:28px 20px !important; }
  h1[style*="font-size:44px"] { font-size:28px !important; }
  h1[style*="font-size:36px"] { font-size:24px !important; }
  div[style*="grid-template-columns:repeat(4,1fr)"] { grid-template-columns:repeat(2,1fr) !important; }
  div[style*="grid-template-columns:1fr 1fr"] { grid-template-columns:1fr !important; }
  div[style*="display:grid;grid-template-columns:1fr 1fr"] { grid-template-columns:1fr !important; }
  div[style*="padding:24px 16px;text-align:center"] { padding:16px 12px !important; }
  div[style*="font-size:32px;font-weight:700"] { font-size:24px !important; }
}'''

def page(title, body, active):
    meta_desc = 'Help us reclassify Godzilla as a Protected Ecological Asset. Sign the petition, view incident reports, and support kaiju advocacy. Municipal Bureau of Kaiju Affairs — Est. 1954.'
    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="alternate icon" href="favicon.ico" type="image/x-icon">
<link rel="canonical" href="https://savegodzilla.org/{active}">
<meta name="description" content="{meta_desc}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:url" content="https://savegodzilla.org/{active}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://savegodzilla.org/favicon.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta_desc}">
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Municipal Bureau of Kaiju Affairs",
  "url": "https://savegodzilla.org",
  "description": "{meta_desc}",
  "foundingDate": "1954",
  "logo": "https://savegodzilla.org/favicon.svg"
}}</script>
<title>{title}</title>
</head><body>
<a href="#main-content" class="skip-link" style="position:absolute;left:-9999px;top:0;z-index:9999;padding:8px 16px;background:#2f4d3a;color:#f4efe0;font-weight:700;font-size:14px;text-decoration:none;">Skip to main content</a>
<style>a.skip-link:focus {{ left:0; }}</style>
<div class="stripe"></div>
{nav(active)}
<main id="main-content">
{body}
</main>
{FOOTER}
<script>
var API = 'https://petition-savegodzilla.loca.lt';
(function(){{
  fetch(API+'/api/count').then(function(r){{return r.json()}}).then(function(d){{
    var bars = document.querySelectorAll('.live-count');
    for (var i=0;i<bars.length;i++) bars[i].textContent = d.count.toLocaleString();
    var pct = Math.min(100, Math.round(d.count/100000*100));
    var fills = document.querySelectorAll('.live-fill');
    for (var i=0;i<fills.length;i++) fills[i].style.width = pct+'%';
    var list = document.getElementById('recentSigners');
    if (list && d.recent) {{
      list.innerHTML = '';
      d.recent.forEach(function(s){{
        var li = document.createElement('div');
        li.className = 'signer-item';
        li.innerHTML = '<span class="signer-name">'+s.name+'</span><span class="signer-muni">'+s.municipality+'</span>';
        list.appendChild(li);
      }});
    }}
  }}).catch(function(e){{}});
}})();

// Signature milestone celebration
(function() {{
  var milestones = [1000, 5000, 10000, 25000, 50000, 75000, 100000];
  var lastMilestone = localStorage.getItem('sg_last_milestone') || 0;
  fetch(API+'/api/count').then(function(r){{return r.json()}}).then(function(d){{ 
    var count = d.count;
    for (var i=0;i<milestones.length;i++) {{
      if (count >= milestones[i] && milestones[i] > lastMilestone) {{
        localStorage.setItem('sg_last_milestone', milestones[i]);
        var banner = document.createElement('div');
        banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#b8943f;color:#2b2b23;padding:20px 24px;text-align:center;font-weight:700;font-size:18px;z-index:9999;border-top:3px solid #2f4d3a;cursor:pointer;animation:slideUp 0.5s ease;';
        banner.innerHTML = '🎉 <strong>' + milestones[i].toLocaleString() + ' signatures!</strong> Thank you for your support. <span style="text-decoration:underline;margin-left:12px;">Dismiss</span>';
        banner.onclick = function(){{this.remove()}};
        document.body.appendChild(banner);
        setTimeout(function(){{banner.remove()}}, 10000);
        break;
      }}
    }}
  }}).catch(function(e){{}});
}})();
</script>
</body></html>'''

def generate_index(d):
    w = d['petition']['goal']
    n = d['petition']['signatures']
    pct = min(100, round(n / w * 100))
    weeks = (date.today() - date(2026, 7, 24)).days // 7
    cities = d['metrics']['cities_protected'] + weeks
    threats = d['metrics']['threats_neutralized'] + weeks

    # Tiers
    tiers = ''.join(f'<div class="tier-card"><div class="tier-name">{t["name"]}</div><div class="tier-amount">${t["amount"]}</div><div class="tier-interval">per {t["interval"]}</div><div class="tier-perks">{t["perks"]}</div></div>' for t in d['donation_tiers'])

    # Impact
    impacts = ''.join(f'<div class="impact-item"><strong>${i["cost"]}</strong> {i["action"]}</div>' for i in d['impact_items'])

    # Incidents with icons
    inc_icons = {
        'Tokyo': 'M4 16 L8 8 L12 16 L8 14 Z',  # wave
        'San Francisco': 'M8 4 L16 20 L0 20 Z',  # building
        'Boston': 'M12 2 L18 8 L14 8 L14 14 L10 14 L10 8 L6 8 Z',  # star
        'Rio': 'M4 12 A8 8 0 1 1 20 12 A8 8 0 1 1 4 12',  # biohazard-ish
        'Sydney': 'M4 20 L12 4 L20 20 Z',  # mountain
        'Osaka': 'M4 18 L12 6 L20 18 Z',  # roof
        'Bay Harbor': 'M4 16 L8 8 L12 16 L8 14 Z',  # wave
    }
    incs = pick(d['incidents'], 5, date.today().isocalendar()[1])
    incs_html = ''
    for i, inc in enumerate(incs):
        full = ' card-full' if i == len(incs)-1 and len(incs)%2==1 else ''
        incs_html += f'<a href="incidents.html" style="text-decoration:none;display:block"><div class="card{full}"><div class="card-label"><span>CASE FILE {inc["id"]}</span><span>RECLASSIFIED</span></div><div class="card-title">{inc["title"]}</div><div class="card-text">{inc["text"]}</div></div></a>'

    # Testimonials
    tests = pick(d['testimonials'], 3, date.today().isocalendar()[1] + 1)
    tests_html = ''.join(f'<a href="about.html#team" style="text-decoration:none;display:block"><div class="testimonial-card"><div class="testimonial-header">Public Comment Card</div><div class="testimonial-body"><p>"{t["text"]}"</p><div class="testimonial-name">{t["name"]}</div><div class="testimonial-org">{t["org"]}</div></div></div></a>' for t in tests)

    # Press
    presses = pick(d['press_releases'], 4, date.today().isocalendar()[1] + 2)
    rots = [-0.6, 0.5, 0.3, -0.4]
    press_html = ''.join(f'<a href="press.html" style="text-decoration:none;display:block"><div class="bulletin-card" style="transform:rotate({rots[i] if i<len(rots) else 0}deg)"><div class="bulletin-date">{p["date"]}</div><div class="bulletin-title">{p["title"]}</div><div class="bulletin-text">{p["text"]}</div></div></a>' for i, p in enumerate(presses))

    # CTA variants
    cta_lines = [
        'The next hearing is Thursday at 7 PM in the Community Room. Public comment is limited to three minutes per resident. Refreshments will be provided.',
        'A special session of the Kaiju Affairs Committee convenes Friday at 6 PM. Written comments may be submitted in advance.',
        'The Bureau will hold open hearings every Tuesday this month. Sign up for public comment at the front desk.',
        'Quarterly town hall: Saturday at 10 AM at the Municipal Annex. All residents are encouraged to attend.',
    ]
    cta = cta_lines[date.today().isocalendar()[1] % len(cta_lines)]

    body = f'''
<div style="padding:60px 44px;background:#ece3cd;">
  <div class="container" style="background:#f4efe0;border:2px solid #6b4f36;padding:48px 56px;box-shadow:6px 6px 0 rgba(107,79,54,0.15);">
    <div style="display:inline-block;padding:5px 14px;background:#b8943f;color:#2b2b23;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:22px;">URGENT &middot; Godzilla Has No Rights</div>
    <h1 style="font-size:44px;line-height:1.25;font-weight:700;color:#2f4d3a;margin:0 0 16px;">Godzilla can't speak for himself.<br>That's why we're here.</h1>
    <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0 0 12px;max-width:640px;">For 72 years, Godzilla has been slandered, shelled, and classified as a threat — without a single hearing, a single lawyer, or a single day in court. The Municipal Bureau of Kaiju Affairs is the only organization working to change that. We need your help.</p>
    <div style="display:flex;gap:14px;flex-wrap:wrap;">
      <a href="#support" class="btn-gold" style="text-decoration:none">Support Our Work</a>
      <a href="petition.html" class="btn-secondary" style="text-decoration:none">Sign the Petition</a>
    </div>
  </div>
</div>

<!-- PETITION BAR -->
<div class="page-section" id="petition">
  <div class="container">
    <div class="petition-bar">
      <div style="font-size:16px;font-weight:700;color:#2f4d3a;">Petition to Reclassify Godzilla as a Protected Ecological Asset</div>
      <div style="font-size:12px;color:#6b4f36;margin:4px 0 8px;">{d['petition']['description']}</div>
      <div class="progress"><div class="progress-fill live-fill" style="width:{pct}%"></div></div>
      <div class="stats"><span><strong class="live-count">{n:,}</strong> signatures</span><span>Goal: <strong>{d['petition']['goal']:,}</strong></span><span>Deadline: <strong>Dec 31, 2026</strong></span></div>
      <div style="margin-top:16px"><a href="petition.html" class="btn-gold" style="text-decoration:none">Sign the Petition</a></div>
    </div>
  </div>
</div>

<!-- RECENT SIGNERS -->
<div class="page-section">
  <div class="container">
    <div class="section-title"><h2>Recent Signers</h2><span class="section-sub">(Live feed &middot; updated in real-time)</span></div>
    <div style="background:#f4efe0;border:2px solid #6b4f36;padding:20px 24px;">
      <div id="recentSigners">
        <div style="padding:12px 0;text-align:center;font-size:13px;color:#6b4f36;">Loading recent signers...</div>
      </div>
      <div style="text-align:center;margin-top:16px"><a href="petition.html" class="btn-secondary" style="text-decoration:none;font-size:12px;">Join <span class="live-count">{n:,}</span> others &rarr;</a></div>
    </div>
  </div>
</div>

<!-- METRICS -->
<div class="page-section">
  <div class="container" style="border:2px solid #6b4f36;">
    <div style="background:#2f4d3a;color:#f4efe0;font-size:12px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:10px 18px;">Bureau Statistics &middot; Fiscal Year 2026</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);background:#f4efe0;">
      <div style="padding:24px 16px;text-align:center;border-right:1px solid #d8cba8;"><div style="font-size:32px;font-weight:700;color:#2f4d3a;">{cities}</div><div style="font-size:11px;color:#6b4f36;margin-top:6px;">Cities Protected</div></div>
      <div style="padding:24px 16px;text-align:center;border-right:1px solid #d8cba8;"><div style="font-size:32px;font-weight:700;color:#2f4d3a;">{threats}</div><div style="font-size:11px;color:#6b4f36;margin-top:6px;">Threats Neutralized</div></div>
      <div style="padding:24px 16px;text-align:center;border-right:1px solid #d8cba8;"><div style="font-size:32px;font-weight:700;color:#2f4d3a;">0</div><div style="font-size:11px;color:#6b4f36;margin-top:6px;">Unprovoked Attacks</div></div>
      <div style="padding:24px 16px;text-align:center;"><div style="font-size:32px;font-weight:700;color:#2f4d3a;">{d['metrics']['years_of_service']}</div><div style="font-size:11px;color:#6b4f36;margin-top:6px;">Years of Service</div></div>
    </div>
  </div>
</div>

<!-- MYTHS -->
<div class="page-section">
  <div class="container">
    <div class="section-title"><h2>Myths &amp; Facts</h2><span class="section-sub">(Fact Sheet 3-B)</span></div>
    <div class="data-table">
      <div class="data-table-header"><div>Common Misconception</div><div>Bureau Finding</div></div>
      <div class="data-table-body">
{''.join(f'<div>{m["myth"]}</div><div>{m["fact"]}</div>' for m in d['myths'])}
      </div>
    </div>
  </div>
</div>

<!-- INCIDENTS -->
<div class="page-section">
  <div class="container">
    <div class="section-title"><h2>Incident Tracker</h2><span class="section-sub">(5 of {len(d["incidents"])} cases shown)</span></div>
    <div class="card-grid">{incs_html}</div>
    <div style="text-align:center;margin-top:20px"><a href="incidents.html" class="btn-secondary" style="text-decoration:none">View All {len(d['incidents'])} Case Files</a></div>
  </div>
</div>

<!-- TESTIMONIALS -->
<div class="page-section">
  <div class="container">
    <div class="section-title"><h2>Voices of Reason</h2><span class="section-sub">(Public Comment Cards)</span></div>
    <div class="testimonial-grid">{tests_html}</div>
  </div>
</div>

<!-- PRESS -->
<div class="page-section">
  <div class="container">
    <div class="section-title"><h2>Press Room</h2><span class="section-sub">(Bulletin board)</span></div>
    <div class="bulletin-board">{press_html}</div>
    <div style="text-align:center;margin-top:20px"><a href="press.html" class="btn-secondary" style="text-decoration:none">View All Press Releases</a></div>
  </div>
</div>

<!-- SUPPORT / DONATION -->
<div class="page-section" id="support">
  <div class="container">
    <div class="section-title"><h2>Support Our Work</h2><span class="section-sub">(Your contribution goes directly to advocacy)</span></div>
    <p style="font-size:14px;color:#3a3a2e;line-height:1.7;margin-bottom:24px;">Godzilla has been misrepresented for 72 years. Every day without legal standing is a day he can be legally attacked. Navies train on him. Governments budget for his destruction. He has no lawyer, no voice, no rights. <strong>We are the only organization fighting for him.</strong> Every dollar goes directly to incident reclassification, legal advocacy, and public education.</p>
    <div class="tier-grid">{tiers}</div>
    <div style="margin-top:24px">
      <div style="font-size:14px;font-weight:700;color:#2f4d3a;margin-bottom:12px;">What your donation does:</div>
      <div class="impact-list">{impacts}</div>
    </div>
  </div>
</div>

<!-- CTA -->
<div class="page-section">
  <div class="container">
    <div class="cta-box">
      <div class="cta-label">Notice of Public Hearing</div>
      <h2 class="cta-title">The next hearing is Thursday at 7 PM.<br>Be there or file a comment.</h2>
      <p class="cta-text">{cta}</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
        <a href="about.html" class="btn-gold" style="text-decoration:none">Learn About Our Mission</a>
        <a href="contact.html" class="btn-secondary" style="text-decoration:none;color:#f4efe0;border-color:#f4efe0;background:transparent">Contact the Bureau</a>
      </div>
    </div>
  </div>
</div>'''
    return page('Home — Save Godzilla', body, 'index.html')

def generate_about(d):
    team = ''.join(f'<div class="team-card"><div class="team-name">{t["name"]}</div><div class="team-title">{t["title"]}</div><div class="team-bio">{t["bio"]}</div></div>' for t in d['team'])
    timeline = ''.join(f'<div class="timeline-item"><div class="timeline-year">{t["year"]}</div><div class="timeline-text">{t["event"]}</div></div>' for t in d['timeline'])

    body = f'''
<div class="page-section" style="padding-top:64px">
  <div class="container">
    <div style="background:#f4efe0;border:2px solid #6b4f36;padding:40px 48px;box-shadow:6px 6px 0 rgba(107,79,54,0.15);margin-bottom:40px;">
      <div style="display:inline-block;padding:5px 14px;background:#b8943f;color:#2b2b23;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:22px;">About the Bureau &middot; Form GZ-2A</div>
      <h1 style="font-size:36px;font-weight:700;color:#2f4d3a;margin:0 0 20px;">Our Mission</h1>
      <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0 0 16px;">The Municipal Bureau of Kaiju Affairs is a public good organization dedicated to the evidence-based reconsideration of Godzilla's legal and social standing. We believe that a being who has repeatedly saved our planet from existential threats deserves due process, not depth charges.</p>
      <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0 0 16px;">Founded in 1954 in the wake of the Tokyo Bay incident, the Bureau has spent seven decades documenting incidents, reclassifying encounters, and advocating for a more accurate understanding of Godzilla's role as a sovereign ecological force. We are the only organization of our kind.</p>
      <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0;">Our work is funded entirely by individual supporters. We accept no government or military funding.</p>
    </div>

    <div id="team" class="section-title"><h2>Our Team</h2><span class="section-sub">(Bureau Staff)</span></div>
    <div class="card-grid" style="grid-template-columns:repeat(2,1fr)">{team}</div>

    <div style="margin-top:48px">
      <div class="section-title"><h2>Our History</h2><span class="section-sub">(Organizational Timeline)</span></div>
      <div class="timeline">{timeline}</div>
    </div>
  </div>
</div>'''
    return page('About — Save Godzilla', body, 'about.html')

def generate_incidents(d):
    incs = ''.join(f'<div class="card"><div class="card-label"><span>CASE FILE {i["id"]}</span><span>RECLASSIFIED</span></div><div class="card-title">{i["title"]}</div><div class="card-text">{i["text"]}</div></div>' for i in d['incidents'])
    body = f'''
<div class="page-section" style="padding-top:64px">
  <div class="container">
    <div style="background:#f4efe0;border:2px solid #6b4f36;padding:40px 48px;box-shadow:6px 6px 0 rgba(107,79,54,0.15);margin-bottom:40px;">
      <div style="display:inline-block;padding:5px 14px;background:#b8943f;color:#2b2b23;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:22px;">Incident Tracker &middot; Form GZ-4</div>
      <h1 style="font-size:36px;font-weight:700;color:#2f4d3a;margin:0 0 20px;">Full Incident Tracker</h1>
      <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0;">All {len(d['incidents'])} case files that have been formally reviewed and reclassified by the Bureau. Each incident was originally reported as an unprovoked attack. The Bureau disagrees.</p>
    </div>
    <div class="card-grid" style="grid-template-columns:repeat(2,1fr)">{incs}</div>
  </div>
</div>'''
    return page('Incidents — Save Godzilla', body, 'incidents.html')

def generate_press(d):
    rots = [-0.6, 0.5, 0.3, -0.4, 0.2, -0.3, 0.6, -0.5]
    items = ''.join(f'<div class="bulletin-card" style="transform:rotate({rots[i] if i<len(rots) else 0}deg)"><div class="bulletin-date">{p["date"]}</div><div class="bulletin-title">{p["title"]}</div><div class="bulletin-text">{p["text"]}</div></div>' for i, p in enumerate(d['press_releases']))
    body = f'''
<div class="page-section" style="padding-top:64px">
  <div class="container">
    <div style="background:#f4efe0;border:2px solid #6b4f36;padding:40px 48px;box-shadow:6px 6px 0 rgba(107,79,54,0.15);margin-bottom:40px;">
      <div style="display:inline-block;padding:5px 14px;background:#b8943f;color:#2b2b23;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:22px;">Press Room &middot; Form GZ-5</div>
      <h1 style="font-size:36px;font-weight:700;color:#2f4d3a;margin:0 0 20px;">Press Releases</h1>
      <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0;">Official statements, research findings, and announcements from the Municipal Bureau of Kaiju Affairs.</p>
    </div>
    <div class="bulletin-board" style="grid-template-columns:repeat(2,1fr)">{items}</div>
  </div>
</div>'''
    return page('Press — Save Godzilla', body, 'press.html')

def generate_contact(d):
    o = d['office']
    body = f'''
<div class="page-section" style="padding-top:64px">
  <div class="container">
    <div style="background:#f4efe0;border:2px solid #6b4f36;padding:40px 48px;box-shadow:6px 6px 0 rgba(107,79,54,0.15);margin-bottom:40px;">
      <div style="display:inline-block;padding:5px 14px;background:#b8943f;color:#2b2b23;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:22px;">Contact &middot; Form GZ-6</div>
      <h1 style="font-size:36px;font-weight:700;color:#2f4d3a;margin:0 0 20px;">Contact the Bureau</h1>
      <p style="font-size:15px;line-height:1.75;color:#3a3a2e;margin:0 0 24px;">Public comments, hearing inquiries, and media requests are welcome. Written correspondence is preferred.</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
        <div>
          <div style="background:#f4efe0;border:2px solid #6b4f36;padding:24px;">
            <div style="font-weight:700;font-size:14px;color:#2f4d3a;margin-bottom:12px;">Office</div>
            <div style="font-size:13px;line-height:1.7;color:#3a3a2e;">
              {o['address']}<br>
              {o['city']}<br><br>
              <strong>Phone:</strong> {o['phone']}<br>
              <strong>Email:</strong> {o['email']}<br><br>
              <strong>Hours:</strong> {o['hours']}<br>
              <strong>Hearing Room:</strong> {o['hearing_room']}
            </div>
          </div>
        </div>
        <div>
          <div style="background:#f4efe0;border:2px solid #6b4f36;padding:24px;">
            <div style="font-weight:700;font-size:14px;color:#2f4d3a;margin-bottom:12px;">Submit a Public Comment</div>
            <div style="font-size:13px;color:#3a3a2e;line-height:1.7;">
              <p>Public comments may be submitted in person at any hearing, by mail to our office address, or via email. Comments are entered into the public record and reviewed at the next scheduled hearing.</p>
              <p>Please include your full name and municipality of residence. Anonymous comments are accepted but given reduced weight in committee deliberations.</p>
            </div>
          </div>
        </div>
      </div>
      <div style="margin-top:24px;background:#f4efe0;border:2px solid #6b4f36;padding:24px;">
        <div style="font-weight:700;font-size:14px;color:#2f4d3a;margin-bottom:8px;">Media Inquiries</div>
        <div style="font-size:13px;color:#3a3a2e;line-height:1.7;">Members of the press should direct inquiries to Ambassador Vivienne Graham at {o['email']} with the subject line "MEDIA REQUEST." Please allow 2-3 business days for a response.</div>
      </div>
    </div>
  </div>
</div>'''
    return page('Contact — Save Godzilla', body, 'contact.html')

def main():
    d = load()
    pages = [
        ('index.html', generate_index(d)),
        ('about.html', generate_about(d)),
        ('incidents.html', generate_incidents(d)),
        ('press.html', generate_press(d)),
        ('contact.html', generate_contact(d)),
    ]
    for name, html in pages:
        path = os.path.join(OUT_DIR, name)
        with open(path, 'w') as f:
            f.write(html)
        print(f'  {name} — {len(html):,} bytes')

if __name__ == '__main__':
    print('Generating savegodzilla.org...')
    main()
    print('Done.')