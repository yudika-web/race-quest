# Rebuild the final Batch 4

Use this branch checkout, Blender 4.3, Python 3/Pillow and Chromium/Playwright.
The cloud runtime supplies the browser module path used by the test scripts.
Existing protected Batch 1–3 helpers/templates are required for rebuild; the final
HTML itself needs no server, installation, model download or Internet to play.

```sh
blender -b --python-exit-code 1 --python visual-upgrade/batch4/source/build_batch4.py
python3 visual-upgrade/batch4/source/assemble_batch4.py --preview
python3 -m http.server 8000 --bind 127.0.0.1
# Leave that server running; in another terminal:
node visual-upgrade/batch4/source/capture_avatars.cjs
python3 visual-upgrade/batch4/source/assemble_batch4.py
node visual-upgrade/batch4/source/capture_models.cjs before
node visual-upgrade/batch4/source/capture_models.cjs after
node visual-upgrade/batch4/source/capture_game.cjs before
node visual-upgrade/batch4/source/capture_game.cjs after
node visual-upgrade/batch4/source/capture_lineup.cjs
blender -b --python-exit-code 1 --python visual-upgrade/batch4/source/validate_models.py
python3 visual-upgrade/batch4/source/verify_scope.py
node visual-upgrade/batch4/source/test_core.cjs
node visual-upgrade/batch4/source/test_rigs.cjs
node visual-upgrade/batch4/source/test_preview_and_races.cjs
node visual-upgrade/batch4/source/test_game.cjs
node visual-upgrade/batch4/source/test_actors.cjs
node visual-upgrade/batch4/source/test_export.cjs
node visual-upgrade/batch4/source/test_unchanged_render.cjs
node visual-upgrade/batch4/source/test_all_characters.cjs
node visual-upgrade/batch4/source/test_file_offline.cjs
python3 visual-upgrade/batch4/source/measure_assets.py
python3 visual-upgrade/batch4/source/write_complete_catalog.py
python3 visual-upgrade/batch4/source/make_comparisons.py
python3 visual-upgrade/batch4/source/build_release.py
```

Start the static server only once. `--preview` permits missing portraits only during
bootstrap; final assembly requires all six actual WebP renders. The assembler
asserts the Batch 3 HTML hash, replaces only the three new pairs and avatars, adds
three lows/happy portraits, and extends the existing model/LOD/framing/expression
maps. It does not append a second engine, input controller or observer.

The builder imports `batch1/source/blocky_factory.py`, AST-loads only the cockpit
and wheel functions from Batch 1, face helper from Batch 2, and contact/low-screen
helper from Batch 3. It never executes old build loops or rebuilds historical assets.
Three independently authored character/vehicle functions follow the same contacts.

`.blend` sources contain named editable pieces, vertex-colour materials, bevel/
weighted-normal modifiers, rigid pivots and studio camera. Game Y-up is converted
by the Blender root to Z-up. High uses two bevel segments; low is regenerated with
one and fewer wheel/rim sectors. No subdivision, large texture or fur simulation.
The `.blend` files are self-contained for editing; HTML integration needs the repo.

GLBs merge by rigid pivot/material and retain default-hidden alternate expressions
for standard viewers. The game chooses those groups via the existing metadata.
Colours are vertex data. Shared PBR categories distinguish enamel, trim, alloy,
rubber, character, LEDs and smoked glass. No animations are driven by a new clock.

Test adapters reuse Batch 1 implementations with explicit species, bounds, blink
phase and pagination transforms. Test-only contexts supply 1,000 tokens then use
the real 60-token purchase. The distributed profile/initial data remain unchanged.
Countdown/gate/finish fixtures exercise real game logic without manual full races.
`test_all_characters.cjs` uses real selection/unlock, garage, both LODs, colour draw
submissions, countdown/racing and pause for all fourteen. `test_actors.cjs` checks
new AI/validated ghosts through RaceRenderer. Optional `file://` test records a
browser policy block distinctly from failures. Full GP endurance and physical HP
FPS are not claimed.

Screenshots use actual GLBs/RaceRenderer; primitive filters hide the vehicle or
character for isolated views. Lineup cameras/time/light/scale match within each
of the three sheets. Pillow only arranges/captions actual captured pixels.
