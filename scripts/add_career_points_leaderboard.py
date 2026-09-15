from pathlib import Path

p=Path('index.html')
s=p.read_text()
MARK='career-points-leaderboard-v1'
if MARK in s:
    raise SystemExit('already installed')

css='''\n/* career-points-leaderboard-v1 */\n.careerptsrow{grid-template-columns:32px minmax(110px,1.45fr) .7fr .7fr .65fr}\n.careerpts-sort{cursor:pointer;user-select:none}.careerpts-sort.active{text-decoration:underline;text-underline-offset:3px}\n.netpos{color:#0b8150;font-weight:1000}.netneg{color:#9f3d3d;font-weight:1000}\n@media(max-width:680px){.careerptsrow{grid-template-columns:30px minmax(105px,1.3fr) .68fr .68fr .62fr}.careerptsrow{font-size:9px}}\n'''
s=s.replace('</style>',css+'</style>',1)

needle='<div class="sectiontitle"><h2>All-Time Managers</h2></div>'
block='''<div class="sectiontitle"><h2>Career Points Leaderboard</h2></div><div class="table" id="careerPointsTable"><div class="trow careerptsrow thead"><b>#</b><b>Manager</b><b class="careerpts-sort active" data-cpsort="pf">Points For ↕</b><b class="careerpts-sort" data-cpsort="pa">Points Against ↕</b><b class="careerpts-sort" data-cpsort="net">Net +/- ↕</b></div><div id="careerPointsRows"></div></div>'''
if needle not in s: raise SystemExit('records insertion point not found')
s=s.replace(needle,block+needle,1)

js=r'''\n<script>\n/* career-points-leaderboard-v1 */\n(function(){\n  var sortKey='pf';\n  function managerName(h,uid){\n    var u=(h.users||[]).find(function(x){return String(x.user_id)===String(uid)});\n    return (u&&(u.display_name||u.username))||String(uid||'Unknown');\n  }\n  function totals(){\n    var by={};\n    (state.history||[]).forEach(function(h){\n      (h.weeks||[]).forEach(function(w){\n        var ms=w.matchups||w.data||w; if(!Array.isArray(ms))return;\n        var groups={};\n        ms.forEach(function(m){if(m&&m.matchup_id!=null)(groups[m.matchup_id]||(groups[m.matchup_id]=[])).push(m)});\n        Object.keys(groups).forEach(function(k){\n          var pair=groups[k]; if(pair.length!==2)return;\n          var a=pair[0],b=pair[1],ap=Number(a.points),bp=Number(b.points);\n          if(!Number.isFinite(ap)||!Number.isFinite(bp))return;\n          var au=ownerId(h,+a.roster_id),bu=ownerId(h,+b.roster_id); if(!au||!bu)return;\n          if(!by[au])by[au]={uid:au,name:managerName(h,au),pf:0,pa:0};\n          if(!by[bu])by[bu]={uid:bu,name:managerName(h,bu),pf:0,pa:0};\n          by[au].pf+=ap;by[au].pa+=bp;by[bu].pf+=bp;by[bu].pa+=ap;\n        });\n      });\n    });\n    return Object.keys(by).map(function(k){var x=by[k];x.net=x.pf-x.pa;return x});\n  }\n  function render(){\n    var root=document.getElementById('careerPointsRows');if(!root)return;\n    var rows=totals().sort(function(a,b){return (b[sortKey]-a[sortKey])||(b.pf-a.pf)}).slice(0,12);\n    root.innerHTML=rows.map(function(x,i){var n=x.net,cls=n>0?'netpos':n<0?'netneg':'';return '<div class="trow careerptsrow"><b class="ranknum '+(i===0?'one':'')+'">'+(i+1)+'</b><b>'+x.name+'</b><span>'+x.pf.toFixed(1)+'</span><span>'+x.pa.toFixed(1)+'</span><span class="'+cls+'">'+(n>0?'+':'')+n.toFixed(1)+'</span></div>'}).join('')||'<div class="empty">Career scoring data is unavailable.</div>';\n    document.querySelectorAll('.careerpts-sort').forEach(function(x){x.classList.toggle('active',x.dataset.cpsort===sortKey)});\n  }\n  document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-cpsort]');if(!b)return;sortKey=b.dataset.cpsort;render()});\n  var old=switchPage;switchPage=function(page){old(page);if(page==='records')setTimeout(render,0)};\n})();\n</script>\n'''
s=s.replace('</body>',js+'</body>',1)
p.write_text(s)
