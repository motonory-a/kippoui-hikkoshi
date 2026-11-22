#!/usr/bin/env python3
"""ナビ子のオフショット写真を 1080x1350 の投稿画像にする（写真が主役、文字は角の小さなカードだけ）
使い方: python3 ig/tool/render_photo.py photo.json ig/wN
photo.json: {"photos":[{"id":"d1a","src":"ig/tool/offshot/ginkgo-walk.png","tag":"11/23 勤労感謝の日","line":"ナビ子のおやすみ","pos":"tl"}]}
pos: tl(左上) / tr(右上) / bl(左下) / br(右下)。顔と体にかからない角を選ぶこと。
"""
import base64, json, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
.p{position:relative;width:1080px;height:1350px;font-family:"Noto Sans CJK JP",sans-serif}
.p img{position:absolute;left:0;top:0;width:1080px;height:1350px;object-fit:cover}
.k{position:absolute;background:rgba(255,255,255,.92);border-radius:22px;padding:14px 22px 16px;box-shadow:0 8px 22px rgba(0,0,0,.18)}
.k .t{display:inline-block;background:#e8742a;color:#fff;font-size:22px;font-weight:800;padding:5px 14px;border-radius:999px;letter-spacing:.04em}
.k .l{font-size:27px;font-weight:800;color:#17375e;margin-top:8px;letter-spacing:.02em}
.k .h{font-size:17px;font-weight:700;color:#7a8394;margin-top:4px}
.tl{left:32px;top:32px}.tr{right:32px;top:32px}.bl{left:32px;bottom:32px}.br{right:32px;bottom:32px}
"""

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1350})
        for ph in spec['photos']:
            b64 = base64.b64encode(open(ph['src'], 'rb').read()).decode()
            card = f'<div class="k {ph.get("pos","tl")}"><span class="t">{ph["tag"]}</span><div class="l">{ph["line"]}</div><div class="h">@kaiun_hikkoshi</div></div>'
            html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="p"><img src="data:image/png;base64,{b64}">{card}</div></body></html>'
            pg.set_content(html); pg.wait_for_timeout(300)
            r = pg.evaluate("()=>{const k=document.querySelector('.k').getBoundingClientRect();return [Math.round(k.left),Math.round(k.top),Math.round(k.right),Math.round(k.bottom)]}")
            print(ph['id'], 'card box', r)
            png = os.path.join(out, ph['id'] + '.png'); pg.screenshot(path=png)
            Image.open(png).convert('RGB').save(os.path.join(out, ph['id'] + '.jpg'), quality=92, optimize=True, progressive=True)
            os.remove(png)
        br.close()
