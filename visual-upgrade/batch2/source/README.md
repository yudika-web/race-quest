# Rebuild Batch 2

From a checkout of this development branch, with Blender 4.3, Python 3/Pillow,
Chromium and Playwright available:

```sh
blender -b --python-exit-code 1 --python visual-upgrade/batch2/source/build_batch2.py
python3 visual-upgrade/batch2/source/assemble_batch2.py --preview
python3 -m http.server 8000 --bind 127.0.0.1
# In another terminal:
node visual-upgrade/batch2/source/capture_avatars.cjs
python3 visual-upgrade/batch2/source/assemble_batch2.py
node visual-upgrade/batch2/source/capture_models.cjs before
node visual-upgrade/batch2/source/capture_models.cjs after
node visual-upgrade/batch2/source/capture_game.cjs before
node visual-upgrade/batch2/source/capture_game.cjs after
node visual-upgrade/batch2/source/capture_lineup.cjs
blender -b --python-exit-code 1 --python visual-upgrade/batch2/source/validate_models.py
python3 visual-upgrade/batch2/source/verify_scope.py
node visual-upgrade/batch2/source/test_core.cjs
node visual-upgrade/batch2/source/test_rigs.cjs
node visual-upgrade/batch2/source/test_preview_and_races.cjs
node visual-upgrade/batch2/source/test_game.cjs
node visual-upgrade/batch2/source/test_export.cjs
node visual-upgrade/batch2/source/test_unchanged_render.cjs
python3 visual-upgrade/batch2/source/measure_assets.py
python3 visual-upgrade/batch2/source/make_comparisons.py
python3 visual-upgrade/batch2/source/build_release.py
```

The running static server command intentionally blocks; start it once, not once per
script. No network access or server is needed to **play** the final HTML.

`blocky_factory.py`, the tested cockpit and wheel functions, and review/test
implementations are reused from `../../batch1/source/`. AST loads only the two
selected function definitions without running the Batch 1 build loop. The small
`reuse.cjs` adapters compile the existing test/capture implementations with explicit
Batch 2 identities, bounds and filenames. None of the old source is modified.

Test fixtures supply 1,000 tokens to the test context, then use the actual
60-token purchase and grid pagination. Distributed initial data and unlock rules
remain byte-identical. Shortened countdowns and repositioned quiz/finish fixtures
exercise actual game code; they do not constitute full manual race endurance tests.

`.blend` sources contain named editable pieces, vertex-colour materials, bevel and
weighted-normal modifiers, rigid hierarchy and a studio camera. Game axes are Y-up;
the Blender scene root adapts to Z-up. GLB exports bake evaluated geometry and
merge by rigid pivot/material, with optional expressions hidden by default scale
for standard glTF viewers. The game selects expression groups explicitly. Low LOD
is regenerated with one-segment bevels and reduced wheel/rim sectors, no subdivision
or heavy textures. All captures use the actual renderer; comparison scripts only
arrange/caption images and preserve matched camera matrices.
