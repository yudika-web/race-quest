from pathlib import Path
import re,hashlib
D=Path(__file__).resolve().parents[1];V=D.parent;B=V/'blokraya-patch8e-startup.html'
assert hashlib.sha256(B.read_bytes()).hexdigest()=='3b8803767a4c0854731260b990ac5bc5ee0da3e714b7c8013c8cd9da8a26fc69'
s=B.read_text()
for marker,file in [('function normalizeData','core.js'),('async function finish()','application.js')]:
 matches=[m for m in re.finditer(r'<script\b[^>]*>([\s\S]*?)</script>',s) if marker in m[1]];assert len(matches)==1
 m=matches[0];s=s[:m.start(1)]+(D/'source'/file).read_text()+s[m.end(1):]
dialog='''<dialog id="characterPurchaseDialog" aria-labelledby="characterPurchaseTitle"><div class="dialog-head"><h2 id="characterPurchaseTitle">Buka Karakter</h2></div><div class="dialog-body"><p id="characterPurchaseBalance"></p><p id="characterPurchaseMessage"></p></div><div class="dialog-foot"><button type="button" class="btn ghost" data-close="characterPurchaseDialog">Kembali</button><button type="button" class="btn" id="characterPurchaseBuy" data-act="buyCharacter">Buka Karakter</button></div></dialog>'''
assert s.count('</body>')==1;s=s.replace('</body>',dialog+'\n</body>')
# The dialog must exist before the application script executes (handlers use delegation).
p=V/'blokraya-patch8f-economy.html';p.write_text(s);print(p.name,p.stat().st_size)
