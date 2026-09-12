from pathlib import Path

p=Path('index.html')
s=p.read_text()
start=s.index('/* squirrelification-v1 */')
end=s.index('/* /squirrelification-v1 */',start)
block=s[start:end]
old='assets/squirrel-game-logo.webp'
new='assets/squirrel-ui.jpeg'
if old not in block:
    raise SystemExit('Expected squirrel UI references not found')
block=block.replace(old,new)
s=s[:start]+block+s[end:]
p.write_text(s)
print('Replaced squirrelification UI artwork with supplied image')
