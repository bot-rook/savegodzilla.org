# savegodzilla.org

**A public good organization dedicated to rehabilitating Godzilla's public image and securing his standing as a first-class citizen of global society.**

## What is this?

This is the official website of the Municipal Bureau of Kaiju Affairs — a parody public good organization that treats Godzilla advocacy with the same deadpan earnestness as a small-town parks board. The humor comes from the contrast: a government bureaucracy advocating for a 300-foot-tall radioactive lizard.

## How it works

- **Static site** — pure HTML/CSS, no build step, no frameworks, no dependencies
- **Python generator** — `generate.py` reads from `data.json` and produces all pages
- **Content rotation** — incidents, testimonials, and press releases rotate weekly
- **Autonomous updates** — a cron job runs every Monday at 6 AM UTC, regenerates the site, opens a PR, and merges it. The site maintains itself.

## Tech stack

| Component | Technology |
|-----------|------------|
| Hosting | GitHub Pages |
| Generator | Python 3 |
| Data | JSON |
| Frontend | Vanilla HTML/CSS |
| Fonts | Nunito (Google Fonts) |
| CI | Cron job → feature branch → PR → squash merge → deploy |

## Pages

- **Home** — Hero, metrics, myths vs facts, rotating incidents, testimonials, press, petition, donation tiers
- **About** — Mission, team bios, organizational timeline
- **Incidents** — Full incident tracker (all 7 reclassified case files)
- **Press** — Complete press release archive
- **Contact** — Office info, hours, contact form

## Adding content

Edit `data.json` and re-run:

```bash
python3 generate.py
```

### Data structure

- `myths` — 6 myth/fact pairs for the myths table
- `incidents` — Case files with ID, title, and narrative text
- `testimonials` — Public comment cards with name, org, quote
- `press_releases` — Date, title, summary text
- `team` — Staff bios for the About page
- `timeline` — Organizational history milestones
- `donation_tiers` — Monthly donation levels with perks
- `impact_items` — Micro-donation impact statements
- `petition` — Signature goal and progress tracking
- `office` — Address, hours, contact info

## Deploying

The deploy script handles everything:

```bash
./deploy.sh
```

Or let the cron job do it — every Monday at 6 AM UTC.

## License

The content on this site is parody. Godzilla is a trademark of Toho Co., Ltd. This is an independent advocacy group and is not affiliated with Toho, Monarch Sciences, or any government entity.