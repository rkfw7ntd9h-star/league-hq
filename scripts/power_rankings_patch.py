from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

css = '''
.power-intro{margin:0 4px 10px;font-size:9px;line-height:1.45;color:var(--muted)}
.powercards{display:grid;gap:10px}
.powercard{background:var(--paper);border:1px solid #cac9c3;border-radius:15px;box-shadow:var(--shadow);overflow:hidden}
.powerhead{display:grid;grid-template-columns:42px minmax(0,1fr) auto;gap:9px;align-items:center;padding:11px 12px;background:linear-gradient(180deg,#fffdf7,#f7f2e8)}
.power-rank{width:34px;height:34px;border-radius:9px;background:var(--forest);color:#fff;display:grid;place-items:center;font:1000 17px Impact,Haettenschweiler,'Arial Narrow Bold',sans-serif}
.powercard:first-child .power-rank{background:var(--green)}
.powerteam{min-width:0}.powerteam .teamname{font-size:14px}.power-meta{font-size:8px;color:var(--muted);margin-top:2px}
.powertrend{text-align:right;font-size:9px;font-weight:1000;white-space:nowrap}.powertrend .arrow{font-size:18px;line-height:.8;display:block}
.powertrend.up{color:#0b8150}.powertrend.down{color:var(--red)}.powertrend.flat{color:#7b847f}
.powerbody{padding:10px 12px 12px;border-top:1px solid #dedbd3}.powerwhy{font-size:10px;line-height:1.45;margin-bottom:9px}
.powerchips{display:grid;grid-template-columns:1fr 1fr;gap:8px}.powerchip{border-radius:10px;padding:8px 9px;font-size:9px;line-height:1.4}
.powerchip.good{background:#e7f3ec;color:#0b5f3f}.powerchip.bad{background:#f5e9e6;color:#823a32}.powerchip b{display:block;text-transform:uppercase;font-size:7px;letter-spacing:.06em;margin-bottom:3px}
.power-stars{font-size:8px;color:var(--muted);margin-top:8px}
@media(max-width:420px){.powerhead{grid-template-columns:38px minmax(0,1fr) auto;padding:10px}.powerbody{padding:9px 10px 11px}.powerchips{gap:6px}.powerteam .teamname{font-size:13px}}
'''
if '.powercards{' not in s:
    s = s.replace('</style></head>', css + '</style></head>')

old_section = '<section class="page" id="page-power"><div class="sectiontitle"><h2>Power Rankings</h2></div><div class="tiny" style="margin:0 4px 9px">HQ blend: <b>50% live Sleeper league/player data</b> + <b>25% FantasyPros</b> + <b>25% Fantasy Footballers</b>. Expert context is a dated snapshot (Sep 10, 2026); Sleeper data stays live.</div><div class="table"><div class="trow powrow thead"><b>Rank</b><b>Team</b><b>HQ</b><b>Move</b><b>Record</b></div><div id="powerRows"></div></div></section>'
new_section = '<section class="page" id="page-power"><div class="sectiontitle"><h2>Power Rankings</h2></div><div class="power-intro">HQ ranking blends <b>roster strength</b> with <b>current results</b>. Trend arrows use recent scoring versus the league average. Strengths and weaknesses compare each position group to the rest of the Traphouse.</div><div id="powerRows" class="powercards"></div></section>'
if old_section in s:
    s = s.replace(old_section, new_section)
elif 'class="powercards"' not in s:
    raise SystemExit('power section not found')

new_func = r'''function powerSeason(){const y=+state.league?.season;return state.history.find(h=>+h.season===y)||state.history[state.history.length-1]}function positionGrade(r,pos){const take={QB:1,RB:3,WR:4,TE:2,DEF:1,DST:1}[pos]||2,v=(r.players||[]).map(expert).filter(x=>x.position===pos||(pos==='DEF'&&x.position==='DST')).sort((a,b)=>b.score-a.score).slice(0,take);return v.length?v.reduce((a,x)=>a+x.score,0)/v.length:48}function recentTrend(r){const h=powerSeason();if(!h)return{dir:'flat',label:'Steady',note:'No recent scoring sample'};const samples=[];h.weeks.filter(w=>w.week<week()).slice(-3).forEach(w=>{const all=w.matchups.filter(m=>(+m.points||0)>0),me=all.find(m=>m.roster_id===r.roster_id);if(me&&all.length){const avg=all.reduce((a,m)=>a+(+m.points||0),0)/all.length;samples.push((+me.points||0)-avg)}});if(!samples.length)return{dir:'flat',label:'Steady',note:'No completed week trend yet'};const wt=[.15,.3,.55].slice(3-samples.length),ws=wt.reduce((a,b)=>a+b,0),d=samples.reduce((a,v,i)=>a+v*wt[i],0)/ws;if(d>4)return{dir:'up',label:'Rising',note:'Recent scoring '+d.toFixed(1)+' above league avg'};if(d<-4)return{dir:'down',label:'Falling',note:'Recent scoring '+Math.abs(d).toFixed(1)+' below league avg'};return{dir:'flat',label:'Steady',note:'Recent scoring near league avg'}}function ordinal(n){const a=['th','st','nd','rd'],v=n%100;return n+(a[(v-20)%10]||a[v]||a[0])}function renderPower(){const standings=renderStandings(),perf=Object.fromEntries(standings.map((r,i)=>[r.roster_id,100-i*(45/Math.max(1,standings.length-1))])),rows=state.rosters.map(r=>({r,ros:rosterROS(r)})).map(x=>({...x,hq:Math.round(.8*x.ros+.2*perf[x.r.roster_id])})).sort((a,b)=>b.hq-a.hq),rosOrder=[...rows].sort((a,b)=>b.ros-a.ros),positions=['QB','RB','WR','TE','DEF'],avg={};positions.forEach(pos=>avg[pos]=state.rosters.reduce((a,r)=>a+positionGrade(r,pos),0)/Math.max(1,state.rosters.length));$('powerRows').innerHTML=rows.map((x,i)=>{const rr=rosOrder.findIndex(y=>y.r.roster_id===x.r.roster_id)+1,sr=standings.findIndex(y=>y.roster_id===x.r.roster_id)+1,tr=recentTrend(x.r),pg=positions.map(pos=>({pos,diff:positionGrade(x.r,pos)-avg[pos]})).sort((a,b)=>b.diff-a.diff),good=pg.slice(0,2),bad=[...pg].sort((a,b)=>a.diff-b.diff).slice(0,2),stars=(x.r.players||[]).map(expert).sort((a,b)=>b.score-a.score).slice(0,3).map(z=>z.name),strength=good.map(z=>z.pos+' '+(z.diff>=0?'+':'')+z.diff.toFixed(1)+' vs league').join(' | '),weakness=bad.map(z=>z.pos+' '+(z.diff>=0?'+':'')+z.diff.toFixed(1)+' vs league').join(' | '),trendText=tr.dir==='up'?'recent scoring is pushing them upward':tr.dir==='down'?'recent scoring is dragging them down':'recent scoring is roughly league-average',why='Ranked #'+(i+1)+' because the roster grades '+ordinal(rr)+' in rest-of-season strength, the team sits '+ordinal(sr)+' in the standings, and '+trendText+'.',arrow=tr.dir==='up'?'&#9650;':tr.dir==='down'?'&#9660;':'&#8594;';return`<article class="powercard"><div class="powerhead"><div class="power-rank">${i+1}</div><div class="powerteam"><div class="team">${avatar(x.r)?`<img class="avatar" src="${avatar(x.r)}">`:''}<div><div class="teamname">${esc(teamName(x.r))}</div><div class="power-meta">HQ ${x.hq} | ${rec(x.r)} | ROS ${ordinal(rr)}</div></div></div></div><div class="powertrend ${tr.dir}"><span class="arrow">${arrow}</span>${tr.label}</div></div><div class="powerbody"><div class="powerwhy">${esc(why)}</div><div class="powerchips"><div class="powerchip good"><b>Strengths</b>${esc(strength)}</div><div class="powerchip bad"><b>Weaknesses</b>${esc(weakness)}</div></div><div class="power-stars"><b>Core:</b> ${esc(stars.join(', ')||'Roster data unavailable')}<br><b>Trend:</b> ${esc(tr.note)}</div></div></article>`}).join('')}'''

m = re.search(r'function renderPower\(\)\{.*?\}function historyEvent', s, re.S)
if m:
    s = s[:m.start()] + new_func + 'function historyEvent' + s[m.end():]
elif 'function powerSeason()' not in s:
    raise SystemExit('renderPower block not found')

p.write_text(s)
