# 🍺 Beer Value Calculator

A simple, self-contained web app for comparing the value of bottled and canned
beers — right down to **pence per millilitre**. Add a few beers, and it ranks
them cheapest-to-priciest and highlights the best value.

## Features

- **Pence-per-ml comparison** to three decimal places
- **Value display toggle** — switch between *pence / ml*, *pence / 100 ml*, or
  *price / pint (568 ml)*
- **Multipack support** — enter a pack quantity (e.g. 4 × 440 ml) and it works
  out the total
- **Optional ABV %** — adds a *pence-per-unit* figure (UK alcohol units) so you
  can factor in strength, not just volume
- **"+X% vs best"** to see how much more each option costs than the winner
- **Saves locally** — your list and chosen units are remembered in your browser
  (nothing is uploaded anywhere)
- **Installable** — "Add to Home Screen" on iPad/iPhone for an app-like,
  full-screen experience with a custom icon

## How to use

1. Open the app (see *Hosting* below, or just open `index.html` in any browser).
2. Enter a beer's name, container, price, and volume — add a pack quantity for
   multipacks, and ABV if you want the per-unit figure.
3. Hit **Add beer** and repeat for each option.
4. The table ranks them by value; the **BEST** badge marks the cheapest per ml.
5. Use the dropdown to view the value as pence/ml, pence/100ml, or price/pint.

## How the maths works

- **Pence per ml** = `(price in £ × 100) ÷ (volume in ml × pack quantity)`
- **Price per pint** = `pence-per-ml × 568.261 ÷ 100` (UK imperial pint)
- **Pence per unit** = one UK unit is 10 ml of pure alcohol, so
  `units = total ml × (ABV ÷ 100) ÷ 10`, then `(price × 100) ÷ units`

## Hosting

This is a static site — just `index.html` plus an icon set and a web app
manifest, with no build step or server needed. It's published with
**GitHub Pages** from the `main` branch.

To run it locally, download the files and open `index.html` in a browser.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole app — markup, styles, and logic in one file |
| `manifest.webmanifest` | Web app config for Home Screen install |
| `icon-180.png` / `icon-192.png` / `icon-512.png` | App icons |
