# Dream Ball

A hi-bit pixel-art 3-on-3 basketball game you can install on your phone. Collect 87 players and show off your starting three on the home screen, pull six banners with Basket Bucks for players, cards and shoes, build a deck of up to 50 cards from 68 play, dribble, shot, pass and defense cards, and play a story-mode season where you hold 8 cards and spend stamina to make plays. Hold shot cards and release on green. The Shop lists Basket Bucks packs in US dollars (checkout is not open yet). Frame rate (30/60/120) and pixel size (Low to Max) are in Settings.

## Play

Open the GitHub Pages link for this repo on your phone, then:

- **Android (Chrome):** tap **Install** in the top bar, or use the menu's "Add to Home screen".
- **iPhone (Safari):** tap Share, then "Add to Home Screen".

After the first load it works offline. Progress saves on the device.

## Files

- `index.html` — the whole game
- `manifest.webmanifest` — app name, icons and portrait lock
- `sw.js` — service worker for offline play
- `icons/` — home-screen icons

When you change `index.html`, bump `VERSION` in `sw.js` so installed copies pick up the update.
