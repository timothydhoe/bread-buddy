# TODO

## Next up

- [ ] **Unit tests** — pytest coverage for model calculations (Recipe, Dough, BakeTimeline). No tests exist yet.
- [ ] **Pre-fermented flour percentage** — levain as % of total flour (ref: The Perfect Loaf pp.130–131)
- [ ] **Levain percentage** — separate from starter %, relevant for recipes that build a dedicated levain
- [ ] **Flour substitution hints** — swapping T60 for T150, rye for spelt: affect on hydration and fermentation
- [ ] **Extract magic numbers to constants** — `1.12` fermentation factor, friction factor defaults, etc. Currently scattered across `dough.py` and `timeline.py`

## Nice-to-have

- [ ] **Oven spring estimator** — can % rise in oven be modelled from hydration + proof state?
- [ ] **Flour class model** — water absorption capacity per flour type (affects hydration targets)
- [ ] **Push notifications (server-side)** — upgrade from `setTimeout`-based reminders to true Web Push via a backend. Requires VAPID keys + a push subscription endpoint. Current implementation works when the PWA is open or backgrounded on iOS 16.4+; server push would work even when fully closed.
- [ ] **Recipe export** — download as PDF or plain text

## Done

- [x] Baker's percentage calculator
- [x] Hydration calculator with live sidebar
- [x] Water temperature calculator (DDT formula)
- [x] Bulk fermentation time adjuster
- [x] Sourdough starter feeding calculator
- [x] Bake timeline (backwards-planned from target time)
- [x] Recipe scaler (loaf count multiplier)
- [x] Flour blend support (multi-flour recipes)
- [x] Recipe save/load (localStorage, no server round-trip)
- [x] Recipe sharing (URL params)
- [x] Bake log
- [x] The Science reference page
- [x] Troubleshooting guide
- [x] Stateless Flask server (no session state)
- [x] PWA: installable on iPhone/iPad, offline-capable
- [x] Bake step notifications (browser Notifications API + service worker)
- [x] Mobile bottom sheet sidebar
- [x] Progressive disclosure stepper
- [x] Quick bake log (one-tap outcome)
- [x] Auto-restore last recipe on page load
