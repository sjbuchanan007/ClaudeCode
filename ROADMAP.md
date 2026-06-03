# 🗺️ Roadmap — Beer Value Calculator

A living plan for where the app is headed. Items are grouped into phases by
priority, not fixed dates. ✅ = done · 🔜 = next up · 💡 = idea / later.

## ✅ Shipped

- Pence-per-ml comparison with best-value ranking
- Value display toggle (pence/ml, pence/100ml, price/pint)
- Multipack support and optional ABV → pence-per-unit
- Local saving of the beer list and chosen units
- Home Screen install support (icons + web manifest, iOS meta tags)
- Light / dark / auto theme toggle (follows system, remembered between visits)
- Custom "v" lettermark branding (app icons, header logo, favicon)
- Analytics: Cloudflare Web Analytics (page views) + GoatCounter (custom events)
- Share button: native share sheet + copy-to-clipboard, with share-event tracking

## 🔜 Phase 1 — Must-haves

### Share to social media
- [x] Native share sheet via the Web Share API (one tap to WhatsApp, Messages, X, etc.)
- [x] "Copy summary" to clipboard (desktop fallback)
- [x] Track when the share function is used (GoatCounter events)
- [ ] Shareable link that encodes the current comparison in the URL
- [ ] Export results as a designed image card for posting to social

### Light / dark mode ✅
- [x] Manual light/dark toggle
- [x] "Auto" option that follows the device's system theme
- [x] Remember the choice between visits

## 🔜 Phase 2 — Calculator improvements

- [ ] Edit existing entries inline (currently add/delete only)
- [ ] Sort options: by value, price, ABV, or name
- [ ] More units: per litre, per serving, per standard drink
- [ ] Categories/tags (lager, IPA, stout…) with filtering
- [ ] Currency support for buying abroad

## 💡 Phase 3 — App-like power

- [ ] Full offline support (PWA service worker) so it works with no internet
- [ ] Multiple saved comparison lists (e.g. "Tesco run" vs "Festival stock-up")
- [ ] Preset beer database to auto-fill volume/ABV for common beers
- [ ] Barcode scanning to auto-fill a beer from its packaging

## 💡 Phase 4 — Polish & reach

- [ ] Accessibility pass (screen reader labels, keyboard navigation)
- [x] Subtle animations — slide-in on add, fade-out on remove, FLIP re-ranking, value count-up
- [ ] Haptic feedback on mobile
- [ ] First-run tip / lightweight onboarding
- [ ] Custom domain (e.g. thevaluator.app)

---

*Suggestions welcome — open an issue or add to the relevant phase above.*
