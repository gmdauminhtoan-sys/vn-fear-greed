"""
build.py — Chạy bởi GitHub Actions mỗi khi có CSV mới
1. Tìm file CSV mới nhất trong csv/
2. Merge vào data.json
3. Tạo index.html (dashboard)
"""

import csv, json, os, glob

def read_csv(path):
    records = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = [h.strip() for h in reader.fieldnames]
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            records.append([
                row['Date/Time'].split(' ')[0],
                round(float(row['vni_close']),1), round(float(row['vni_pct_chg']),2),
                round(float(row['vni_rsi']),1), int(float(row['advance'])),
                int(float(row['decline'])), int(float(row['ceiling'])),
                int(float(row['floor'])), int(float(row['total_stocks'])),
                int(float(row['above_ma50'])), int(float(row['ema_cross'])),
                round(float(row['volume']),2), round(float(row['parkinson_vol']),2),
                round(float(row['vol_ratio']),2), round(float(row['ad_ratio']),2),
                round(float(row['thrust_pct']),2),
            ])
    return records

def _pd(d):
    p=d.split('/'); return(int(p[2]),int(p[0]),int(p[1]))

def merge(existing, new_recs):
    dates={r[0] for r in existing}
    added=0
    for r in new_recs:
        if r[0] in dates:
            for i,e in enumerate(existing):
                if e[0]==r[0]: existing[i]=r; break
        else:
            existing.append(r); added+=1
    existing.sort(key=lambda r:_pd(r[0]))
    return existing, added

def main():
    # Find CSV files (root folder or csv/ subfolder)
    csvs = glob.glob('*.csv') + glob.glob('csv/*.csv')
    if not csvs:
        print("No CSV files found in csv/")
        # Still rebuild HTML from existing data.json
        if not os.path.exists('data.json'):
            print("No data.json either. Nothing to do.")
            return
        with open('data.json','r') as f:
            final = json.load(f)
    else:
        # Read all CSVs and merge
        all_new = []
        for c in sorted(csvs):
            recs = read_csv(c)
            all_new.extend(recs)
            print(f"Read {c}: {len(recs)} records")

        # Load existing
        existing = []
        if os.path.exists('data.json'):
            with open('data.json','r') as f:
                existing = json.load(f)

        if len(all_new) >= 50:
            final = sorted(all_new, key=lambda r:_pd(r[0]))
            print(f"FULL REPLACE: {len(final)} sessions")
        else:
            final, added = merge(existing, all_new)
            print(f"APPEND: +{added} new, total {len(final)} sessions")

        # Save data.json
        with open('data.json','w') as f:
            json.dump(final, f)

    print(f"Data: {final[0][0]} -> {final[-1][0]} ({len(final)} sessions)")

    # Build index.html
    html = HTML.replace('__DATA__', json.dumps(final))
    with open('index.html','w',encoding='utf-8') as f:
        f.write(html)
    print(f"index.html: {os.path.getsize('index.html')//1024}KB")


HTML = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VN Fear & Greed Index</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0d0f13;--panel:#12141a;--border:#1e2028;--grid:#1a1d24;--t1:#e8eaed;--t2:#c8ccd4;--t3:#8a8f98;--t4:#555;--fear:#ff3b30;--warn:#ff9500;--neu:#ffcc00;--greed:#34c759;--xgreed:#30d158;--blue:#5ac8fa;--purple:#bf5af2}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--t2);font-family:'DM Mono','IBM Plex Mono',monospace;height:100vh;overflow:hidden;display:flex;flex-direction:column;padding:8px 10px;gap:6px}
.topbar{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--grid);padding-bottom:5px;flex-wrap:wrap}
.topbar .logo{font-size:13px;font-weight:700;font-family:'Instrument Sans',sans-serif;color:var(--t1);letter-spacing:-.5px}
.tag{font-size:9px;color:var(--t4);background:var(--panel);padding:2px 6px;border-radius:3px;margin-left:8px}
.main{flex:1;display:grid;grid-template-columns:220px 1fr;gap:8px;overflow:hidden}
@media(max-width:700px){.main{grid-template-columns:1fr;overflow:auto}}
.left{display:flex;flex-direction:column;gap:5px;overflow:auto}
.left::-webkit-scrollbar{width:3px}.left::-webkit-scrollbar-thumb{background:#333;border-radius:2px}
.pnl{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:8px 10px}
.pnl .lbl{font-size:8px;color:var(--t4);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:5px}
.right{display:flex;flex-direction:column;gap:6px;overflow:hidden}
.range-btns{display:flex;gap:4px}
.range-btns button{background:transparent;border:1px solid var(--border);color:var(--t4);font-size:9px;padding:2px 10px;border-radius:3px;cursor:pointer;font-family:inherit;transition:all .15s}
.range-btns button:hover{border-color:#444}.range-btns button.on{background:var(--border);color:var(--t1)}
.chart-pnl{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:8px 6px 4px 0;flex:1;display:flex;flex-direction:column}
.chart-pnl .lbl{font-size:8px;color:var(--t4);letter-spacing:1.5px;padding-left:10px;margin-bottom:2px;text-transform:uppercase}
.chart-pnl .wrap{flex:1;position:relative}.chart-pnl canvas{position:absolute;inset:0}
.bar-row{display:flex;align-items:center;gap:5px;margin-bottom:3px}
.bar-row .nm{width:58px;font-size:9px;color:var(--t3)}.bar-row .track{flex:1;height:5px;background:#1c1f26;border-radius:3px;overflow:hidden}
.bar-row .fill{height:100%;border-radius:3px;transition:width .3s}.bar-row .val{width:22px;font-size:11px;font-weight:700;text-align:right}
.bar-row .wt{width:22px;font-size:8px;color:var(--t4);text-align:right}
.dist-row{display:flex;align-items:center;gap:4px;margin-bottom:2px}
.dist-row .nm{width:52px;font-size:8px}.dist-row .track{flex:1;height:4px;background:#1c1f26;border-radius:2px;overflow:hidden}
.dist-row .fill{height:100%;border-radius:2px}.dist-row .val{font-size:8px;color:var(--t4);width:36px;text-align:right}
.ev-row{display:flex;justify-content:space-between;align-items:center;padding:3px 0;cursor:pointer;border-bottom:1px solid var(--grid)}
.ev-row:hover{background:rgba(255,149,0,.05)}
.guide{font-size:8px;color:var(--t4);line-height:1.6}
</style>
</head>
<body>
<div class="topbar">
  <div style="display:flex;align-items:center;gap:10px">
    <div class="logo"><span id="dot">●</span> VN FEAR & GREED</div>
    <span class="tag" id="tagInfo"></span>
  </div>
  <div style="font-size:10px;color:var(--t3)" id="headerMeta"></div>
</div>
<div class="main">
  <div class="left">
    <div class="pnl" style="text-align:center;padding:6px 10px 8px">
      <canvas id="gaugeCanvas" width="200" height="140"></canvas>
      <div id="gaugeMeta" style="font-size:9px;color:var(--t4);margin-top:0"></div>
    </div>
    <div class="pnl"><div class="lbl">Components</div><div id="compBars"></div></div>
    <div class="pnl"><div class="lbl">Distribution</div><div id="distBars"></div></div>
    <div class="pnl" style="flex:1;overflow:auto"><div class="lbl">Key Events</div><div id="evRows"></div></div>
    <div class="pnl guide">
      <span style="color:var(--fear)">■</span> 0–20 Tích lũy &nbsp;
      <span style="color:var(--warn)">■</span> 20–40 Theo dõi &nbsp;
      <span style="color:var(--neu)">■</span> 40–60 Neutral<br>
      <span style="color:var(--greed)">■</span> 60–80 Cảnh giác &nbsp;
      <span style="color:var(--xgreed)">■</span> 80–100 Chốt lời
    </div>
  </div>
  <div class="right">
    <div class="range-btns" id="rangeBtns"></div>
    <div class="chart-pnl" style="flex:3"><div class="lbl">Fear & Greed vs VN-Index</div><div class="wrap"><canvas id="mainChart"></canvas></div></div>
    <div class="chart-pnl" style="flex:2"><div class="lbl">Component Breakdown</div><div class="wrap"><canvas id="compChart"></canvas></div></div>
  </div>
</div>
<script>
const R=__DATA__;
const RAW=R.map(r=>({date:r[0],close:r[1],pct_chg:r[2],rsi:r[3],advance:r[4],decline:r[5],ceiling:r[6],floor:r[7],total_stocks:r[8],above_ma50:r[9],ema_cross:r[10],volume:r[11],parkinson_vol:r[12],vol_ratio:r[13],ad_ratio:r[14],thrust_pct:r[15]}));
const cl=v=>Math.max(0,Math.min(100,v));
function cB(d){const t=d.total_stocks||32;let a=d.ad_ratio<=0?5:d.ad_ratio<1?5+d.ad_ratio*45:50+Math.min((d.ad_ratio-1)/4,1)*45;const fp=(d.floor/t)*100,cp=(d.ceiling/t)*100;let fc=50;if(fp>0)fc=Math.max(0,50-fp*2.5);if(cp>0)fc=Math.min(100,50+cp*2.5);const m=cl((d.above_ma50/t)*100),e=cl((d.ema_cross/t)*100);let th=50;if(d.thrust_pct>5){th=d.decline>d.advance?Math.max(0,50-d.thrust_pct*.55):Math.min(100,50+d.thrust_pct*.55);}return cl(a*.35+fc*.2+m*.2+e*.15+th*.1);}
function cV(d){const vr=d.vol_ratio,pc=d.pct_chg,pv=d.parkinson_vol;let v;if(vr>=1.5)v=pc>=0?cl(60+(vr-1.5)*30):cl(40-(vr-1.5)*30);else if(vr<=.7)v=35+(vr/.7)*10;else v=pc>=0?55+pc*5:45+pc*5;return cl(v-(pv>2?(pv-2)*15:0));}
function cR(r){if(r<=25)return r*.6;if(r<=40)return 15+((r-25)/15)*20;if(r<=60)return 35+((r-40)/20)*30;if(r<=75)return 65+((r-60)/15)*20;return 85+((r-75)/25)*10;}
const D=RAW.map(d=>{const b=cB(d),v=cV(d),r=cR(d.rsi);return{...d,comp:Math.round(cl(b*.5+v*.25+r*.25)),br:Math.round(b),vl:Math.round(v),rs:Math.round(r)};});
const zL=s=>s<=20?"EXTREME FEAR":s<=40?"FEAR":s<=60?"NEUTRAL":s<=80?"GREED":"EXTREME GREED";
const zC=s=>s<=20?"#ff3b30":s<=40?"#ff9500":s<=60?"#ffcc00":s<=80?"#34c759":"#30d158";
let ci=D.length-1,rs=Math.max(0,D.length-120),re=D.length-1,mC,cC;

function drawGauge(val){
  const cv=document.getElementById('gaugeCanvas'),ctx=cv.getContext('2d');
  const w=cv.width,h=cv.height,cx=w/2,cy=h*.48,r=w*.3,sw=w*.04;
  ctx.clearRect(0,0,w,h);
  [[-140,-84,"#ff3b30"],[-84,-28,"#ff9500"],[-28,28,"#ffcc00"],[28,84,"#34c759"],[84,140,"#30d158"]].forEach(([s,e,c])=>{ctx.beginPath();ctx.arc(cx,cy,r,s*Math.PI/180,e*Math.PI/180);ctx.strokeStyle=c;ctx.globalAlpha=.15;ctx.lineWidth=sw;ctx.lineCap='round';ctx.stroke();ctx.globalAlpha=1;});
  const ang=-140+(val/100)*280,c=zC(val);
  ctx.beginPath();ctx.arc(cx,cy,r,-140*Math.PI/180,ang*Math.PI/180);ctx.strokeStyle=c;ctx.lineWidth=sw;ctx.lineCap='round';ctx.stroke();
  const na=ang*Math.PI/180,nl=r*.6;
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+nl*Math.cos(na),cy+nl*Math.sin(na));ctx.strokeStyle=c;ctx.lineWidth=2;ctx.lineCap='round';ctx.stroke();
  ctx.beginPath();ctx.arc(cx,cy,3,0,Math.PI*2);ctx.fillStyle=c;ctx.fill();
  ctx.textAlign='center';ctx.fillStyle=c;
  ctx.font="800 32px 'DM Mono',monospace";ctx.fillText(val,cx,cy+26);
  ctx.font="600 9px 'DM Mono',monospace";ctx.globalAlpha=.7;ctx.fillText(zL(val),cx,cy+42);ctx.globalAlpha=1;
}

function render(){
  const c=D[ci],p=ci>0?D[ci-1]:c,dt=c.comp-p.comp;
  document.getElementById('dot').style.color=zC(c.comp);
  document.getElementById('tagInfo').textContent=`${D.length} sessions`;
  document.getElementById('headerMeta').innerHTML=`${c.date} · <span style="color:${c.pct_chg>=0?'#34c759':'#ff3b30'};font-weight:600">VNI ${c.close} (${c.pct_chg>=0?'+':''}${c.pct_chg}%)</span> <span style="color:#555;margin-left:6px">RSI ${c.rsi}</span>`;
  drawGauge(c.comp);
  document.getElementById('gaugeMeta').innerHTML=`Δ <span style="color:${dt>0?'#34c759':dt<0?'#ff3b30':'#555'};font-weight:600">${dt>0?'+':''}${dt}</span> &nbsp; Prev <span style="color:#8a8f98">${p.comp}</span>`;
  document.getElementById('compBars').innerHTML=[{n:'Breadth',v:c.br,w:'50%',i:'◧'},{n:'Volume',v:c.vl,w:'25%',i:'◨'},{n:'RSI',v:c.rs,w:'25%',i:'◩'}].map(b=>`<div class="bar-row"><span class="nm">${b.i} ${b.n}</span><div class="track"><div class="fill" style="width:${b.v}%;background:linear-gradient(90deg,${zC(b.v)}88,${zC(b.v)})"></div></div><span class="val" style="color:${zC(b.v)}">${b.v}</span><span class="wt">${b.w}</span></div>`).join('');
  updC();
}
function updC(){
  const sl=D.slice(rs,re+1),lb=sl.map(d=>{const t=new Date(d.date);return`${t.getMonth()+1}/${String(t.getFullYear()).slice(2)}`;});
  const tt={backgroundColor:'#16181d',borderColor:'#2a2d35',borderWidth:1,titleColor:'#555',bodyColor:'#c8ccd4',titleFont:{size:9},bodyFont:{size:9},padding:6,cornerRadius:4};
  if(mC)mC.destroy();
  mC=new Chart(document.getElementById('mainChart'),{type:'line',data:{labels:lb,datasets:[
    {label:'F&G',data:sl.map(d=>d.comp),borderColor:'#ff9500',backgroundColor:'rgba(255,149,0,.08)',fill:true,borderWidth:1.5,pointRadius:0,yAxisID:'y',tension:.1},
    {label:'VNI',data:sl.map(d=>d.close),borderColor:'#5ac8fa',borderWidth:1.2,pointRadius:0,yAxisID:'y1',tension:.1}
  ]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},animation:{duration:200},
    plugins:{legend:{display:true,labels:{color:'#555',font:{size:8,family:"'DM Mono'"},boxWidth:10,padding:8}},tooltip:tt},
    scales:{x:{ticks:{color:'#444',font:{size:8},maxTicksLimit:8},grid:{color:'#1a1d24'}},y:{position:'left',min:0,max:100,ticks:{color:'#444',font:{size:8}},grid:{color:'#1a1d24'}},y1:{position:'right',ticks:{color:'#444',font:{size:8}},grid:{display:false}}},
    onClick:(e,els)=>{if(els.length>0){ci=rs+els[0].index;render();}}
  }});
  if(cC)cC.destroy();
  cC=new Chart(document.getElementById('compChart'),{type:'line',data:{labels:lb,datasets:[
    {label:'Breadth',data:sl.map(d=>d.br),borderColor:'#5ac8fa',borderWidth:1.2,pointRadius:0,tension:.1},
    {label:'Volume',data:sl.map(d=>d.vl),borderColor:'#bf5af2',borderWidth:1.2,pointRadius:0,tension:.1},
    {label:'RSI',data:sl.map(d=>d.rs),borderColor:'#30d158',borderWidth:1.2,pointRadius:0,tension:.1}
  ]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},animation:{duration:200},
    plugins:{legend:{display:true,labels:{color:'#555',font:{size:8,family:"'DM Mono'"},boxWidth:10,padding:8}},tooltip:tt},
    scales:{x:{ticks:{color:'#444',font:{size:8},maxTicksLimit:8},grid:{color:'#1a1d24'}},y:{min:0,max:100,ticks:{color:'#444',font:{size:8}},grid:{color:'#1a1d24'}}}
  }});
}
const ranges=[['3M',60],['6M',120],['1Y',252],['2Y',504],['ALL',D.length]];
document.getElementById('rangeBtns').innerHTML=ranges.map(([l,n])=>`<button data-n="${n}">${l}</button>`).join('');
document.getElementById('rangeBtns').addEventListener('click',e=>{if(e.target.tagName!=='BUTTON')return;const n=+e.target.dataset.n;rs=Math.max(0,D.length-n);re=D.length-1;ci=re;document.querySelectorAll('.range-btns button').forEach(b=>b.classList.remove('on'));e.target.classList.add('on');render();});
document.querySelector('.range-btns button:nth-child(2)').classList.add('on');
const dz=[{n:"Ext Fear",lo:0,hi:20,c:"#ff3b30"},{n:"Fear",lo:20,hi:40,c:"#ff9500"},{n:"Neutral",lo:40,hi:60,c:"#ffcc00"},{n:"Greed",lo:60,hi:80,c:"#34c759"},{n:"Ext Greed",lo:80,hi:101,c:"#30d158"}];
document.getElementById('distBars').innerHTML=dz.map(z=>{const ct=D.filter(d=>d.comp>=z.lo&&d.comp<z.hi).length;return`<div class="dist-row"><div class="nm" style="color:${z.c}">${z.n}</div><div class="track"><div class="fill" style="width:${(ct/D.length*100).toFixed(1)}%;background:${z.c}55"></div></div><div class="val">${(ct/D.length*100).toFixed(1)}%</div></div>`;}).join('');
const EVS=[{d:"3/23/2020",l:"COVID-19",c:"#ff3b30"},{d:"1/28/2021",l:"Flash Crash",c:"#ff3b30"},{d:"7/19/2021",l:"Delta",c:"#ff9500"},{d:"1/4/2022",l:"ATH 1525",c:"#34c759"},{d:"11/15/2022",l:"Bear Bottom",c:"#ff3b30"},{d:"4/8/2025",l:"Tariff",c:"#ff3b30"},{d:"7/28/2025",l:"ATH 1557",c:"#34c759"},{d:"3/9/2026",l:"Crash",c:"#ff3b30"}];
document.getElementById('evRows').innerHTML=EVS.map(ev=>{const d=D.find(x=>x.date===ev.d);if(!d)return'';return`<div class="ev-row" data-d="${ev.d}"><div style="display:flex;align-items:center;gap:4px"><span style="width:4px;height:4px;border-radius:2px;background:${ev.c};display:inline-block"></span><span style="font-size:9px;color:#8a8f98">${ev.l}</span></div><span style="font-size:10px;font-weight:700;color:${zC(d.comp)}">${d.comp}</span></div>`;}).join('');
document.getElementById('evRows').addEventListener('click',e=>{const r=e.target.closest('.ev-row');if(!r)return;const d=r.dataset.d,i=D.findIndex(x=>x.date===d);if(i>=0){ci=i;rs=Math.max(0,i-60);re=Math.min(D.length-1,i+60);render();}});
render();
</script>
</body>
</html>'''


if __name__ == '__main__':
    main()
