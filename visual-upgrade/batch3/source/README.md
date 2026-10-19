# Rebuild Batch 3

Use a checkout of this branch, Blender 4.3, Python 3/Pillow, Chromium and
Playwright (the cloud runtime provides the latter). No installation or server is
needed to **play** the delivered standalone HTML.

```sh
blender -b --python-exit-code 1 --python visual-upgrade/batch3/source/build_batch3.py
python3 visual-upgrade/batch3/source/assemble_batch3.py --preview
python3 -m http.server 8000 --bind 127.0.0.1
# Leave the server running; in another terminal:
node visual-upgrade/batch3/source/capture_avatars.cjs
python3 visual-upgrade/batch3/source/assemble_batch3.py
node visual-upgrade/batch3/source/capture_models.cjs before
node visual-upgrade/batch3/source/capture_models.cjs after
node visual-upgrade/batch3/source/capture_game.cjs before
node visual-upgrade/batch3/source/capture_game.cjs after
node visual-upgrade/batch3/source/capture_lineup.cjs
blender -b --python-exit-code 1 --python visual-upgrade/batch3/source/validate_models.py
python3 visual-upgrade/batch3/source/verify_scope.py
node visual-upgrade/batch3/source/test_core.cjs
node visual-upgrade/batch3/source/test_rigs.cjs
node visual-upgrade/batch3/source/test_preview_and_races.cjs
node visual-upgrade/batch3/source/test_game.cjs
node visual-upgrade/batch3/source/test_export.cjs
node visual-upgrade/batch3/source/test_unchanged_render.cjs
node visual-upgrade/batch3/source/test_actors.cjs
python3 visual-upgrade/batch3/source/measure_assets.py
python3 visual-upgrade/batch3/source/make_comparisons.py
python3 visual-upgrade/batch3/source/build_release.py
```

Run the static server only once. The assembler asserts the baseline HTML hash.
It replaces three pairs/portraits and extends the existing model map, blink phases,
close-up framing, expression widget and results mapping. It embeds no second engine.

`build_batch3.py` reuses `batch1/source/blocky_factory.py`, the Batch 1 cockpit/wheel
functions, and Batch 2's face-expression helper. AST loads only selected function
definitions, without executing old build loops. The three character/vehicle meshes
are authored independently in this stage. The six GLBs are texture-free and merged
by rigid pivot/material, with two-segment high / one-segment low bevels and reduced
wheel sectors. There is no subdivision. Default alternate facial groups are hidden
for standard GLTF viewers; the game selects expression groups explicitly.

Each high `.blend` contains editable named pieces, vertex-colour materials, bevel
and weighted-normal modifiers, rigid hierarchy and studio camera. The scene root
converts game Y-up to Blender Z-up. Rebuilding low LOD uses the script rather than a
second .blend. Each .blend can be edited on its own; rebuilding/integrating the HTML
requires this repository checkout and the protected Batch 1/2 helpers/template.

Small `reuse.cjs` adapters reuse the original capture/regression implementation.
Their explicit species specs include bounds, eye/mouth positions, blink offsets,
second-page selection and file paths. Tests supply 1,000 tokens in test contexts,
then exercise the real purchase/unlock UI; distributed unlock/data are unchanged.
Countdown, gate and finish fixtures shorten testing while executing actual game
logic. `test_actors.cjs` uses a real Session plus validated ghost samples to check
new AI and translucent ghosts. It writes actual race-renderer captures.

Comparisons use exactly matched view/projection/resolution/time, with independent
character/vehicle primitive visibility filters. Images are actual GLB/game renders;
Pillow only captions and arranges them. `evaluation/first-pass/` retains geometry
before the targeted panel/windscreen/hubcap corrections.
