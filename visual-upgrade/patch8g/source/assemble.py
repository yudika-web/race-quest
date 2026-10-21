from pathlib import Path
import re,hashlib
D=Path(__file__).resolve().parents[1];V=D.parent;B=V/'blokraya-patch8f-economy.html'
assert hashlib.sha256(B.read_bytes()).hexdigest()=='b2f926f52e9a127ec96fe37c28d6563e4c39692790104b5d568f50f60f8f834e'
s=B.read_text()
s,n=re.subn(r'(<script id="studentOnboarding">)[\s\S]*?(</script>)',lambda m:m[1]+(D/'source/onboarding.js').read_text()+m[2],s);assert n==1
replacements={
 '<span>Nama panggilan</span>':'<span>Nama Siswa</span>',
 '<span>Kelas siswa</span>':'<span>Kelas</span>',
 'placeholder="Nama pembalap"':'placeholder="Nama siswa"',
 'lalu raih garis finis bersama teman AI.':'lalu raih garis finis bersama lawan komputer.',
 'Otomatis · sesuai perangkat/input':'Otomatis · sesuai perangkat dan kontrol',
}
for a,b in replacements.items():
 assert a in s,a;s=s.replace(a,b)
s=s.replace('</head>','<style id="patch8gTypography">\n'+(D/'source/typography.css').read_text()+'</style>\n</head>')
p=V/'blokraya-patch8g-ui-polish.html';p.write_text(s);print(p.name,p.stat().st_size,'bytes; growth',p.stat().st_size-B.stat().st_size)
