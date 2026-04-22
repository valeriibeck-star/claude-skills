# AI-to-Designer UI Polish

## Description
A skill for transforming generic, AI-looking UI output into polished, professional-grade design. Combines three proven approaches from the Claude Code design community: motion/animation integration, design-vocabulary commands, and taste-driven critique. Eliminates the most common vibe-coding anti-patterns — default Inter font everywhere, lorem-ipsum-style copy, flat layouts with no rhythm, and zero motion.

## When to Use
- After generating any UI component, page, or layout — run a polish pass before shipping
- When a user says "make this look better", "this looks like AI made it", "polish this", or "add animations"
- When reviewing any frontend code for design quality
- Before any demo, deploy, or PR that includes UI changes
- When the output uses Inter font with no typographic variation, has generic placeholder copy, lacks spacing rhythm, or has no transitions/animations

## Instructions

### Step 1: Audit for AI-Looking Anti-Patterns
Before changing anything, scan the current UI for these common signs of unpolished AI output:

**Typography red flags:**
- Inter font used everywhere with no variation (the #1 tell of AI-generated UI)
- No font size hierarchy — headings and body text are too similar in scale
- Missing letter-spacing adjustments (too loose on headings, too tight on body)
- No font weight contrast between elements

**Layout red flags:**
- Equal spacing everywhere — no vertical rhythm or intentional density variation
- Components floating with no visual grouping or proximity logic
- Content not aligned to any consistent grid or baseline
- No whitespace used as a design element

**Content red flags:**
- Generic copy like "Welcome to Our Platform" or "Lorem ipsum"
- Button labels that say "Submit" or "Click Here" instead of action-specific verbs
- No microcopy — missing helper text, empty states, or contextual hints

**Motion red flags:**
- No hover states, transitions, or feedback animations
- Page loads with everything appearing at once (no stagger or entrance motion)
- Interactive elements feel dead — no visual response to user actions

### Step 2: Apply Design-Vocabulary Commands
Use these 20 design-intent commands to fix issues. Each maps to specific CSS/code changes:

1. `/polish` — Run a full cleanup pass: fix spacing, typography, color contrast, and alignment in one sweep
2. `/rhythm` — Establish vertical rhythm using a consistent spacing scale (e.g., 4px base: 4, 8, 12, 16, 24, 32, 48, 64)
3. `/hierarchy` — Create clear visual hierarchy: make headings significantly larger, use weight and color to distinguish levels
4. `/contrast` — Improve color contrast ratios for accessibility (minimum 4.5:1 for body text, 3:1 for large text)
5. `/density` — Adjust information density: tighten related items, add breathing room between sections
6. `/type-scale` — Apply a modular type scale (e.g., 1.25 ratio: 14, 16, 20, 25, 31, 39px)
7. `/font-pair` — Replace single-font usage with a complementary pair (e.g., display + body font)
8. `/letter-space` — Tighten letter-spacing on large headings (-0.02em to -0.04em), loosen on small caps (+0.05em to +0.1em)
9. `/color-system` — Build a cohesive color palette: primary, secondary, neutral scale, semantic colors (success, warning, error)
10. `/surface` — Add depth with subtle background variations, card surfaces, and border treatments
11. `/shadow` — Apply layered, realistic shadows instead of flat borders (use multiple box-shadows at different offsets)
12. `/radius` — Make border-radius consistent and intentional (pick one scale: 4/8/12/16px and stick to it)
13. `/grid` — Align content to a responsive grid with consistent gutters
14. `/whitespace` — Use whitespace as a design element: generous padding on hero sections, tighter on data-dense areas
15. `/animate` — Add entrance animations with staggered delays (fade-up, slide-in, scale)
16. `/transition` — Add micro-interactions: hover states (scale 1.02, shadow lift), focus rings, active states
17. `/motion` — Add real motion and animations — spring-based easing, page transitions, layout animations using Framer Motion or CSS
18. `/icon` — Ensure icons are consistent in style (outline vs. filled), size, and stroke width
19. `/responsive` — Check and fix breakpoints: stack on mobile, adjust font sizes, touch-friendly tap targets (min 44px)
20. `/copy` — Replace generic placeholder text with realistic, specific microcopy that matches the product's actual purpose

### Step 3: Add Real Motion and Animation
Motion is what separates polished UI from flat AI output. Apply these patterns:

**Entrance animations (when elements first appear):**
```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
.element { animation: fadeUp 0.5s ease-out both; }
.element:nth-child(2) { animation-delay: 0.1s; }
.element:nth-child(3) { animation-delay: 0.2s; }
```

**Hover micro-interactions:**
```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
.button {
  transition: all 0.15s ease;
}
.button:hover {
  transform: scale(1.02);
}
.button:active {
  transform: scale(0.98);
}
```

**For React projects, use Framer Motion:**
```jsx
import { motion } from "framer-motion";

// Staggered list entrance
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }}
>
```

**Spring-based easing** (feels more natural than linear/ease):
```jsx
transition={{ type: "spring", stiffness: 300, damping: 30 }}
```

### Step 4: Train Your Eye — What Good Design Looks Like
Before finalizing, check against these taste criteria:

**Does it pass the squint test?** Squint at the screen — can you still see the visual hierarchy? The most important element should be obvious even blurred.

**Does it have intentional contrast?** Good design has loud parts and quiet parts. Not everything should demand attention equally.

**Does it feel cohesive?** Every color, font size, spacing value, and radius should come from a defined system — not arbitrary one-off values.

**Does it have personality?** The best UIs have one or two distinctive touches — a custom illustration, an unexpected color accent, a clever animation — that make it feel human-made, not template-generated.

**Would a designer approve this?** If the answer is "it's fine" rather than "this is good," keep iterating.

### Step 5: Final Polish Checklist
Run through this before shipping:

- [ ] No default Inter-only typography — at least vary weights and sizes meaningfully
- [ ] Spacing follows a consistent scale (not random pixel values)
- [ ] Color palette is cohesive (3-5 colors max, with intentional neutral scale)
- [ ] Interactive elements all have hover/focus/active states
- [ ] At least one entrance animation or page transition exists
- [ ] Text content is realistic and specific (no lorem ipsum, no "Welcome to Our Platform")
- [ ] Shadows and borders are subtle and layered (not 1px solid gray everywhere)
- [ ] Layout works at mobile, tablet, and desktop breakpoints
- [ ] Contrast ratios meet WCAG AA minimum (4.5:1 body, 3:1 large text)
- [ ] The page has visual rhythm — varying section heights and density

## Credits
Techniques synthesized from three Claude Code design skills shared by [@yury.ai on TikTok](https://www.tiktok.com/@yury.ai):
- **Emil Kowalski's Animation Skill** — real motion and animations via one command
- **Impeccable** by pjaakaus — 20 design-vocabulary commands including `/polish` (install: `npx skills add pjaakaus/impeccable`)
- **Taste Skill** — trains Claude on what good design actually looks like
