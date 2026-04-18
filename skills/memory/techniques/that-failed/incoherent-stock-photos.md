# Incoherent Stock Photos Tank Visual Scores
**Date:** 2026-03-29
**Category:** technique
**Related:** memory/clients/titan-plumbing/site.md

## What
V2 used 3 Unsplash photos with different color temperatures: warm bathroom, orange copper pipes, cool blue renovation. Plus a generic "construction workers" team photo that wasn't even plumbers.

## Result
Visuals scored 2.5/4 across both V1 and V2 audits. The GSD auditor called the photos "visually incoherent" and said "stock photo selection quality is what separates a $5K site from a $10K site."

## Fix Applied (V3)
- Replaced all 3 with warm-toned plumbing images
- Added CSS filter: `sepia(0.05) saturate(0.95)` to unify color temperature
- Swapped generic construction workers for actual plumbing work photo

## Takeaway
When using stock photos: pick images with matching color temperature and lighting. Apply a subtle CSS filter to unify them visually. Never use a photo where the subject doesn't match the business (construction workers ≠ plumbers).
