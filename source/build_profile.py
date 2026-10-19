from pathlib import Path
import sys,re,base64,html,zipfile,shutil
SOURCE=Path(__file__).resolve().parent
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.varLib.instancer import instantiateVariableFont
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ROOT=Path('/Users/ihsan/Repository/portofolio-web')
OUT=SOURCE.parent
A=OUT/'assets'
INK='#111113';MUTED='#6e6e76';CANVAS='#f3f2ee';ACCENT='#5b4cf5';LAV='#ded8ff';MINT='#cdeedd';PEACH='#ffdcc7';SKY='#d3e7ff'
fonts={}
for family,path,weights in [('sans',str(SOURCE/'fonts/Geist.ttf'),[400,500,600]),('mono',str(SOURCE/'fonts/GeistMono.ttf'),[400])]:
 for weight in weights:
  ft=instantiateVariableFont(TTFont(path),{'wght':weight},inplace=False)
  fonts[(family,weight)]=(ft,ft.getGlyphSet(),ft.getBestCmap(),ft['head'].unitsPerEm)
class SVG:
 def __init__(self,w,h,title):self.w=w;self.h=h;self.title=title;self.parts=[];self.glyphs={};self.defs=[]
 def add(self,v):self.parts.append(v)
 def rect(self,x,y,w,h,fill='white',r=28,stroke=True):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(' stroke="#111113" stroke-opacity=".08"' if stroke else '')+'/>')
 def text(self,s,x,y,size=16,weight=400,fill=INK,track=0,family='sans',extra=''):
  ft,gs,cmap,upm=fonts[(family,weight)];sc=size/upm;start=x;uses=[]
  for ch in s:
   gn=cmap.get(ord(ch),'.notdef');key=(family,weight,gn)
   if key not in self.glyphs:
    pen=SVGPathPen(gs);gs[gn].draw(pen);gid=f'g{len(self.glyphs)}';self.glyphs[key]=gid
    self.defs.append(f'<path id="{gid}" d="{pen.getCommands()}"/>')
   gid=self.glyphs[key]
   uses.append(f'<use xlink:href="#{gid}" transform="translate({x:.3f} {y}) scale({sc:.6f} {-sc:.6f})"/>')
   x+=gs[gn].width*sc+track
  if fill.startswith('url('):
   maskid=f'textmask{len(self.defs)}'
   self.defs.append(f'<mask id="{maskid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{self.w}" height="{self.h}"><g fill="white">'+''.join(uses)+'</g></mask>')
   self.add(f'<rect width="{self.w}" height="{self.h}" fill="{fill}" mask="url(#{maskid})"/>')
  else:self.add(f'<g fill="{fill}" {extra}>'+''.join(uses)+'</g>')
  return x-start
 def label(self,s,x,y,fill=MUTED):return self.text(s.upper(),x,y,11.5,fill=fill,track=.69,family='mono')
 def arrow(self,x,y,color=INK):self.add(f'<path d="M{x} {y+10}l10-10m-9 0h9v9" fill="none" stroke="{color}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>')
 def image(self,path,x,y,w,h):
  path=Path(path)
  if path.suffix==".png" and path.parent.name=="logo":path=(SOURCE/"optimized-logos")/path.name
  if path.suffix=='.svg':
   # Keep the SVG root's fill, stroke and other presentation attributes.
   # Dropping them turns single-color brand icons black in image mode.
   root=ET.parse(path).getroot()
   root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(h))
   root.set('preserveAspectRatio','xMidYMid meet')
   pref=f'asset{len(self.parts)}_'
   body=ET.tostring(root,encoding='unicode')
   for ident in re.findall(r'\bid="([^"]+)"',body):
    body=body.replace(f'id="{ident}"',f'id="{pref}{ident}"').replace(f'url(#{ident})',f'url(#{pref}{ident})')
   self.add(body)
  else:
   mime='image/jpeg' if path.suffix in ['.jpg','.jpeg'] else 'image/png';data=base64.b64encode(path.read_bytes()).decode()
   self.add(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:{mime};base64,{data}"/>')
 def save(self,name,animate=True):
  defs='''<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.2" fill="#111113" opacity=".09"/></pattern>
<pattern id="locationdots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="1.3" fill="#111113" opacity=".15"/></pattern>
<linearGradient id="flow" gradientUnits="userSpaceOnUse" x1="64" y1="0" x2="1136" y2="70"><stop offset="0" stop-color="#5b4cf5"/><stop offset=".28" stop-color="#c04cf5"/><stop offset=".5" stop-color="#f5844c"/><stop offset=".75" stop-color="#c04cf5"/><stop offset="1" stop-color="#5b4cf5"/></linearGradient>
<linearGradient id="mark" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5b4cf5"/><stop offset=".55" stop-color="#c04cf5"/><stop offset="1" stop-color="#f5844c"/></linearGradient>
<radialGradient id="lavenderglow"><stop stop-color="#ded8ff"/><stop offset="1" stop-color="#ded8ff" stop-opacity="0"/></radialGradient><radialGradient id="peachglow"><stop stop-color="#ffdcc7"/><stop offset="1" stop-color="#ffdcc7" stop-opacity="0"/></radialGradient>'''
  css='''<style>@keyframes mesh{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(25px,-18px) scale(1.08)}}@keyframes shadeA{0%,100%{stop-color:#5b4cf5}50%{stop-color:#f5844c}}@keyframes shadeB{0%,100%{stop-color:#f5844c}50%{stop-color:#5b4cf5}}@keyframes ping{0%{r:5;opacity:.5}85%,100%{r:19;opacity:0}}@keyframes locationping{0%{r:8;opacity:.35}100%{r:60;opacity:0}}@keyframes marquee{to{transform:translateX(-50%)}}@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}.mesh{animation:mesh 14s ease-in-out infinite}.mesh2{animation:mesh 14s -5s ease-in-out infinite reverse}#flow stop:first-child,#flow stop:last-child{animation:shadeA 6s ease-in-out infinite}#flow stop:nth-child(3){animation:shadeB 6s ease-in-out infinite}.ping{animation:ping 2.4s cubic-bezier(0,0,.2,1) infinite}.locationping{animation:locationping 3.4s ease-out infinite}.marquee{animation:marquee 32s linear infinite}.reverse{animation-direction:reverse}.entrance{animation:rise 1.2s cubic-bezier(.16,1,.3,1) both}@media(prefers-reduced-motion:reduce){*{animation:none!important}.ping,.locationping{opacity:0}}</style>'''
  s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{html.escape(self.title)}"><title>{html.escape(self.title)}</title><defs>{defs}{"".join(self.defs)}</defs>{css if animate else ""}{"".join(self.parts)}</svg>'
  ET.fromstring(s);(A/name).write_text(s)
 def canvas(self):self.rect(0,0,self.w,self.h,CANVAS,28,False);self.add(f'<rect width="{self.w}" height="{self.h}" rx="28" fill="url(#dots)"/>')
def pill(s,label,x,y,fill='white',color=INK,size=13,padx=14,h=30):
 # Geist advance for pill width.
 ft,gs,cm,upm=fonts[('sans',400)];w=sum(gs[cm.get(ord(c),'.notdef')].width for c in label)*size/upm+padx*2
 s.rect(x,y,w,h,fill,h/2);s.text(label,x+padx,y+h/2+size*.33,size,fill=color);return w

data=(ROOT/'src/data/portfolio.ts').read_text()
groups=[]
for label,body in re.findall(r'label: "(Languages|Frameworks|Styling|Data & Infra)",\s*items: \[(.*?)\]',data,re.S):groups.append((label,re.findall(r'name: "([^"]+)", logo: "([^"]+)"',body)))
tools=[v for _,items in groups for v in items]
# The GitHub hero contains only the two cards selected by the user.
s=SVG(1200,744,'Muhammad Ihsan Wahyudin — Software Engineer. Backend, web and mobile systems. Animated introduction and 30-tool technology marquee.')
s.canvas();s.add('<g class="entrance">')
s.rect(24,24,1152,484)
s.defs.append('<clipPath id="mainclip"><rect x="24" y="24" width="1152" height="484" rx="28"/></clipPath>')
s.add('<g clip-path="url(#mainclip)"><ellipse class="mesh" cx="1080" cy="15" rx="435" ry="350" fill="url(#lavenderglow)"/><ellipse class="mesh2" cx="870" cy="540" rx="480" ry="250" fill="url(#peachglow)"/></g>')
s.add('<circle cx="88" cy="82" r="27" fill="white" stroke="url(#mark)" stroke-width="2"/><g transform="translate(76 70)" fill="none" stroke="url(#mark)" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></g>')
s.text('Muhammad Ihsan Wahyudin',132,78,24,500,track=-.6)
s.label('Software Engineer · Backend & Full-Stack',132,102)
# Exact Geist outlines with the original 600 weight, tight tracking and ink ampersand.
s.text('Crafting software solutions',64,203,72,600,INK,-3.24)
x=64+s.text('in ',64,273,72,600,INK,-3.24)
x+=s.text('backend services, web',x,273,72,600,'url(#flow)',-3.24)
x=64+s.text('& ',64,343,72,600,INK,-3.24)
x+=s.text('mobile',x,343,72,600,'url(#flow)',-3.24)
s.text(' systems.',x,343,72,600,INK,-3.24)
s.text('Experienced in building ERP, Supplier Portals, HRIS & E-Commerce Platforms.',64,397,20,fill=MUTED)
s.rect(64,432,167,44,INK,22,False);s.text('Get in touch',84,459,15,500,'white');s.arrow(202,448,'white')
s.rect(239,432,127,44,'white',22);s.text('View work',260,459,15,500)
# Smooth, clipped, counter-scrolling tracks with preserved brand colors.
s.rect(24,524,1152,196);s.label('Tech stack',56,562);s.label('30 tools',1070,562)
s.defs.append('<clipPath id="marqueeclip"><rect x="25" y="578" width="1150" height="126" rx="12"/></clipPath><linearGradient id="fade"><stop stop-color="white" stop-opacity="0"/><stop offset=".05" stop-color="white"/><stop offset=".95" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient><mask id="techfade" maskUnits="userSpaceOnUse" x="24" y="578" width="1152" height="126"><rect x="24" y="578" width="1152" height="126" fill="url(#fade)"/></mask>')
for row,items in enumerate([tools[:15],list(reversed(tools[15:]))]):
 widths=[];ft,gs,cm,upm=fonts[('sans',400)]
 for name,logo in items:widths.append(sum(gs[cm.get(ord(c),'.notdef')].width for c in name)*16/upm+64)
 total=sum(widths)+10*len(widths)
 # Use the exact track width to avoid a jump at the loop boundary.
 s.defs.append(f'<style>@keyframes track{row}{{from{{transform:translateX(0)}}to{{transform:translateX(-{total:.3f}px)}}}}</style>')
 s.add('<g clip-path="url(#marqueeclip)" mask="url(#techfade)">')
 s.add(f'<g class="marquee {"reverse" if row else ""}" style="animation-name:track{row}">')
 for copy in range(2):
  x=40+copy*total;y=586+row*57
  for (name,logo),w in zip(items,widths):
   s.rect(x,y,w,42,'#f8f7f4',21);s.add(f'<circle cx="{x+23}" cy="{y+21}" r="15" fill="white"/>')
   s.image(ROOT/'public/images/logo'/logo,x+12,y+10,22,22)
   s.text(name,x+47,y+27,16);x+=w+10
 s.add('</g></g>')
s.add('</g>');s.save('hero.svg');s.save('hero-static.svg',False)
# Adjacent thirds span the hero width exactly. Transparent SVG insets provide
# equal 12-unit gaps without adding whitespace to the README image row.
for index,(name,label,sub) in enumerate([('portfolio','Portfolio','ihsan.my.id'),('linkedin','LinkedIn',"Let’s connect"),('email','Email','Say hello')]):
 s=SVG(400,88,label+' — '+sub);s.add(f'<g transform="translate({index*4} 0)">');s.rect(0,0,392,88,'white',24);s.label(label,24,31);s.text(sub,24,62,22,500,track=-.5);s.add('<circle cx="350" cy="44" r="18" fill="#111113"/>');s.arrow(345,39,'white');s.add('</g>');s.save(name+'.svg')
# README uses the same assets for the complete composition, with real links kept outside image-only cards.
(OUT/'README.md').write_text('''<a href="https://www.ihsan.my.id"><img src="./assets/hero.svg" width="100%" alt="Muhammad Ihsan Wahyudin — Software Engineer · Backend & Full-Stack. Backend, web and mobile systems. Animated tech stack." /></a>

<p align="center">
<a href="https://www.ihsan.my.id"><img src="./assets/portfolio.svg" width="33.333333%" alt="Visit my portfolio" /></a><a href="https://www.linkedin.com/in/muhammad-ihsan-wahyudin-1a4a19209"><img src="./assets/linkedin.svg" width="33.333333%" alt="Connect on LinkedIn" /></a><a href="mailto:m.ihsanwahyudin@gmail.com"><img src="./assets/email.svg" width="33.333333%" alt="Send me an email" /></a>
</p>
''')
(OUT/'INSTALL.md').write_text('''# GitHub profile — portfolio design edition

## Pasang

1. Buka repository publik ihsanwahyudin/ihsanwahyudin.
2. Ganti README.md dan seluruh folder assets/ dengan isi paket ini. Commit perubahan.
3. Buka profil GitHub. Banner animasi tetap memakai path assets/hero.svg.

## Desain yang disamakan

Acuan: src/components/sections/Hero.tsx, src/styles/globals.css, src/components/ui/CodeMark.tsx dan src/data/portfolio.ts dari /Users/ihsan/Repository/portofolio-web, 19 Oktober 2026.

- Font Geist dan Geist Mono; outline vektor menjaga bentuk huruf tanpa unduhan font saat profil dibuka.
- Warna persis: canvas #f3f2ee, ink #111113, accent #5b4cf5, lavender #ded8ff, mint #cdeedd, peach #ffdcc7, sky #d3e7ff.
- Hero memakai dua kartu pilihan: perkenalan dan tech stack. Keduanya selebar profil, dengan radius 28 dan marquee dua arah.
- Logo dan screenshot proyek asli dari folder public/ website; tidak memakai screenshot atau data contoh buatan.
- Gradasi bergerak, glow lavender/peach, dan marquee CSS dua arah; menghormati prefers-reduced-motion.
- Tidak bergantung pada server gambar untuk aset desain. Semua gambar yang ditampilkan disimpan dalam repository.

## Batas tampilan GitHub

SVG di README adalah gambar. Kontrol di dalam banner merupakan bagian gambar, bukan tombol HTML terpisah. Seluruh banner membuka portfolio; tiga kartu kontak di bawah banner memiliki tautan masing-masing. Hover 3D, navigasi scroll, dan jam lokal real-time website tidak berjalan di gambar GitHub. Hero hanya memuat perkenalan dan tech stack. Logo SVG mempertahankan atribut fill dan stroke asli. Ikon kode memakai tiga path terpisah seperti CodeMark.tsx.

hero-static.svg menyediakan versi tanpa animasi. Untuk memakainya, ubah src banner pada README menjadi ./assets/hero-static.svg.

## Kredit

Font: Geist / Geist Mono (SIL Open Font License), https://github.com/google/fonts/tree/main/ofl/geist dan https://github.com/google/fonts/tree/main/ofl/geistmono. Lisensi disertakan di folder licenses/.
CodeMark dan ikon antarmuka diadaptasi dari komponen website. Lucide code-xml memakai lisensi ISC.
''')
# Preview HTML uses exactly the same SVG image references as README.
(OUT/'preview.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ihsan · GitHub profile preview</title><style>*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#c9d1d9;font:14px Arial,sans-serif}main{max-width:1012px;margin:32px auto;padding:28px;border:1px solid #30363d;border-radius:12px}img{width:100%;display:block}.links{margin:16px 0;line-height:0}.links a{display:inline}.links img{display:inline-block;vertical-align:top;width:33.333333%}.projects{display:flex;gap:12px}.projects a{width:50%}section{margin-top:24px}p{text-align:center;margin:24px}a{color:#a399ff}small{display:block;color:#8b949e;margin-bottom:24px} @media(max-width:650px){main{padding:12px;margin:0;border:none}}</style><main><small>README.md · Preview</small><a href="https://www.ihsan.my.id"><img src="assets/hero.svg" alt="Ihsan profile"/></a><div class="links"><a href="https://www.ihsan.my.id"><img src="assets/portfolio.svg" alt="Portfolio"/></a><a href="https://www.linkedin.com/in/muhammad-ihsan-wahyudin-1a4a19209"><img src="assets/linkedin.svg" alt="LinkedIn"/></a><a href="mailto:m.ihsanwahyudin@gmail.com"><img src="assets/email.svg" alt="Email"/></a></div></main></html>''')
print('Rebuilt',len(list(A.glob('*.svg'))),'SVG assets with original Geist outlines, colors, real logos and project screenshots.')
