from pathlib import Path
import base64,json
D=Path(__file__).resolve().parents[1];O=D/'icons';O.mkdir(exist_ok=True)
shapes={
'reflect':('<path d="M32 5 55 14v17c0 15-23 27-23 27S9 46 9 31V14Z" fill="#8b65ed"/>','<path d="m21 28 10-9 10 9M31 19v22h13m-5-6 7 6-7 6" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'),
'nitro':('<rect x="3" y="4" width="58" height="56" rx="13" fill="#183e59"/>','<path d="M22 8 8 35h13l-3 21 17-31H23l7-17Zm25 0L33 35h13l-3 21 17-31H48l7-17Z" fill="#ffbf58"/>'),
'grip':('<rect x="14" y="5" width="36" height="54" rx="14" fill="#243e49" stroke="#68dbb2" stroke-width="3"/>','<path d="m20 15 12 6 12-6M20 27l12 6 12-6M20 39l12 6 12-6" fill="none" stroke="#eafff4" stroke-width="5"/>'),
'radar':('<rect x="3" y="3" width="58" height="58" rx="14" fill="#103e48"/><g fill="none" stroke="#67e2c1" stroke-width="2"><circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="12"/><path d="M32 10v44M10 32h44m-22 0L47 16"/></g>','<g fill="#ffe399"><circle cx="22" cy="22" r="4"/><circle cx="42" cy="39" r="4"/></g>')}
assets={}
for id,parts in shapes.items():
 text='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'+''.join(parts)+'</svg>';p=O/(id+'.svg');p.write_text(text);data=text.encode();assets['icon_'+id+'.svg']={'uri':'data:image/svg+xml;base64,'+base64.b64encode(data).decode(),'bytes':len(data)}
(O/'icons.json').write_text(json.dumps(assets,separators=(',',':')))
