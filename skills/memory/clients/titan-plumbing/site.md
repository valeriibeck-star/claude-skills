# Titan Plumbing — Site Build
**Date:** 2026-03-29
**Category:** design
**Related:** memory/clients/titan-plumbing/profile.md

## Build Details
- **Tech:** Static HTML/CSS/JS — no framework
- **Fonts:** Inter (body) + Plus Jakarta Sans (headings)
- **Colors:** Navy #1a2744 + Gold #d4a853 + White
- **Hosting:** GitHub Pages (valeriibeck-star.github.io/titan-plumbing-demo)
- **Repo:** github.com/valeriibeck-star/titan-plumbing-demo
- **Build time:** ~3 min V1, ~5 min V2 fixes, ~3 min V3 fixes
- **API cost:** ~$15 total across 3 versions + 2 audits

## Versions
- **V1:** Claude Code built from BRIEF.md. Score: 16/24
- **V2:** Fixed form (Formspree), added photos, sticky mobile CTA, contrast fixes. Score: 17/24
- **V3:** WCAG contrast fixed, photo cohesion, favicon, CTA consistency, skip link. Not re-scored but estimated 19-20/24.

## GSD UI Audit Scores (V2)
| Pillar | Score |
|--------|-------|
| Copywriting | 3.0/4 |
| Visuals | 2.5/4 |
| Color | 2.5/4 |
| Typography | 3.0/4 |
| Spacing | 3.0/4 |
| Experience | 3.0/4 |

## What Worked
- Navy + gold palette reads as "trustworthy and strong" for plumbing
- Real Google reviews quoted on site builds credibility fast
- Plus Jakarta Sans as display font killed the template feel
- Animated counters on stats (40+, 24/7) add life
- Emergency service card with gold border stands out

## What Didn't Work (V1 issues)
- Formspree placeholder threw away leads — critical miss
- Stock photos from different shoots looked incoherent
- Gold-on-white failed WCAG contrast
- No favicon = looks unfinished
- "Schedule Online" vs "Book Now" inconsistency

## Takeaway
Navy + gold is a strong palette for trades/plumbing. Always wire forms to a real endpoint before deploying. Stock photo cohesion matters more than individual photo quality. Two fonts minimum to avoid template feel.
