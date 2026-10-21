# PATCH 8F — Token economy and unlock persistence

Baseline: `34b9defab52e2b992235f24ce8162e411f6833cd` (PATCH 8E). Distribution: `../blokraya-patch8f-economy.html`.

## Verified cause and policy

`normalizeData()` explicitly supplied all 14 character IDs when a profile was absent. This differed from `sampleData()` and `normalizeProfile()`, whose defaults were already correct. The browser comparison reproduces this with the same missing-profile fixture in 8E and 8F. Missing/null profiles now receive 0 tokens and `[0,1,2,3]`; valid saved profiles, including all-unlocked profiles, remain valid. Already-saved accidental unlocks cannot reliably be distinguished from purchases, so they are not revoked.

Bank JSON import adds banks only and never replaces the recipient profile, whether the file includes a profile or not. Loading a saved application/package with a valid profile retains its normalized balance/unlocks. Teacher HTML export deliberately creates a fresh student profile, preserving the exporting device's data and excluding its PIN. Storage keys are unchanged.

## Transactions and rewards

Locked cards show name, price (60), balance and an explicit purchase action. Insufficient balances disable purchase and explain how to earn tokens. A second confirmation precedes payment. A transaction guard prevents concurrent purchases; the pure purchase function also returns already-unlocked characters without charging. Failed local storage writes roll the in-memory purchase back. Successful purchases save and update the garage immediately. Extra paints remain 40 tokens.

Reward amounts are unchanged: track pickups + 10 completion + 15 for first place. The existing daily ten-correct bonus is 30 tokens, once per day. Existing achievements are badges, not additional token awards. Grand Prix rounds use the same result reward path; no new cup payout was introduced. Tokens collected on track enter the wallet when the race result is settled, as before.

A session settlement marker prevents repeat history/progress/Grand Prix/reward processing. A bounded ledger of the latest 256 result IDs persists with the profile, making repeated reward calls for the same result idempotent after normalization/reload. Existing results without receipts are not retrospectively awarded or deducted. Results and profile continue to save atomically in the same localStorage value. Failed race saves retain the result in memory and display the existing storage warning; no durable-storage guarantee is claimed when the browser rejects writes.

## Build and tests

Run from repository root:

```sh
python visual-upgrade/patch8f/source/assemble.py
node visual-upgrade/patch8f/source/test_economy.cjs
node visual-upgrade/patch8f/source/test_browser.cjs
node visual-upgrade/patch8f/source/test_edges.cjs
node visual-upgrade/patch8f/source/test_visual.cjs
node visual-upgrade/patch8f/source/test_flow.cjs
python visual-upgrade/patch8f/source/test_scope.py
python visual-upgrade/patch8f/source/package.py
```

Browser tests use Chromium and Playwright installed in the execution environment. Test profiles/balances are injected into isolated browser contexts or VM fixtures, never into the distributed HTML. `test_browser` uses a test-only instrumented document to call the actual finish handler twice; its race is accelerated to completion for settlement verification, not a claim of a complete manual race. The inherited flow regression drives a quiz, analog+gas+drift, pause, results, podium, replay, teacher PIN and exported offline game. Fresh and legacy profile fixtures are separate.

Screenshots are actual browser/game renders. `before-missing-profile.png` versus `after-locked-garage.png` reproduces the reported fallback case. Purchase/confirmation/success, mobile dialogs and actual podium are also included. Machine-readable evidence is in `*-results.json` and `flow-tests.json`; exact protected payload hashes and source diffs accompany this report.

No full 13-stage physics benchmark was repeated: stage, AI, buff, model, control, podium and startup script payloads are unchanged. No physical phone/iOS tests or FPS claims. Offline is tested with the network-disabled browser context and locally fulfilled HTML, including teacher-export output; direct file:// navigation is blocked by this managed browser policy and is not claimed tested here. No CDN or new asset requests.
