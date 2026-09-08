from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

s = re.sub(r'<div class="big">\d+/\d+</div><h3>2026 Week 1 expert context</h3>', '<div class="big">9/8</div><h3>2026 Week 1 expert context</h3>', s)
s = re.sub(r'<p>Dated Sep\. \d+, 2026</p>', '<p>Dated Sep. 8, 2026</p>', s)
s = re.sub(r'/\* Dated public expert context, Sep\. \d+ 2026\.[\s\S]*?These are normalized signals, not a copied proprietary database\. \*/', '''/* Dated public expert context, Sep. 8 2026.\n   FantasyPros: Sep. 7 Half-PPR expert consensus + Week 1 waiver context.\n   Footballers: Sep. 6-7 public MVP/riser analysis plus current My Guys/value signals.\n   These are normalized League HQ signals, not copied proprietary ranking databases. */''', s)

fp = """const FP_RANK={
'jahmyrgibbs':1,'bijanrobinson':2,'jamarrchase':3,'pukanacua':4,'amonrastbrown':5,'jamescookiii':6,'jaxonsmithnjigba':7,'jonathantaylor':8,'kennethwalkeriii':9,'chasebrown':10,'christianmccaffrey':11,'ceedelamb':12,'justinjefferson':13,'saquonbarkley':14,'devonachane':15,'ajbrown':16,'drakelondon':17,'nicocollins':18,'omarionhampton':19,'brockbowers':20,'derrickhenry':21,'georgepickens':22,'ashtonjeanty':23,'chrisolave':24,'treymcbride':25,'maliknabers':26,'devontasmith':27,'joshallen':28,'zayflowers':30,'javontewilliams':32,'teehiggins':33,'breecehall':34,'jaylenwaddle':36,'garrettwilson':38,'colstonloveland':41,'terrymclaurin':46,'davidmontgomery':54,'djmoore':55,'christianwatson':57,
'juwanjohnson':93,'chrisrodriguezjr':106,'daltonschultz':112,'tyjaespears':129,'brentonstrange':114,'tjhockenson':132,'rashidshaheed':110,'denzelboston':118,'keenanallen':136,'woodymarks':130,'tylerallgeier':111,'mikewashingtonjr':122,'jonahcoleman':154,'jakobilane':140
};"""

ffb = """const FFB_SIGNAL={
'jahmyrgibbs':{r:1,n:'elite first-round anchor'},
'bijanrobinson':{r:2,n:'elite first-round anchor'},
'jamarrchase':{r:3,n:'first-round cornerstone'},
'amonrastbrown':{r:6,n:'high-floor first-round value'},
'kennethwalkeriii':{r:11,n:'first-round conviction and strong My Guy signal'},
'garrettwilson':{r:43,n:'Jason My Guy; fourth-round ADP called a steal'},
'omarionhampton':{r:20,n:'Jason My Guy; second-round smash endorsement'},
'christianwatson':{r:58,n:'Mike My Guy; value conviction'},
'colstonloveland':{r:34,n:'Sep. 6 MVP pick with TE1-overall upside case'},
'laddmcconkey':{r:45,n:'Andy My Guy; fourth-round value with OC upgrade'},
'calebwilliams':{r:80,n:'Andy My Guy; top-five QB upside case'},
'treveyonhenderson':{r:44,n:'writing-staff My Guy; explosive RB upside'},
'joshallen':{r:28,n:'elite QB anchor'},
'brockbowers':{r:20,n:'elite TE cornerstone'},
'treymcbride':{r:25,n:'elite TE tier'},
'christianmccaffrey':{r:8,n:'Sep. 6 MVP case: league-winning ceiling if healthy'},
'ajbrown':{r:14,n:'Sep. 6 MVP endorsement; strong rebound/value profile'},
'justinjefferson':{r:16,n:'elite talent with current price uncertainty'},
'zayflowers':{r:38,n:'high-end WR upside case'},
'breecehall':{r:41,n:'RB2-range value with ceiling'},
'teehiggins':{r:36,n:'strong mid-round value'},
'maliknabers':{r:31,n:'high weekly ceiling'},
'derrickhenry':{r:30,n:'strong RB value despite age curve'},
'jamesonwilliams':{r:35,n:'Sep. 6 MVP endorsement after 2025 WR9 finish'},
'tylerwarren':{r:48,n:'staff My Guy; target-share driven TE1 upside'},
'jakobilane':{r:88,n:'Sep. 7 preseason riser; monitor for immediate Ravens role'},
'kalebjohnson':{r:115,n:'Sep. 7 riser; contingent value behind Marshawn Lloyd'},
'chrisbell':{r:108,n:'Sep. 7 riser; low-rostered Miami WR with flex-path upside'},
'emanuelwilson':{r:122,n:'Sep. 7 riser; one usage break from waiver relevance'}
};"""

s = re.sub(r'const FP_RANK=\{[\s\S]*?\};\nconst FFB_SIGNAL=\{[\s\S]*?\};', fp + '\n' + ffb, s, count=1)
s = s.replace('2026 Half-PPR consensus ranking context. The snapshot is normalized into player-value scores instead of reproducing a proprietary ranking list.', 'Sep. 7 Half-PPR consensus plus Week 1 waiver/ranking context, normalized into player-value scores instead of reproducing a proprietary ranking list.')
s = s.replace('Public 2026 position rankings, “My Guys,” mock-draft and current value/risk analysis converted into player signals.', 'Public 2026 “My Guys,” Sep. 6 MVP calls, Sep. 7 Week 1 risers and current value/risk analysis converted into player signals.')

p.write_text(s)
