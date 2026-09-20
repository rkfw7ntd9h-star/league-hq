from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='<article class="card span6"><div class="eyebrow">Loser of the Week</div><div class="big" id="loserWeek">—</div><p class="muted" id="loserWeekNote"></p></article></div></section>'
new=old.replace('</article></div></section>','</article><article class="card span6"><div class="eyebrow">🔥 Highest Scoring Starters</div><div id="recapHighStarters"></div></article><article class="card span6"><div class="eyebrow">🧊 Lowest Scoring Starters</div><div id="recapLowStarters"></div></article><article class="card span12"><div class="eyebrow">🪑 Highest Scoring Bench Players</div><div id="recapBench"></div></article></div></section>')
if old not in s: raise SystemExit('recap markup target not found')
s=s.replace(old,new,1)
needle="function renderRecap(){"
start=s.index(needle)
end=s.index("function completedRecordGames()",start)
block=s[start:end]
anchor="const gs=group(done.matchups||[]),rw=$('recapWeekNo');"
if anchor not in block: raise SystemExit('recap function anchor not found')
helper=r'''const gs=group(done.matchups||[]),rw=$('recapWeekNo');const rosterById=id=>state.rosters.find(r=>+r.roster_id===+id),managerFor=m=>{const r=rosterById(m.roster_id);return r?teamName(r):'Unknown'},played=[];for(const m of done.matchups||[]){const starters=new Set((m.starters||[]).map(String));for(const id of (m.players||[])){const pts=Number(m.players_points?.[id]??0),pl=player(id);played.push({id,name:pl.full_name||String(id),pos:pl.position||'',pts,started:starters.has(String(id)),manager:managerFor(m)})}}const starterRows=played.filter(x=>x.started),benchRows=played.filter(x=>!x.started);const recapPlayerRows=(arr,empty)=>arr.length?arr.map((x,i)=>`<div class="rosterplayer"><b>${i+1}. ${esc(x.name)}</b><span>${esc(x.pos)} • ${x.pts.toFixed(1)} pts</span><span>${esc(x.manager)}</span></div>`).join(''):`<div class="empty">${empty}</div>`;$('recapHighStarters').innerHTML=recapPlayerRows([...starterRows].sort((a,b)=>b.pts-a.pts).slice(0,3),'No starter scoring data.');$('recapLowStarters').innerHTML=recapPlayerRows([...starterRows].sort((a,b)=>a.pts-b.pts).slice(0,3),'No starter scoring data.');$('recapBench').innerHTML=recapPlayerRows([...benchRows].sort((a,b)=>b.pts-a.pts).slice(0,3),'No bench scoring data.');'''
block=block.replace(anchor,helper,1)
s=s[:start]+block+s[end:]
p.write_text(s)
print('added recap starter and bench leaderboards')
