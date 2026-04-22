# Remotion Motion Design with Claude Code

## Description
Turn Claude Code into a full motion design studio using Remotion — a React-based framework for creating videos programmatically. This skill enables Claude Code to scaffold, generate, and iteratively refine motion graphics, animated videos, and visual content entirely from code, without traditional video editing software.

## When to Use
- User asks to create a motion graphic, animated video, or visual content from code
- User wants to generate video intros, explainers, logo animations, social media clips, or promotional videos
- User mentions "Remotion", "programmatic video", "code-based video", or "motion design"
- User wants to iterate on video designs quickly by describing changes in natural language
- User needs to produce multiple video variants (different colors, text, branding) from a single template

## Instructions

### 1. Set Up Remotion in One Command

Initialize a new Remotion project directly from the terminal:

```bash
npx create-video@latest my-motion-project
```

This scaffolds a full Remotion project with TypeScript, React, and a dev server for real-time preview. Alternatively, to add Remotion to an existing project:

```bash
npm init video
# or
npm i remotion @remotion/cli @remotion/player
```

### 2. Understand the Remotion Project Structure

A Remotion project has these key files:

- `src/Root.tsx` — Registers all compositions (video scenes)
- `src/Composition.tsx` — Defines video dimensions, FPS, and duration
- `src/MyComposition.tsx` — The actual video content (React components)
- `remotion.config.ts` — Build and rendering configuration

### 3. Generate Motion Design from Code

Create video compositions as React components. Every animation is a function of the current frame:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

export const MyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  const scale = spring({ frame, fps, config: { damping: 200 } });

  return (
    <div style={{ opacity, transform: `scale(${scale})`, 
                  display: "flex", justifyContent: "center", alignItems: "center",
                  height: "100%", backgroundColor: "#0f0f0f" }}>
      <h1 style={{ color: "white", fontSize: 80 }}>Hello Motion</h1>
    </div>
  );
};
```

Key Remotion APIs to use:
- `useCurrentFrame()` — Get the current frame number for animation
- `interpolate()` — Map frame ranges to value ranges (opacity, position, scale)
- `spring()` — Physics-based easing for natural motion
- `<Sequence>` — Time-shift sections of the video
- `<AbsoluteFill>` — Full-screen positioning layer
- `<Img>`, `<Video>`, `<Audio>` — Media components with frame-accurate timing

### 4. Preview in Real Time

Start the Remotion dev server to see changes instantly:

```bash
npx remotion studio
```

This opens a browser-based preview with a timeline, frame scrubbing, and hot reload. Every code change is reflected immediately.

### 5. Iterate by Describing Changes

This is where Claude Code shines. After the initial composition is set up, the user can request changes in plain English and Claude modifies the code:

- **"Change the color to blue"** → Update `backgroundColor` or `color` values
- **"Make the text fly in from the left"** → Add `interpolate()` on `translateX`
- **"Add a second scene with a logo"** → Create a new component, wrap in `<Sequence>`
- **"Speed up the intro"** → Adjust frame ranges in `interpolate()` calls
- **"Add a bounce effect"** → Use `spring()` with custom `damping` and `mass`
- **"Export at 4K"** → Change composition width/height to 3840x2160

### 6. Render the Final Video

Export the finished video to MP4:

```bash
npx remotion render src/index.ts MyComposition out/video.mp4
```

Rendering options:
- `--codec=h264` (default), `h265`, `vp8`, `vp9`, `gif`
- `--image-format=jpeg` or `png`
- `--quality=80` (0-100 for lossy codecs)
- `--scale=2` (render at 2x resolution)
- Render specific frame ranges with `--frames=0-60`

### 7. Common Motion Design Patterns

**Staggered text reveal:**
```tsx
{words.map((word, i) => (
  <span key={i} style={{
    opacity: interpolate(frame, [i * 5, i * 5 + 10], [0, 1], { extrapolateRight: "clamp" })
  }}>{word} </span>
))}
```

**Slide transitions between scenes:**
```tsx
<Sequence from={0} durationInFrames={90}><SceneOne /></Sequence>
<Sequence from={90} durationInFrames={90}><SceneTwo /></Sequence>
```

**Data-driven videos (batch rendering):**
Use Remotion's parametrized compositions to generate variants — different names, colors, or content from a JSON/CSV data source.

### 8. Tips for Best Results

- Start simple: get one scene working, then add complexity
- Use `spring()` over linear `interpolate()` for natural-feeling motion
- Keep compositions short (15-60 seconds) for social media
- Use `<AbsoluteFill>` for layering elements
- Test at the target resolution early — layout can shift at different sizes
- Use Remotion's `<Series>` component for sequential scenes with automatic timing
- Install `@remotion/tailwind` for utility-class styling in video components

## Source
Extracted from TikTok by @mr_pynk (Mr. Pynk) — motion design creator sharing AI + code workflows. Original video: https://vm.tiktok.com/ZNRqtGBcH/
