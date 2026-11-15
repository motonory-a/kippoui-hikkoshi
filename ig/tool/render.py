#!/usr/bin/env python3
"""引越しナビ Instagram 画像 v2（雑誌・チラシ風レイアウト）1080x1350"""
import base64, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
B = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
NAVI = {k: B(os.path.join(HERE, 'navi', k + '.png')) for k in ['n1', 'n2', 'n3', 'n4', 'n5', '02', '04']}
BANNER = B(os.path.join(HERE, '..', '..', 'img', 'og.jpg'))

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden;background:#fbf6ee}
.p{position:relative;width:1080px;height:1350px;font-family:"Noto Sans CJK JP",sans-serif;color:#1b2a41;background:#fbf6ee}
.hd{position:absolute;left:0;top:0;width:1080px;height:660px;overflow:hidden;
 background:radial-gradient(circle at 850px 230px,#fffdf6 0,#fff3d6 150px,rgba(255,226,170,.75) 260px,rgba(255,226,170,0) 430px),linear-gradient(165deg,#e3f2fb 0%,#fdf3e3 52%,#ffe7cf 100%)}
.hd svg{position:absolute;left:0;top:0}
.cat{position:absolute;left:64px;top:64px;display:flex;gap:12px;z-index:5}
.cat span{padding:10px 24px;border-radius:999px;font-size:28px;font-weight:800;letter-spacing:.06em}
.cat .a{background:#e8742a;color:#fff}
.cat .b{background:#fff;color:#17375e;border:2px solid #f3d8b6}
.ttl{position:absolute;left:64px;top:150px;width:600px;font-family:"Noto Serif CJK JP",serif;font-weight:900;color:#17375e;line-height:1.28;letter-spacing:.02em;z-index:4}
.ttl em{font-style:normal;color:#e8742a;background:linear-gradient(transparent 70%,rgba(255,196,107,.6) 70%)}
.navi{position:absolute;z-index:3;-webkit-mask-image:linear-gradient(to bottom,#000 82%,transparent 99%);mask-image:linear-gradient(to bottom,#000 82%,transparent 99%)}
.navi.n{right:40px;top:14px;height:540px;-webkit-mask-image:none;mask-image:none}
.navi.o{right:30px;top:24px;height:600px}
.name{position:absolute;right:30px;top:470px;z-index:6;background:#fff;color:#17375e;font-weight:800;font-size:26px;padding:8px 22px;border-radius:999px;box-shadow:0 6px 16px rgba(0,0,0,.18)}
.name:before{content:"案内役 ";color:#e8742a;font-size:22px}
.card{position:absolute;left:52px;right:52px;top:548px;bottom:132px;z-index:5;background:#fff;border-radius:36px;box-shadow:0 18px 50px rgba(200,120,40,.16);padding:52px 56px;display:flex;flex-direction:column;justify-content:center}
.lead{font-size:40px;line-height:1.75;color:#24324a}
.lead b{color:#d9601a;font-weight:800}
.lead .big{font-size:52px;font-weight:900;color:#17375e;line-height:1.4}
.list{list-style:none}
.list li{display:flex;gap:24px;align-items:center;padding:20px 0;border-bottom:2px dashed #eadfce}
.list li:first-child{padding-top:0}.list li:last-child{border-bottom:0;padding-bottom:0}
.list .no{flex:0 0 auto;width:64px;height:64px;border-radius:18px;background:#17375e;color:#fff;font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center}
.list.r .no{background:#e8742a}
.list h3{font-size:39px;line-height:1.3;color:#17375e;font-weight:900}
.list p{font-size:29px;line-height:1.45;color:#5b6474;margin-top:4px}
.list.big li{padding:30px 0}.list.big h3{font-size:44px}.list.big p{font-size:31px}.list.big .no{width:76px;height:76px;font-size:38px}
.list.tight li{padding:15px 0}
.list.tight h3{font-size:35px}.list.tight p{font-size:27px}
.duo{display:flex;gap:26px}
.duo>div{flex:1;border-radius:28px;padding:34px 10px 30px;text-align:center}
.duo .d{font-family:"Noto Serif CJK JP",serif;font-weight:900;font-size:140px;line-height:1.05}
.duo .t{font-size:36px;font-weight:800;line-height:1.45;color:#17375e;margin-top:14px}
.duo .x{background:#fff1e2}.duo .x .d{color:#e8742a}
.duo .y{background:#eaf1f9}.duo .y .d{color:#17375e}
.warn{margin-top:30px;padding:22px 28px;border-radius:20px;background:#fbf6ee;font-size:30px;line-height:1.6;color:#24324a}
.warn b{color:#d9601a}
.ban{width:100%;border-radius:22px;display:block;box-shadow:0 8px 22px rgba(17,43,75,.2)}
.ft{position:absolute;left:52px;right:52px;bottom:34px;height:70px;display:flex;align-items:center;justify-content:space-between;z-index:6}
.ft .h{font-size:30px;font-weight:800;color:#17375e;letter-spacing:.03em}
.ft .c{background:#e8742a;color:#fff;font-size:28px;font-weight:800;padding:14px 30px;border-radius:999px;box-shadow:0 8px 18px rgba(232,116,42,.35)}
"""

def deco():
    import math
    cx, cy, r = 830, 215, 86
    pts = set()
    # フラワーオブライフ：中心から2周（19円）
    for q in range(-2, 3):
        for rr in range(-2, 3):
            if abs(q) + abs(rr) + abs(-q - rr) <= 4:
                x = cx + r * (q + rr / 2)
                y = cy + r * rr * math.sqrt(3) / 2
                pts.add((round(x, 1), round(y, 1)))
    circ = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y in pts)
    R = r * 3
    clip = f'<clipPath id="fol"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>'
    fol = f'<g clip-path="url(#fol)" fill="none" stroke="#e8742a" stroke-opacity=".32" stroke-width="2.2">{circ}</g>'
    outer = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#e8742a" stroke-opacity=".38" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="{R+14}" fill="none" stroke="#e8742a" stroke-opacity=".2" stroke-width="1.6"/>'
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="{d}" fill="#ffb84d" opacity=".9"/>' for x, y, d in [(110, 520, 3), (560, 90, 2.5), (640, 560, 2), (40, 300, 2), (700, 40, 2)])
    return f'<svg width="1080" height="660" viewBox="0 0 1080 660"><defs>{clip}</defs>{fol}{outer}{dots}</svg>'

DECO = deco()

def page(cat, title, size, body, navi, sub=None, cta='無料で鑑定 ▶ プロフのリンク'):
    kind = 'n' if navi.startswith('n') else 'o'
    b = f'<span class="b">{sub}</span>' if sub else ''
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="p">
<div class="hd">{DECO}</div>
<div class="cat"><span class="a">{cat}</span>{b}</div>
<div class="ttl" style="font-size:{size}px">{title}</div>
<img class="navi {kind}" src="data:image/png;base64,{NAVI[navi]}">
<div class="name">ナビ子</div>
<div class="card">{body}</div>
<div class="ft"><span class="h">@kaiun_hikkoshi</span><span class="c">{cta}</span></div>
</div></body></html>"""

def lst(items, red=False, tight=False, big=False):
    cls = 'list' + (' r' if red else '') + (' tight' if tight else '') + (' big' if big else '')
    return f'<ul class="{cls}">' + ''.join(f'<li><span class="no">{i+1}</span><div><h3>{a}</h3>' + (f'<p>{b}</p>' if b else '') + '</div></li>' for i, (a, b) in enumerate(items)) + '</ul>'

def duo(a, at, b, bt):
    return f'<div class="duo"><div class="x"><div class="d">{a}</div><div class="t">{at}</div></div><div class="y"><div class="d">{b}</div><div class="t">{bt}</div></div></div>'

WARN = '<div class="warn">ただし、あなたに合わない年もあります。<br><b>今年のあなたに合うかは、サイトで確認しましょう。</b></div>'


def body(b):
    t = b['type']
    if t == 'lead':
        return '<p class="lead">' + b['html'] + '</p>'
    if t == 'list':
        return lst([tuple(x) for x in b['items']], red=b.get('red', False), tight=b.get('tight', False), big=b.get('big', False))
    if t == 'duo':
        return duo(b['a'], b['at'], b['b'], b['bt']) + (WARN if b.get('warn', True) else '')
    if t == 'banner':
        return f'<img class="ban" src="data:image/jpeg;base64,{BANNER}"><p class="lead" style="margin-top:34px;font-size:38px">' + b['html'] + '</p>'
    raise ValueError(t)

if __name__ == '__main__':
    import json, sys
    from PIL import Image
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    bad = []
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1350})
        for sl in spec['slides']:
            html = page(sl['cat'], sl['title'], sl.get('size', 68), body(sl['body']), sl.get('navi', 'n1'), sub=sl.get('sub'))
            pg.set_content(html); pg.wait_for_timeout(250)
            r = pg.evaluate("()=>{const c=document.querySelector('.card');return [c.scrollHeight,c.clientHeight,document.querySelector('.ttl').getBoundingClientRect().bottom]}")
            if r[0] > r[1] + 2 or r[2] > 540: bad.append((sl['id'], r))
            png = os.path.join(out, sl['id'] + '.png'); pg.screenshot(path=png)
            Image.open(png).convert('RGB').save(os.path.join(out, sl['id'] + '.jpg'), quality=92, optimize=True, progressive=True)
            os.remove(png)
        br.close()
    print('NG(はみ出し):', bad if bad else 'なし')
