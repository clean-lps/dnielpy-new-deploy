# Blossom Luxe Studio — Decorative Web Assets

Assets created for background decoration and brand atmosphere, inspired by the client's actual logo/interior photos.

Hero:
curtain-wave-white-gold.svg + soft-glow-orbs.png

Secciones internas:
lotus-outline-gold.svg en opacidad baja

Página de lashes:
eyelash-arc-black-gold.svg

Divisores:
luxe-line-divider-gold.svg

Fondos suaves:
lotus-pattern-tile.svg con opacity 0.06–0.12

## Recommended use

- Use `.svg` files for web backgrounds, dividers, masks and scalable decorative elements.
- Use `.png` files when the code agent needs a quick transparent raster image.
- Keep opacity low: 0.06–0.18 for background patterns, 0.35–0.75 for dividers.
- Do not use these as the official logo; they are decorative brand elements.

## Included assets

1. `lotus-outline-gold` — lotus from the logo style; use behind hero or section headings.
2. `eyelash-arc-black-gold` — lash curve; use in lashes page or services area.
3. `curtain-wave-white-gold` — curtain/veil wave; use for the approved "Abrir la Cortina del Ritual" concept.
4. `blossom-sparkles-gold` — small luxe sparks/dots; use as subtle background detail.
5. `luxe-line-divider-gold` — elegant section divider.
6. `lotus-pattern-tile` — repeatable background pattern.
7. `soft-glow-orbs` — soft decorative glow for hero backgrounds.

## CSS example

```css
.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("/assets/decor/curtain-wave-white-gold.svg");
  background-size: cover;
  background-position: center;
  opacity: 0.22;
  pointer-events: none;
}

.section-lotus::after {
  content: "";
  position: absolute;
  width: 420px;
  height: 420px;
  right: -120px;
  top: 10%;
  background: url("/assets/decor/lotus-outline-gold.svg") center / contain no-repeat;
  opacity: 0.10;
  pointer-events: none;
}
```

## Brand colors used

- Gold: #A48865
- Luxe black: #050504
- Warm ink: #3F352B
- Blossom red accent: #470D11
