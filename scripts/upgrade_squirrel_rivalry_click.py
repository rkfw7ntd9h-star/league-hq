from pathlib import Path

p = Path('index.html')
s = p.read_text()
marker = '<!-- squirrel-rivalry-click-v2 -->'
if marker in s:
    raise SystemExit(0)

css = r'''
/* squirrel-rivalry-click-v2 */
#rivalry{cursor:pointer;position:relative}
#rivalry:after{content:"Tap for matchup + last 3 meetings →";display:block;text-align:center;margin-top:8px;color:var(--green);font-size:8px;font-weight:1000;text-transform:uppercase;letter-spacing:.04em}
.squirrel-history{margin-top:16px;border-top:2px solid #d7d5ce;padding-top:12px}
.squirrel-history h3{margin:0 0 8px;color:var(--forest);font:1000 17px Impact,Haettenschweiler,'Arial Narrow Bold',sans-serif;text-transform:uppercase}
.squirrel-history-row{display:grid;grid-template-columns:70px 1fr auto;gap:8px;align-items:center;padding:9px 0;border-top:1px solid #ddd9d2;font-size:10px}
.squirrel-history-row:first-of-type{border-top:0}
.squirrel-history-when{font-size:8px;color:var(--muted);font-weight:800;text-transform:uppercase}
.squirrel-history-result{font-weight:900;line-height:1.25}
.squirrel-history-score{font-size:13px;font-weight:1000;color:var(--forest);white-space:nowrap}
.squirrel-winner{color:var(--green)}
'''
if '</style>' not in s:
    raise SystemExit('No </style> marker; refusing unsafe edit')
s = s.replace('</style>', css + '</style>', 1)

js = r'''
<script>
<!-- squirrel-rivalry-click-v2 -->
(function(){
  function currentRosterByName(name){
    return (state.rosters||[]).find(function(r){return teamName(r,state.users||[])===name;})||null;
  }
  function lastThreeBetween(aRid,bRid){
    var aCur=(state.rosters||[]).find(function(r){return +r.roster_id===+aRid;});
    var bCur=(state.rosters||[]).find(function(r){return +r.roster_id===+bRid;});
    if(!aCur||!bCur)return[];
    var aUid=aCur.owner_id,bUid=bCur.owner_id,out=[];
    (state.history||[]).forEach(function(h){
      (h.weeks||[]).forEach(function(w){
        if(String(h.season)===String((state.league&&state.league.season)||'') && +w.week>=+week())return;
        (group(w.matchups||[])||[]).forEach(function(pair){
          if(!pair||pair.length<2)return;
          var x=pair[0],y=pair[1],xu=ownerId(h,x.roster_id),yu=ownerId(h,y.roster_id);
          var same=(String(xu)===String(aUid)&&String(yu)===String(bUid))||(String(xu)===String(bUid)&&String(yu)===String(aUid));
          if(!same)return;
          var xp=+x.points,yp=+y.points;
          if(!Number.isFinite(xp)||!Number.isFinite(yp))return;
          var aIsX=String(xu)===String(aUid),aPts=aIsX?xp:yp,bPts=aIsX?yp:xp;
          out.push({season:+h.season||0,week:+w.week||0,aPts:aPts,bPts:bPts});
        });
      });
    });
    out.sort(function(m,n){return n.season-m.season||n.week-m.week;});
    return out.slice(0,3);
  }
  function addHistory(aRid,bRid,aName,bName){
    var sheet=document.querySelector('#modal .sheet');
    if(!sheet)return;
    var old=sheet.querySelector('.squirrel-history');if(old)old.remove();
    var games=lastThreeBetween(aRid,bRid);
    var block=document.createElement('div');block.className='squirrel-history';
    var html='<h3>Last 3 Meetings</h3>';
    if(games.length){
      html+=games.map(function(g){
        var tie=g.aPts===g.bPts,aWon=g.aPts>g.bPts;
        var winner=tie?'Tie':(aWon?aName:bName),loser=tie?'':(aWon?bName:aName);
        return '<div class="squirrel-history-row"><div class="squirrel-history-when">'+g.season+' · Week '+g.week+'</div><div class="squirrel-history-result">'+(tie?'<span>Tie</span>':'<span class="squirrel-winner">'+winner+' won</span><br><span class="muted">'+loser+' lost</span>')+'</div><div class="squirrel-history-score">'+g.aPts.toFixed(1)+' – '+g.bPts.toFixed(1)+'</div></div>';
      }).join('');
    }else{
      html+='<div class="empty">No previous Sleeper matchups found between these managers.</div>';
    }
    block.innerHTML=html;sheet.appendChild(block);
  }
  document.addEventListener('click',function(e){
    var r=e.target.closest&&e.target.closest('#rivalry');
    if(!r)return;
    var names=Array.prototype.slice.call(r.querySelectorAll('.rivalryteam .teamname')).map(function(x){return x.textContent.trim();}).filter(Boolean);
    if(names.length<2)return;
    var a=currentRosterByName(names[0]),b=currentRosterByName(names[1]);
    if(!a||!b)return;
    showMatchup(+a.roster_id,+b.roster_id);
    setTimeout(function(){addHistory(+a.roster_id,+b.roster_id,names[0],names[1]);},0);
  },true);
})();
</script>
'''
if '</body>' not in s:
    raise SystemExit('No </body> marker; refusing unsafe edit')
s = s.replace('</body>', js + '</body>', 1)
p.write_text(s)
