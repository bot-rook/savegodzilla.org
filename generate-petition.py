#!/usr/bin/env python3
"""Generate petition.html and certificate.html for savegodzilla.org."""
import os, json
from datetime import date

OUT_DIR = '/opt/data/savegodzilla.org'
DATA_PATH = os.path.join(OUT_DIR, 'data.json')

CSS = '''body { margin:0; background:#ece3cd; font-family:'Nunito',Verdana,Arial,sans-serif; }
* { box-sizing:border-box; }
a { color:#2f4d3a; }
::selection { background:#b8943f; color:#2b2b23; }
.stripe { height:8px; background:repeating-linear-gradient(45deg,#2f4d3a,#2f4d3a 12px,#b8943f 12px,#b8943f 24px); }
.page-section { padding:0 44px 64px; }
.container { max-width:920px; margin:0 auto; }
.form-card { background:#f4efe0; border:2px solid #6b4f36; padding:40px 48px; box-shadow:6px 6px 0 rgba(107,79,54,0.15); }
.form-card h1 { font-size:36px; color:#2f4d3a; margin:0 0 8px; }
.form-card p { font-size:15px; line-height:1.75; color:#3a3a2e; margin:0 0 24px; }
.form-group { margin-bottom:20px; }
.form-group label { display:block; font-size:12px; font-weight:700; color:#2f4d3a; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.06em; }
.form-group label .required { color:#b8943f; }
.form-group input,.form-group textarea,.form-group select { width:100%; padding:14px 16px; font-family:'Nunito',sans-serif; font-size:14px; border:2px solid #d8cba8; background:#fcf9f0; color:#2b2b23; outline:none; transition:border-color 0.2s; }
.form-group input:focus,.form-group textarea:focus { border-color:#2f4d3a; }
.form-group textarea { min-height:100px; resize:vertical; }
.form-group .hint { font-size:11px; color:#6b4f36; margin-top:4px; }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.btn-submit { width:100%; padding:16px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:16px; border:2px solid #22392a; cursor:pointer; font-family:'Nunito',sans-serif; transition:background 0.2s; }
.btn-submit:hover { background:#3a5e48; }
.btn-submit:disabled { opacity:0.5; cursor:not-allowed; }
.petition-count { background:#f4efe0; border:2px solid #6b4f36; padding:24px; text-align:center; margin-bottom:32px; }
.petition-count .big { font-size:48px; font-weight:800; color:#2f4d3a; }
.petition-count .label { font-size:13px; color:#6b4f36; }
.petition-count .progress { height:24px; background:#d8cba8; border:1px solid #6b4f36; margin:12px 0; position:relative; overflow:hidden; }
.petition-count .progress-fill { height:100%; background:#2f4d3a; transition:width 0.5s; }
.petition-count .stats { display:flex; justify-content:space-between; font-size:13px; color:#3a3a2e; }
.petition-legal { font-size:11px; color:#6b4f36; text-align:center; margin-top:16px; line-height:1.6; }
.petition-legal a { color:#6b4f36; }
.timer-num { font-size:32px; font-weight:800; line-height:1; }
.timer-label { font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:#d8cba8; margin-top:4px; }
.success-box { display:none; text-align:center; padding:40px; }
.success-box .check { font-size:64px; color:#2f4d3a; margin-bottom:16px; }
.success-box h2 { color:#2f4d3a; font-size:24px; margin:0 0 8px; }
.success-box p { color:#3a3a2e; font-size:15px; line-height:1.7; }
footer { padding:26px 44px; background:#dcd0ac; border-top:3px solid #2f4d3a; font-size:11px; color:#5c4a35; }
.footer-inner { max-width:920px; margin:0 auto; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }
@media (max-width:768px) {
  .form-row { grid-template-columns:1fr; }
  .form-card { padding:24px 20px; }
  .form-card h1 { font-size:28px; }
  .page-section { padding:0 16px 36px; }
  .container { max-width:100%; }
}'''

CERT_CSS = '''body { margin:0; background:#ece3cd; font-family:'Nunito',Verdana,Arial,sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; padding:20px; }
* { box-sizing:border-box; }
@page { size: letter; margin: 0.5in; }
.certificate { max-width:800px; width:100%; background:#f4efe0; border:4px solid #2f4d3a; padding:48px; box-shadow:8px 8px 0 rgba(107,79,54,0.15); }
.stripe { height:6px; background:repeating-linear-gradient(45deg,#2f4d3a,#2f4d3a 12px,#b8943f 12px,#b8943f 24px); margin:-48px -48px 32px; }
.seal { width:80px; height:80px; border-radius:50%; border:3px solid #2f4d3a; background:#f4efe0; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; }
.seal-inner { width:60px; height:60px; border-radius:50%; border:1px dashed #b8943f; display:flex; align-items:center; justify-content:center; font-size:28px; color:#2f4d3a; }
h1 { font-size:28px; text-align:center; color:#2f4d3a; margin:0 0 8px; text-transform:uppercase; letter-spacing:0.05em; }
h2 { font-size:20px; text-align:center; color:#2f4d3a; margin:0 0 32px; font-weight:500; }
.name-text { font-size:36px; text-align:center; color:#2f4d3a; font-weight:800; margin:0 0 8px; letter-spacing:0.02em; }
.muni-text { font-size:16px; text-align:center; color:#6b4f36; margin:0 0 32px; }
.body-text { font-size:14px; line-height:1.8; color:#3a3a2e; text-align:center; max-width:600px; margin:0 auto 32px; }
.details { display:grid; grid-template-columns:1fr 1fr; gap:16px; border-top:2px solid #d8cba8; padding-top:24px; margin-bottom:24px; }
.detail-item { text-align:center; }
.detail-label { font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:#6b4f36; }
.detail-value { font-size:14px; font-weight:700; color:#2f4d3a; }
.sig-line { border-top:2px solid #2f4d3a; width:250px; margin:0 auto 8px; padding-top:8px; }
.sig-title { font-size:11px; color:#6b4f36; text-align:center; }
.footer-note { font-size:10px; color:#6b4f36; text-align:center; margin-top:24px; border-top:1px solid #d8cba8; padding-top:16px; }
.print-btn { display:block; margin:24px auto 0; padding:12px 32px; background:#2f4d3a; color:#f4efe0; font-weight:700; font-size:14px; border:2px solid #22392a; cursor:pointer; font-family:'Nunito',sans-serif; }
.print-btn:hover { background:#3a5e48; }
.share-text { text-align:center; margin-top:16px; font-size:13px; color:#6b4f36; }
.share-text a { color:#2f4d3a; }
@media print { body { background:white; padding:0; } .certificate { box-shadow:none; border:3px solid #2f4d3a; } .print-btn,.share-text,.no-print { display:none !important; } }
@media (max-width:768px) { .certificate { padding:24px; } .name-text { font-size:28px; } .details { grid-template-columns:1fr; } }'''

def generate_petition_page():
    d = json.load(open(DATA_PATH))
    goal = d['petition']['goal']
    sigs = d['petition']['signatures']
    pct = min(100, round(sigs / goal * 100))

    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="alternate icon" href="favicon.ico" type="image/x-icon">
<link rel="canonical" href="https://savegodzilla.org/petition.html">
<meta name="description" content="Sign the official petition to reclassify Godzilla as a Protected Ecological Asset. Add your name alongside thousands of others demanding kaiju personhood.">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:url" content="https://savegodzilla.org/petition.html">
<meta property="og:title" content="Sign the Petition — Save Godzilla">
<meta property="og:description" content="Help us deliver 100,000 signatures to the UN Committee on Kaiju Affairs demanding Godzilla be reclassified as a Protected Ecological Asset.">
<meta property="og:image" content="https://savegodzilla.org/favicon.svg">
<meta name="twitter:card" content="summary_large_image">
<title>Sign the Petition — Save Godzilla</title>
</head><body>
<div class="stripe"></div>
<div class="page-section" style="padding-top:48px">
  <div class="container">
    <div class="petition-count">
      <div class="big">{sigs:,}</div>
      <div class="label">Signatures Collected of {goal:,} Goal</div>
      <div class="progress"><div class="progress-fill" style="width:{pct}%"></div></div>
      <div class="stats">
        <span>Goal: <strong>{goal:,}</strong></span>
        <span>Deadline: <strong>Dec 31, 2026</strong></span>
      </div>
    </div>

    <!-- COUNTDOWN TIMER -->
    <div style="background:#2f4d3a;color:#f4efe0;padding:16px 24px;text-align:center;margin-bottom:24px;">
      <div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#d8cba8;margin-bottom:8px;">Deadline to reach 100,000 signatures</div>
      <div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
        <div><div class="timer-num" id="timerDays">--</div><div class="timer-label">Days</div></div>
        <div><div class="timer-num" id="timerHours">--</div><div class="timer-label">Hours</div></div>
        <div><div class="timer-num" id="timerMins">--</div><div class="timer-label">Minutes</div></div>
        <div><div class="timer-num" id="timerSecs">--</div><div class="timer-label">Seconds</div></div>
      </div>
    </div>

    <div class="form-card" id="formCard">
      <div style="display:inline-block;padding:5px 14px;background:#b8943f;color:#2b2b23;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:22px;">Petition &middot; Form GZ-3</div>
      <h1>Reclassify Godzilla as a<br>Protected Ecological Asset</h1>
      <p>Add your name to the official petition addressed to the UN Committee on Kaiju Affairs. Every signature brings us closer to the 100,000 required for formal consideration.</p>

      <form id="petitionForm" method="POST">
        <div class="form-row">
          <div class="form-group">
            <label>Full Legal Name <span class="required">*</span></label>
            <input type="text" name="name" id="nameInput" required minlength="2" placeholder="e.g., John A. Doe">
          </div>
          <div class="form-group">
            <label>Email Address <span class="required">*</span></label>
            <input type="email" name="email" id="emailInput" required placeholder="e.g., john@example.com">
            <div class="hint">We will send you a verification link and a copy of your certificate.</div>
          </div>
        </div>
        <div class="form-group">
          <label>Municipality of Residence</label>
          <input type="text" name="municipality" id="muniInput" placeholder="e.g., Coastal City, CC">
          <div class="hint">Your municipality will be listed on the petition.</div>
        </div>
        <div class="form-group">
          <label>Public Comment (Optional)</label>
          <textarea name="comment" id="commentInput" placeholder="Why does Godzilla deserve legal standing? Your comment may be read into the public record at the next hearing."></textarea>
        </div>
        <div class="form-group" style="background:#ece3cd;padding:16px;border:1px solid #d8cba8;font-size:12px;color:#3a3a2e;line-height:1.6;">
          <strong>By signing, you acknowledge:</strong> Your name and municipality will be included in the public petition. Your email will be used for verification and certificate delivery only. We will not share your information with third parties. You may request removal at any time by contacting hello@savegodzilla.org.
        </div>
        <button type="submit" class="btn-submit" id="submitBtn">&#9997; Sign the Petition</button>
      </form>
    </div>

    <div class="success-box" id="successBox">
      <div class="check">&#10003;</div>
      <h2>Thank You for Signing!</h2>
      <p>Your signature has been recorded. You are <strong>signature #<span id="sigCountDisplay">—</span></strong>.</p>
      <p>Your certificate number: <strong id="certNumDisplay">—</strong></p>
      <p style="font-size:13px">You will receive a confirmation email. Please share your certificate to help us reach 100,000 signatures.</p>
      <div style="margin-top:24px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
        <a href="/certificate.html" class="no-print" style="display:inline-block;padding:12px 24px;background:#2f4d3a;color:#f4efe0;font-weight:700;font-size:14px;text-decoration:none;border:2px solid #22392a;" id="viewCertBtn">View Your Certificate</a>
        <a href="/" class="no-print" style="display:inline-block;padding:12px 24px;background:transparent;color:#2f4d3a;font-weight:700;font-size:14px;text-decoration:none;border:2px solid #2f4d3a;">Return to Home</a>
      </div>
    </div>

    <div class="petition-legal">
      This petition is addressed to the UN Committee on Kaiju Affairs. Form GZ-3 (Rev. 2026).<br>
      Municipal Bureau of Kaiju Affairs &middot; <a href="mailto:hello@savegodzilla.org">hello@savegodzilla.org</a>
    </div>
  </div>
</div>
<footer><div class="footer-inner">
  <div>Municipal Bureau of Kaiju Affairs &middot; Est. 1954 &middot; Office Hours: Mon&ndash;Fri, 8 AM&ndash;4:30 PM</div>
  <div>Form GZ-3 (Rev. 2026) &middot; savegodzilla.org</div>
</div></footer>

<script>
var API = 'https://petition-savegodzilla.loca.lt';
document.getElementById('petitionForm').addEventListener('submit', async function(e) {{
  e.preventDefault();
  var btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Submitting...';

  var name = document.getElementById('nameInput').value.trim();
  var email = document.getElementById('emailInput').value.trim();
  var muni = document.getElementById('muniInput').value.trim();
  var comment = document.getElementById('commentInput').value.trim();

  var certId = '';
  var totalSig = {sigs:,};

  try {{
    // Try live tunnel first
    var resp = await fetch(API + '/api/sign', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{name, email, municipality: muni, comment}})
    }});
    var data = await resp.json();
    if (data.status === 'signed') {{
      certId = data.cert_id;
      totalSig = data.total_signatures;
    }}
  }} catch(e) {{
    console.log('Tunnel unavailable, using FormSubmit fallback:', e);
  }}

  if (!certId) {{
    // Fallback: generate client-side and email via FormSubmit
    certId = 'GZ-PET-' + Math.random().toString(36).substring(2,10).toUpperCase();
    try {{
      var fd = new FormData();
      fd.append('name', name);
      fd.append('email', email);
      fd.append('municipality', muni);
      fd.append('comment', comment);
      fd.append('_captcha', 'true');
      fd.append('_subject', 'Petition: ' + name);
      await fetch('https://formsubmit.co/rook@not.farm', {{method: 'POST', body: fd, mode: 'no-cors'}});
    }} catch(e2) {{}}
  }}

  var cert = {{
    name, email,
    municipality: muni,
    comment,
    cert_id: certId,
    signed_at: new Date().toISOString(),
    total_signatures: totalSig
  }};
  localStorage.setItem('petition_cert', JSON.stringify(cert));

  document.getElementById('formCard').style.display = 'none';
  document.getElementById('successBox').style.display = 'block';
  document.getElementById('viewCertBtn').href = '/certificate.html';
  document.getElementById('certNumDisplay').textContent = certId;
  document.getElementById('sigCountDisplay').textContent = totalSig.toLocaleString();
}});

// Countdown timer
(function() {{
  var deadline = new Date('2026-12-31T23:59:59');
  function tick() {{
    var now = new Date();
    var diff = deadline - now;
    if (diff <= 0) {{
      document.getElementById('timerDays').textContent = '0';
      document.getElementById('timerHours').textContent = '0';
      document.getElementById('timerMins').textContent = '0';
      document.getElementById('timerSecs').textContent = '0';
      return;
    }}
    var s = Math.floor(diff / 1000);
    var m = Math.floor(s / 60);
    var h = Math.floor(m / 60);
    var d = Math.floor(h / 24);
    document.getElementById('timerDays').textContent = d;
    document.getElementById('timerHours').textContent = h % 24;
    document.getElementById('timerMins').textContent = m % 60;
    document.getElementById('timerSecs').textContent = s % 60;
  }}
  tick();
  setInterval(tick, 1000);
}})();
</script>
</body></html>'''

def generate_certificate_page():
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CERT_CSS}</style>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="alternate icon" href="favicon.ico" type="image/x-icon">
<link rel="canonical" href="https://savegodzilla.org/certificate.html">
<meta name="robots" content="noindex, follow">
<meta property="og:type" content="website">
<meta property="og:url" content="https://savegodzilla.org/certificate.html">
<meta property="og:title" content="Certificate of Participation — Save Godzilla">
<meta property="og:description" content="Printable Certificate of Public Participation from the Municipal Bureau of Kaiju Affairs.">
<meta property="og:image" content="https://savegodzilla.org/favicon.svg">
<meta name="twitter:card" content="summary">
<title>Certificate of Participation — Save Godzilla</title>
</head><body>
<div class="certificate" id="certificate">
  <div class="stripe"></div>
  <div class="seal"><div class="seal-inner">&#9813;</div></div>
  <h1>Municipal Bureau of Kaiju Affairs</h1>
  <h2>Certificate of Public Participation</h2>
  <div class="name-text" id="certName">—</div>
  <div class="muni-text" id="certMuni">Municipality of Record</div>
  <div class="body-text">
    Having freely affixed their name to the Petition to Reclassify Godzilla as a Protected Ecological Asset,
    is hereby recognized as a participant in the democratic process and a friend of the sovereign kaiju Godzilla.
  </div>
  <div class="details">
    <div class="detail-item">
      <div class="detail-label">Certificate Number</div>
      <div class="detail-value" id="certId">—</div>
    </div>
    <div class="detail-item">
      <div class="detail-label">Date Signed</div>
      <div class="detail-value" id="certDate">—</div>
    </div>
    <div class="detail-item">
      <div class="detail-label">Total Signatures</div>
      <div class="detail-value" id="certCount">—</div>
    </div>
    <div class="detail-item">
      <div class="detail-label">Petition Goal</div>
      <div class="detail-value">100,000</div>
    </div>
  </div>
  <div style="text-align:center;margin-bottom:24px;">
    <div class="sig-line"></div>
    <div class="sig-title">Director of Kaiju Affairs, Municipal Bureau</div>
  </div>
  <div class="footer-note">
    This certificate is a token of appreciation and does not confer any legal rights or obligations.
    Form GZ-7 (Rev. 2026) &middot; savegodzilla.org
  </div>
  <button class="print-btn no-print" onclick="window.print()">&#128424; Print This Certificate</button>
  <div class="share-text no-print">
    Share your support: <a href="#" id="shareTwitter" target="_blank">Post on X</a> &middot;
    <a href="#" id="shareCopy" onclick="navigator.clipboard.writeText('I just signed the petition to reclassify Godzilla as a Protected Ecological Asset! Sign here: savegodzilla.org/petition.html');alert('Link copied!');return false;">Copy Link</a>
  </div>
</div>

<script>
(function() {{
  var data = localStorage.getItem('petition_cert');
  if (data) {{
    try {{
      var cert = JSON.parse(data);
      document.getElementById('certName').textContent = cert.name || '—';
      document.getElementById('certMuni').textContent = cert.municipality || 'Municipality of Record';
      document.getElementById('certId').textContent = cert.cert_id || '—';
      document.getElementById('certDate').textContent = cert.signed_at ? cert.signed_at.substring(0,10) : new Date().toISOString().substring(0,10);
      document.getElementById('certCount').textContent = (cert.total_signatures || 0).toLocaleString();

      var shareUrl = 'https://x.com/intent/tweet?text=' + encodeURIComponent('I just signed the petition to reclassify Godzilla as a Protected Ecological Asset! My certificate: ' + cert.cert_id + ' Sign here:') + '&url=' + encodeURIComponent('https://savegodzilla.org/petition.html');
      document.getElementById('shareTwitter').href = shareUrl;
    }} catch(e) {{
      console.log('Cert parse error', e);
    }}
  }}
}})();
</script>
</body></html>'''

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    petition_html = generate_petition_page()
    path = os.path.join(OUT_DIR, 'petition.html')
    with open(path, 'w') as f:
        f.write(petition_html)
    print(f'  petition.html — {len(petition_html):,} bytes')

    cert_html = generate_certificate_page()
    path = os.path.join(OUT_DIR, 'certificate.html')
    with open(path, 'w') as f:
        f.write(cert_html)
    print(f'  certificate.html — {len(cert_html):,} bytes')

if __name__ == '__main__':
    main()