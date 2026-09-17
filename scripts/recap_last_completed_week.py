from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="state.matchups=await j(`${API}/league/${LEAGUE}/matchups/${week()}`).catch(()=>[]);if(week()>1)state.last=await j(`${API}/league/${LEAGUE}/matchups/${week()-1}`).catch(()=>[]);"
new="state.matchups=await j(`${API}/league/${LEAGUE}/matchups/${week()}`).catch(()=>[]);const recapWeek=Math.max(0,week()-1);state.last=recapWeek?await j(`${API}/league/${LEAGUE}/matchups/${recapWeek}`).catch(()=>[]):[];"
if old not in s: raise SystemExit('boot recap target not found')
s=s.replace(old,new,1)
# Label the recap section with the actual completed week without touching matchup/home week labels.
old2='<div class="sectionbar">Last Week Final Scores</div><div id="recapScores"></div>'
new2='<div class="sectionbar">Week <span id="recapWeekNo">—</span> Final Scores</div><div id="recapScores"></div>'
if old2 not in s: raise SystemExit('recap label target not found')
s=s.replace(old2,new2,1)
old3="document.querySelectorAll('.weekNo').forEach(x=>x.textContent=week());renderPower();renderCurrent();historyEvent();renderRecap();"
new3="document.querySelectorAll('.weekNo').forEach(x=>x.textContent=week());const rw=document.getElementById('recapWeekNo');if(rw)rw.textContent=week()>1?week()-1:'—';renderPower();renderCurrent();historyEvent();renderRecap();"
if old3 not in s: raise SystemExit('render recap target not found')
s=s.replace(old3,new3,1)
p.write_text(s)
print('Recap now explicitly uses the most recently completed Sleeper week.')
