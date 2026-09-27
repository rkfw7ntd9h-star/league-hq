from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="const best=[...scored].sort((a,b)=>b.value-a.value||b.points-a.points).slice(0,5),busts=[...scored].sort((a,b)=>a.value-b.value||a.points-b.points).slice(0,5)"
new="const best=[...scored].sort((a,b)=>b.value-a.value||b.points-a.points).slice(0,10),busts=[...scored].sort((a,b)=>a.value-b.value||a.points-b.points).slice(0,10)"
if old not in s: raise SystemExit('draft top-5 target not found')
s=s.replace(old,new,1)
p.write_text(s)
print('expanded draft best picks and busts to 10')
