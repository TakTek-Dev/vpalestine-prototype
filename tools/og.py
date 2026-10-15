"""tools/out/og.html -> assets/og.png (1200x630 link preview), via tools/shot.mjs.

python -I tools/og.py && node --experimental-websocket tools/shot.mjs http://127.0.0.1:8161/tools/out/og.html assets/og.png 1200 630 view
The preview is a poster of its own: the film sheet, the music sheet overprinting it, and the wordmark in the key.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../assets/css/vp.css?v={B.V}">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:var(--stock)}}
.og{{position:relative;width:1200px;height:630px}}
.f{{position:absolute;left:0;top:0;width:700px;height:630px;background:var(--film)}}
.m{{position:absolute;left:640px;top:0;right:0;height:630px;background:var(--music);mix-blend-mode:multiply}}
.w{{position:absolute;left:48px;right:48px;bottom:56px}}
.w svg{{width:100%;height:auto;overflow:visible}}
.w .f,.w .m{{position:static;mix-blend-mode:normal}}
.w path.f{{fill:var(--on-film)}}.w path.m{{fill:var(--music)}}.w path.o{{fill:var(--over)}}.w .w{{fill:var(--key)}}
.t{{position:absolute;left:48px;top:44px;font:900 76px/.86 var(--poster);font-stretch:70%;text-transform:uppercase;color:var(--key);width:560px}}
.s{{position:absolute;left:700px;top:50px;width:440px;font:800 30px/1.12 var(--poster);font-stretch:92%;color:var(--on-music)}}
</style></head><body><div class="og"><i class="f"></i><i class="m"></i>
<p class="t">Palestinian film and music</p><p class="s">Followed from premiere to audience. Printed in two screens and a key.</p>
<div class="w">{B.wordmark('og', 'VPalestine')}</div></div></body></html>"""
os.makedirs(os.path.join(ROOT, 'tools', 'out'), exist_ok=True)
open(os.path.join(ROOT, 'tools', 'out', 'og.html'), 'w', encoding='utf-8').write(html)
print('tools/out/og.html')
