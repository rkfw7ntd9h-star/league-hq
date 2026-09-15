from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker=r'''\n<script>\n/* career-points-leaderboard-v1 */\n'''
if marker not in s:
    raise SystemExit('broken career points marker not found')
start=s.index(marker)
end=s.index(r'''\n</script>\n</body></html>''', start)+len(r'''\n</script>\n''')
broken=s[start:end]
fixed=broken.replace(r'\n','\n')
s=s[:start]+fixed+s[end:]
p.write_text(s)
print('fixed literal newline escapes in career points script')
