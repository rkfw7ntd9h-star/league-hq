from pathlib import Path
p=Path('index.html')
s=p.read_text()
link='<link rel="stylesheet" href="assets/squirrel-nav.css?v=2">'
if link in s:
    print('Squirrel navigation already installed')
    raise SystemExit(0)
# Remove any earlier version of this stylesheet link, then install v2.
import re
s=re.sub(r'<link[^>]+href=["\']assets/squirrel-nav\.css[^"\']*["\'][^>]*>','',s)
if '</head>' not in s:
    raise SystemExit('head anchor not found')
s=s.replace('</head>',link+'</head>',1)
p.write_text(s)
print('Installed squirrel sign navigation stylesheet')
