from pathlib import Path

p=Path('index.html')
s=p.read_text()
marker='/* squirrelification-v1 */'
if marker in s:
    print('Squirrel visuals already installed')
    raise SystemExit(0)
css=r'''
/* squirrelification-v1 */
.sectiontitle:before{content:"";display:block!important;width:48px;height:34px;flex:0 0 48px;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat;filter:drop-shadow(0 2px 1px rgba(0,0,0,.18))}
.sectionbar:before{content:"";display:block;width:38px;height:28px;flex:0 0 38px;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat;filter:drop-shadow(0 1px 1px rgba(0,0,0,.2))}
.sectionbar>img:first-child{display:none}
.tab.active:before{content:"";display:inline-block;width:21px;height:15px;margin:-4px 4px -3px 0;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat;vertical-align:middle}
.recordgrid .record:nth-child(3n+1){position:relative;overflow:hidden}
.recordgrid .record:nth-child(3n+1):after{content:"";position:absolute;right:-9px;bottom:-8px;width:48px;height:38px;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat;opacity:.13;transform:rotate(-7deg);pointer-events:none}
.managercard:nth-child(3n+2){position:relative;overflow:hidden}
.managercard:nth-child(3n+2):after{content:"";position:absolute;right:-10px;bottom:-9px;width:55px;height:42px;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat;opacity:.10;transform:scaleX(-1) rotate(-5deg);pointer-events:none}
.champ-main b:before{content:"";display:inline-block;width:28px;height:20px;margin:0 4px -5px 0;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat}
.loading:after{content:"";display:block;position:absolute;width:28px;height:20px;background:url("assets/squirrel-game-logo.webp") center/contain no-repeat;animation:squirrelrun 1.4s linear infinite;transform:translateY(-11px)}
.loading{position:relative;overflow:visible}
@keyframes squirrelrun{from{left:-30px}to{left:calc(100% + 5px)}}
@media(max-width:680px){.sectiontitle:before{width:40px;height:29px;flex-basis:40px}.sectionbar:before{width:32px;height:24px;flex-basis:32px}.tab.active:before{width:18px;height:13px;margin-right:3px}}
/* /squirrelification-v1 */
'''
if '</style>' not in s:
    raise SystemExit('style close tag not found')
s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s)
print('Squirrel visuals installed')
