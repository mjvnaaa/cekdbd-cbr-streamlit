"""Tema visual CekDBD untuk Streamlit.

Modul ini HANYA mengurus tampilan: CSS global, ikon SVG (Lucide), dan helper
HTML kecil. Tidak ada logika diagnosis di sini.

Desain mengikuti aplikasi referensi (``css/style.css`` pada proyek HTML):
palet biru-teal, font Inter, navbar pil melayang, kartu bersudut besar, tile
gejala, dan lembar laporan.
"""

import html as _html
import re

import streamlit as st

# ---------------------------------------------------------------------------
# Ikon (Lucide) - path disalin dari js/app.js proyek referensi
# ---------------------------------------------------------------------------
IKON = {
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "clipboard-list": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
    "user-round": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "calculator": '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M16 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/><path d="M16 18h.01"/>',
}


def ikon(nama, ukuran=20):
    """SVG inline untuk dipakai di dalam HTML."""

    return (
        f'<svg class="ic" width="{ukuran}" height="{ukuran}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{IKON[nama]}</svg>'
    )


def _uri_svg(nama, warna):
    """Data-URI SVG untuk dipakai di CSS (background / mask)."""

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        f'stroke="{warna}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{IKON[nama]}</svg>'
    )
    return "url(\"data:image/svg+xml;utf8," + svg.replace("#", "%23").replace('"', "'") + '")'


def esc(teks):
    return _html.escape(str(teks), quote=True)


def html(konten):
    """Render HTML. Indentasi/baris baru dibuang agar tidak dibaca sebagai blok kode Markdown."""

    st.markdown(re.sub(r"\n\s*", " ", konten).strip(), unsafe_allow_html=True)


def galat(pesan):
    """Pesan kesalahan form bergaya referensi (teks merah, bukan kotak Streamlit)."""

    html(f'<p class="err" role="alert">{esc(pesan)}</p>')


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --deep-twilight:#03045E;--bright-teal-blue:#0077B6;--turquoise-surf:#00B4D8;
  --frosted-blue:#90E0EF;--light-cyan:#CAF0F8;--white:#fff;--bg:#F3FBFD;
  --ink:#0E1A3D;--mute:#4E6182;--line:#C6E6F0;--err:#C0362C;
  --font:Inter,"Plus Jakarta Sans",system-ui,"Segoe UI",Arial,sans-serif;
}

/* ---------- kerangka Streamlit ---------- */
.stApp{background:var(--bg);color:var(--ink)}
.stApp, .stApp div, .stApp p, .stApp label, .stApp button, .stApp input,
.stApp summary, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp table,
.stApp th, .stApp td, .stApp li, .stApp small, .stApp b{font-family:var(--font)}
[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],
[data-testid="stToolbar"],[data-testid="stDecoration"],footer{display:none!important}
[data-testid="stMainBlockContainer"]{max-width:1080px;padding:0 18px 0!important;margin:0 auto}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]{gap:0}
.stApp p{margin:0}
.stApp h1,.stApp h2,.stApp h3{color:var(--deep-twilight);margin:0;padding:0;line-height:1.15;letter-spacing:-.03em;font-weight:800}
.ic{flex:none;vertical-align:middle}
.mute{color:var(--mute)}

/* ---------- navbar pil melayang ---------- */
[data-testid="stLayoutWrapper"]:has(> .st-key-nav),
[data-testid="stElementContainer"]:has(> .st-key-nav),
.st-key-nav{position:sticky;top:0;z-index:60}
.st-key-nav{background:var(--bg);padding:12px 0 10px;box-shadow:0 0 0 100vmax var(--bg);clip-path:inset(0 -100vmax -14px -100vmax)}
.st-key-nav::after{content:"";position:absolute;left:0;right:0;top:100%;height:14px;background:linear-gradient(var(--bg),rgba(243,251,253,0));pointer-events:none}
.st-key-nav > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
.st-key-nav > [data-testid="stHorizontalBlock"]{
  max-width:720px;margin:0 auto;display:flex!important;flex-wrap:nowrap!important;align-items:center;gap:2px!important;
  background:var(--deep-twilight);border-radius:999px;padding:7px 7px 7px 20px;box-shadow:0 10px 30px rgba(3,4,94,.22)}
.st-key-nav [data-testid="stColumn"]{flex:0 0 auto!important;width:auto!important;min-width:0!important}
.st-key-nav [data-testid="stColumn"]:first-child{margin-right:auto}
.st-key-nav [data-testid="stElementContainer"]{width:auto!important}
.st-key-nav [data-testid="stVerticalBlock"],.st-key-nav [data-testid="stMarkdownContainer"]{gap:0!important;margin:0!important;line-height:1}
.brand{display:flex;align-items:center;gap:8px;color:#fff;font-weight:800;letter-spacing:-.02em;font-size:1rem;white-space:nowrap}
.brand .ic{color:var(--turquoise-surf)}
.st-key-nav button[data-testid^="stBaseButton"]{
  background:transparent!important;color:var(--light-cyan)!important;box-shadow:none!important;
  min-height:0!important;line-height:1.6!important;padding:8px 14px!important;font-size:.88rem;font-weight:600;transform:none!important;transition:background .15s}
.st-key-nav button[data-testid^="stBaseButton"]:hover{background:rgba(144,224,239,.2)!important}

/* ---------- tombol ---------- */
.stApp button[data-testid^="stBaseButton"]{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;line-height:1.25;white-space:nowrap;
  padding:12px 22px;border:0;border-radius:999px;font:600 .95rem var(--font);cursor:pointer;transition:transform .15s,background .15s}
.stApp button[data-testid^="stBaseButton"] p{color:inherit;font:inherit;margin:0}
.stApp button[data-testid^="stBaseButton"] > div{display:flex;align-items:center;justify-content:center}
.stApp button[data-testid^="stBaseButton"] > div > span{display:flex;align-items:center;justify-content:center;gap:8px;flex-direction:row-reverse}
.stApp button[data-testid^="stBaseButton"] [data-testid="stIconMaterial"]{font-size:1.15rem;color:inherit}
.stApp button[kind="primary"],.stApp button[kind="primaryFormSubmit"]{background:var(--bright-teal-blue);color:#fff}
.stApp button[kind="primary"]:hover,.stApp button[kind="primaryFormSubmit"]:hover{background:var(--deep-twilight);color:#fff;transform:translateY(-2px)}
.stApp button[kind="secondary"],.stApp button[kind="secondaryFormSubmit"]{background:transparent;color:var(--bright-teal-blue);box-shadow:inset 0 0 0 1.5px var(--frosted-blue)}
.stApp button[kind="secondary"]:hover,.stApp button[kind="secondaryFormSubmit"]:hover{background:var(--light-cyan);color:var(--deep-twilight);transform:translateY(-2px)}
.stApp button[data-testid^="stBaseButton"]:focus-visible{outline:3px solid var(--turquoise-surf);outline-offset:2px}
.stApp button[data-testid^="stBaseButton"]:focus:not(:focus-visible){box-shadow:inherit}

/* ---------- beranda: hero ---------- */
.st-key-hero{
  background:linear-gradient(120deg,var(--deep-twilight) 0%,var(--bright-teal-blue) 68%,var(--turquoise-surf) 135%);
  color:#fff;border-radius:32px;padding:56px 48px;overflow:hidden;margin-top:20px}
.st-key-hero > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
.st-key-hero > [data-testid="stHorizontalBlock"]{align-items:center;gap:30px}
.stApp .st-key-hero h1{color:#fff;font-size:clamp(1.9rem,6vw,3rem);margin:16px 0 14px}
.lead{color:var(--light-cyan);max-width:34em;font-size:1.05rem;line-height:1.6}
.pill{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:99px;background:rgba(144,224,239,.2);color:var(--light-cyan);font-size:.8rem;font-weight:600}
.st-key-cta > [data-testid="stHorizontalBlock"],.st-key-cta{gap:10px}
.st-key-cta{display:flex!important;flex-direction:row!important;flex-wrap:wrap;margin-top:24px}
.st-key-cta [data-testid="stElementContainer"]{width:auto!important}
.st-key-hero_start button{background:#fff!important;color:var(--deep-twilight)!important;box-shadow:none!important}
.st-key-hero_start button:hover{background:var(--frosted-blue)!important}
.st-key-hero_data button{background:transparent!important;color:#fff!important;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.5)!important}
.st-key-hero_data button:hover{background:rgba(255,255,255,.14)!important}
.fan{--s:1;position:relative;height:250px;width:100%;max-width:380px;margin:0 auto;transform:scale(var(--s));transform-origin:50% 100%}
.fan div{--x:0px;--a:0deg;position:absolute;bottom:0;left:50%;width:118px;height:168px;margin-left:-59px;border-radius:22px;padding:14px;display:flex;flex-direction:column;justify-content:space-between;
  transform-origin:50% 130%;transform:translateX(var(--x)) rotate(var(--a));transition:transform .4s cubic-bezier(.2,.8,.2,1);box-shadow:0 14px 28px rgba(3,4,94,.28)}
.fan b{font-size:2.6rem;font-weight:800;line-height:1}.fan small{font-weight:600;font-size:.75rem;opacity:.8}
.fan div:nth-child(1){--x:-118px;--a:-14deg;background:var(--light-cyan);color:var(--deep-twilight)}
.fan div:nth-child(2){--x:-40px;--a:-5deg;background:var(--frosted-blue);color:var(--deep-twilight)}
.fan div:nth-child(3){--x:40px;--a:5deg;background:var(--turquoise-surf);color:var(--deep-twilight)}
.fan div:nth-child(4){--x:118px;--a:14deg;background:#fff;color:var(--deep-twilight)}
.fan:hover div:nth-child(1){--x:-150px;--a:-19deg}.fan:hover div:nth-child(2){--x:-52px;--a:-7deg}
.fan:hover div:nth-child(3){--x:52px;--a:7deg}.fan:hover div:nth-child(4){--x:150px;--a:19deg}

.blok{padding-top:44px}
.stApp .blok h2{font-size:1.5rem}
.g3{display:grid;gap:14px;grid-template-columns:repeat(3,1fr)}
.st-card{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:22px;transition:border-color .2s,transform .2s}
.st-card:hover{border-color:var(--turquoise-surf);transform:translateY(-3px)}
.stt{display:flex;justify-content:space-between;align-items:center;margin-bottom:22px;color:var(--bright-teal-blue)}
.stt small{font-weight:700;color:var(--mute);font-size:.8rem}
.stApp .st-card h3{font-size:1.2rem;margin-bottom:6px}
.st-card p{color:var(--mute);font-size:.95rem}
.metode{display:grid;gap:24px;align-items:center;background:var(--light-cyan);border-radius:28px;padding:34px;grid-template-columns:1fr 1fr}
.bits{display:grid;grid-template-columns:repeat(14,1fr);gap:4px}
.bits i{aspect-ratio:1;border-radius:7px;background:#fff;opacity:.7}
.bits i.on{background:var(--bright-teal-blue);opacity:1}

/* ---------- kartu, form, split ---------- */
[class*="st-key-card"]{background:#fff;border:1.5px solid var(--line);border-radius:28px;padding:24px;gap:0!important}
.page-top{height:34px}
.page-bot{height:48px}
.stApp .card-h h2{font-size:1.5rem}
.stApp .card-h p{margin-top:4px;color:var(--mute)}
.stApp .jd{font-size:clamp(1.8rem,5vw,2.6rem)}
[class*="st-key-split_"] > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
[class*="st-key-split_"] > [data-testid="stHorizontalBlock"]{gap:16px;align-items:flex-start}
@media (min-width:900px){
.st-key-split_gejala [data-testid="stColumn"]:nth-child(2){order:-1}
.st-key-split_gejala [data-testid="stColumn"]:nth-child(2){flex:0 0 300px!important;width:300px!important}
.st-key-split_gejala [data-testid="stColumn"]:nth-child(1){flex:1 1 0!important;width:auto!important;min-width:0}
.st-key-split_ident [data-testid="stColumn"]:nth-child(1){flex:0 0 300px!important;width:300px!important}
.st-key-split_ident [data-testid="stColumn"]:nth-child(2){flex:1 1 0!important;width:auto!important;min-width:0}
}
.side-h{margin-bottom:6px}
.stApp .side-h h3{font-size:1rem;letter-spacing:-.01em}
.vs{list-style:none;margin:14px 0 0;padding:0}
.vs li{position:relative;display:flex;align-items:center;gap:12px;padding:9px 0}
.vs li:not(:last-child)::after{content:"";position:absolute;left:14px;top:40px;height:calc(100% - 22px);width:2px;background:var(--frosted-blue)}
.vs li.done:not(:last-child)::after{background:var(--turquoise-surf)}
.dt{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:var(--light-cyan);color:var(--bright-teal-blue);font-weight:700;font-size:.85rem;position:relative;z-index:1}
.vs b{display:block;font-size:.92rem;color:var(--deep-twilight);line-height:1.2}
.vs small{color:var(--mute);font-size:.78rem}
.vs li.done .dt{background:var(--turquoise-surf);color:#fff}
.vs li.now .dt{background:var(--bright-teal-blue);color:#fff;box-shadow:0 0 0 4px var(--frosted-blue)}

/* form: label, input, segmented */
[data-testid="stForm"]{border:0!important;padding:0!important;background:transparent!important}
[data-testid="stForm"] > [data-testid="stVerticalBlock"]{gap:18px}
[data-testid="stWidgetLabel"] p{font-weight:600;font-size:.88rem;color:var(--deep-twilight);margin-bottom:0}
[data-testid="stWidgetLabel"]{margin-bottom:8px;min-height:0}
[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"]{
  background:#fff;border:1.5px solid var(--line)!important;border-radius:14px!important;overflow:hidden;transition:border-color .15s,box-shadow .15s}
[data-testid="stTextInputRootElement"]:focus-within,[data-testid="stNumberInputContainer"]:focus-within{border-color:var(--bright-teal-blue)!important;box-shadow:0 0 0 4px rgba(0,180,216,.22)!important}
[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"]{min-height:54px;align-items:center}
[data-testid="stTextInputRootElement"] input,[data-testid="stNumberInputContainer"] input{padding:15px 16px;font:inherit;font-size:1rem;color:var(--ink);background:#fff}
[data-testid="stTextInputRootElement"] input::placeholder{color:#8EA0BD}
[data-testid="stNumberInputContainer"] button{background:#fff;color:var(--mute);border:0;border-left:1px solid var(--line)!important;min-height:0;border-radius:0}
[data-testid="stNumberInputContainer"] button:hover{background:var(--light-cyan);color:var(--deep-twilight)}
[data-testid="stElementContainer"]:has(> [data-testid="stRadio"]),[data-testid="stRadio"]{width:100%!important}
[data-testid="stRadioGroup"]{display:grid!important;grid-template-columns:1fr 1fr;gap:0!important;width:100%;border:1.5px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
[data-testid="stRadioGroup"] > div{margin:0!important;width:100%}
[data-testid="stRadioOption"]{display:flex!important;justify-content:center;width:100%;margin:0!important;padding:12px 6px;cursor:pointer;text-align:center;transition:background .15s}
[data-testid="stRadioOption"] > div{justify-content:center}
[data-testid="stRadioOption"] > div > div:first-child{display:none!important}
[data-testid="stRadioOption"] p{color:var(--mute)!important;font-weight:600;font-size:1rem}
[data-testid="stRadioOption"]:has(input:checked){background:var(--bright-teal-blue)}
[data-testid="stRadioOption"]:has(input:checked) p{color:#fff!important}
[data-testid="stRadioOption"]:has(input:focus-visible){box-shadow:inset 0 0 0 3px var(--turquoise-surf)}
.err{color:var(--err);font-size:.9rem;min-height:1.4em;margin:12px 0 4px}
.st-key-submit_row{margin-top:8px}

/* ---------- gejala: tile ---------- */
.stApp .gh{margin:26px 0 0;padding:0 0 14px!important;color:var(--bright-teal-blue);font-size:1rem;line-height:1.2;letter-spacing:-.01em}
.stApp .gh .mute{font-weight:500;font-size:1rem}
.st-key-tiles_keluhan,.st-key-tiles_lab{margin-top:16px!important;display:grid!important;grid-template-columns:repeat(3,1fr);gap:10px!important}
.st-key-tiles_keluhan [data-testid="stElementContainer"],.st-key-tiles_lab [data-testid="stElementContainer"]{width:100%!important}
[class*="st-key-gejala_"] [data-testid="stCheckbox"]{width:100%}
[class*="st-key-gejala_"] label{
  position:relative;display:flex!important;flex-direction:column;align-items:flex-start;justify-content:space-between;gap:16px;
  width:100%;min-height:98px;margin:0;padding:14px;background:#fff;border:1.5px solid var(--line);border-radius:20px;cursor:pointer;
  transition:background .15s,border-color .15s,transform .15s}
[class*="st-key-gejala_"] label:hover{border-color:var(--turquoise-surf);transform:translateY(-2px)}
[class*="st-key-gejala_"] label > div:not([data-testid="stWidgetLabel"]){display:none!important}
[class*="st-key-gejala_"] label::before{
  align-self:flex-start;font-size:.72rem;font-weight:700;line-height:1.5;padding:2px 9px;border-radius:99px;background:var(--light-cyan);color:var(--bright-teal-blue)}
[class*="st-key-gejala_"] label::after{
  content:"";position:absolute;top:12px;right:12px;width:22px;height:22px;border-radius:50%;border:2px solid var(--frosted-blue);box-sizing:border-box;transition:all .15s}
[class*="st-key-gejala_"] [data-testid="stWidgetLabel"]{margin:0;visibility:visible!important}
[class*="st-key-gejala_"] [data-testid="stWidgetLabel"] p{font-weight:600;font-size:1rem;line-height:1.25;color:var(--ink)}
[class*="st-key-gejala_"] label:has(input:checked){background:var(--bright-teal-blue);border-color:var(--bright-teal-blue)}
[class*="st-key-gejala_"] label:has(input:checked) p{color:#fff}
[class*="st-key-gejala_"] label:has(input:checked)::before{background:rgba(255,255,255,.22);color:#fff}
[class*="st-key-gejala_"] label:has(input:checked)::after{
  background-color:var(--turquoise-surf);border-color:var(--turquoise-surf);
  background-image:CHECK_URI;background-repeat:no-repeat;background-position:center;background-size:13px}
[class*="st-key-gejala_"] label:has(input:focus-visible){outline:3px solid var(--turquoise-surf);outline-offset:2px}

.meter{margin:18px 0 6px;padding:16px;border-radius:20px;background:var(--light-cyan)}
.mn b{font-size:2.4rem;font-weight:800;color:var(--deep-twilight);line-height:1}
.mn span{margin-left:6px;color:var(--mute);font-size:.9rem}
.mn em{font-style:normal}
.prog{height:8px;margin-top:10px;border-radius:99px;background:#fff;overflow:hidden}
.prog i{display:block;height:100%;background:var(--turquoise-surf);border-radius:99px;transition:width .3s}
.st-key-side_actions{margin-top:14px;gap:8px!important}
.st-key-side_actions [data-testid="stElementContainer"],.st-key-side_actions .stButton{width:100%!important}
.st-key-side_actions button{width:100%}

/* ---------- hasil: lembar laporan ---------- */
.st-key-wrap920{max-width:884px;margin:0 auto;width:100%;gap:0!important}
.sheet{background:#fff;border:1.5px solid var(--line);border-radius:28px;overflow:hidden}
.sh-top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px;padding:14px 24px;background:var(--light-cyan);color:var(--deep-twilight);font-size:.85rem}
.sh-top .ic{margin-right:6px}
.sh-main{display:grid;gap:22px;padding:28px 24px;grid-template-columns:1fr auto;align-items:end}
.stApp .lbl{font-size:.82rem;font-weight:600;color:var(--mute);margin-bottom:6px}
.big{font-size:clamp(3.2rem,13vw,5.4rem);font-weight:800;letter-spacing:-.045em;color:var(--deep-twilight);line-height:1}
.pct{font-size:clamp(2.2rem,8vw,3.2rem);font-weight:800;letter-spacing:-.04em;color:var(--bright-teal-blue);line-height:1}
.scale{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:20px;max-width:420px}
.scale div{position:relative;padding:11px 4px;border-radius:12px;background:var(--light-cyan);color:var(--bright-teal-blue);text-align:center;font-weight:800}
.scale .on{background:var(--deep-twilight);color:#fff}
.scale .on::after{content:"";position:absolute;bottom:-7px;left:50%;margin-left:-7px;border:7px solid transparent;border-top-color:var(--deep-twilight);border-bottom:0}
.sh-body{border-top:1.5px dashed var(--line);display:grid;grid-template-columns:1fr 1fr}
.sh-body .blk+.blk{border-left:1.5px dashed var(--line)}
.blk{padding:22px 24px}.blk h3{margin-bottom:12px;font-size:1rem;letter-spacing:-.01em}
.blk.top{border-top:1.5px dashed var(--line)}
dl{display:grid;grid-template-columns:max-content 1fr;gap:8px 20px;margin:0}
dt{color:var(--mute)}dd{margin:0;font-weight:600}
.tag{display:inline-block;padding:5px 13px;margin:0 6px 8px 0;border-radius:99px;background:var(--light-cyan);color:var(--deep-twilight);font-size:.88rem;font-weight:600}
.chart{display:flex;align-items:flex-end;gap:12px;height:190px}
.col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;gap:8px}
.area{flex:1;width:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:6px}
.col .v{font-size:.82rem;font-weight:700;color:var(--deep-twilight)}
.col .b{width:100%;max-width:70px;height:var(--h);border-radius:14px 14px 4px 4px;background:var(--frosted-blue);animation:grow 1s cubic-bezier(.2,.8,.2,1)}
.col.top .b{background:linear-gradient(0deg,var(--bright-teal-blue),var(--turquoise-surf))}
.col small{font-weight:700;color:var(--mute);font-size:.78rem}.col.top small{color:var(--bright-teal-blue)}
@keyframes grow{from{height:0}}
.note{display:flex;gap:10px;align-items:flex-start;margin-top:16px;padding:14px 16px;border-radius:18px;background:var(--light-cyan);color:var(--deep-twilight);font-size:.9rem}
.note .ic{color:var(--bright-teal-blue);margin-top:2px}

/* expander gaya <details> referensi */
[data-testid="stExpander"]{margin-top:16px;background:#fff;border:1.5px solid var(--line)!important;border-radius:24px!important;overflow:hidden}
[data-testid="stExpander"] details{border:0!important;background:transparent}
[data-testid="stExpander"] summary{display:flex;align-items:center;gap:10px;padding:16px 22px;cursor:pointer;font-weight:700;color:var(--deep-twilight);list-style:none}
[data-testid="stExpander"] summary:hover{background:#F1FBFD}
[data-testid="stExpander"] summary [data-testid="stIconMaterial"]{display:none!important}
[data-testid="stExpander"] summary p{font-weight:700;color:var(--deep-twilight);font-size:1rem}
[data-testid="stExpander"] summary::after{content:"";margin-left:auto;width:20px;height:20px;flex:none;transition:transform .2s;
  background:CHEVRON_URI no-repeat center/20px}
[data-testid="stExpander"] details[open] > summary::after{transform:rotate(180deg)}
[data-testid="stExpanderDetails"]{padding:0 22px 22px!important}
[data-testid="stExpanderDetails"] h4{font-size:1rem;letter-spacing:-.01em;margin:20px 0 10px}
[data-testid="stExpanderDetails"] code{background:var(--light-cyan);color:var(--deep-twilight);border-radius:8px}
[data-testid="stExpanderDetails"] pre{background:var(--light-cyan)!important;border-radius:14px}

/* tabel (markdown + HTML) */
.scroll{overflow-x:auto}
[data-testid="stMarkdownContainer"] table,.tbl{width:100%;border-collapse:collapse;font-size:.92rem;border:0}
[data-testid="stMarkdownContainer"] th,[data-testid="stMarkdownContainer"] td,.tbl th,.tbl td{padding:11px 14px;border:0;border-bottom:1px solid var(--line);text-align:center;color:var(--ink)}
[data-testid="stMarkdownContainer"] th,.tbl th{background:var(--light-cyan);color:var(--deep-twilight);font-weight:700;white-space:nowrap}
[data-testid="stMarkdownContainer"] th:first-child,.tbl th:first-child{border-radius:14px 0 0 14px;text-align:left}
[data-testid="stMarkdownContainer"] th:last-child,.tbl th:last-child{border-radius:0 14px 14px 0}
[data-testid="stMarkdownContainer"] td:first-child,.tbl td:first-child{text-align:left}
[data-testid="stMarkdownContainer"] tbody tr:hover td,.tbl tbody tr:hover td{background:#F1FBFD}
.tbl tfoot td{border:0;background:var(--light-cyan);color:var(--deep-twilight)}
.tbl tfoot td:first-child{border-radius:14px 0 0 14px;font-weight:700}.tbl tfoot td:last-child{border-radius:0 14px 14px 0}
.tbl.mat{min-width:480px}
.dot{display:inline-block;width:16px;height:16px;border-radius:50%;vertical-align:middle}
.dot.y{background:var(--bright-teal-blue)}.dot.n{border:2px solid var(--frosted-blue)}
.kosong{padding:24px;text-align:center;color:var(--mute)}
.st-key-cari{max-width:360px;margin:18px 0;position:relative}
.st-key-cari::before{content:"";position:absolute;left:16px;top:50%;transform:translateY(-50%);width:18px;height:18px;z-index:2;pointer-events:none;
  background:SEARCH_URI no-repeat center/18px}
.st-key-cari input{padding-left:44px!important}

.acts-wrap{margin-top:20px}
.st-key-acts{display:flex!important;flex-direction:row!important;flex-wrap:wrap;align-items:center;gap:12px!important;margin-top:20px}
.st-key-acts [data-testid="stElementContainer"]{width:auto!important}

/* ---------- footer ---------- */
.foot{margin:40px 0 12px;background:var(--deep-twilight);color:var(--light-cyan);border-radius:28px;padding:26px 22px;font-size:.88rem}
.foot b{color:#fff;font-size:1.05rem}
.foot p{margin-top:6px;max-width:52em;opacity:.85}

/* tombol 'kembali': ikon di kiri teks */
.st-key-btn_kembali_identitas button > div > span,.st-key-btn_ubah_gejala button > div > span,.st-key-btn_periksa_lain button > div > span{flex-direction:row!important}

/* ---------- responsif ---------- */
@media (max-width:899px){
  [class*="st-key-split_"] > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
  [class*="st-key-split_"] > [data-testid="stHorizontalBlock"]{flex-direction:column!important}
  [class*="st-key-split_"] [data-testid="stColumn"]{flex:none!important;width:100%!important;min-width:0!important}
  .st-key-split_gejala [data-testid="stColumn"]:nth-child(2){order:0}
  .st-key-hero{padding:34px 22px}
  .st-key-hero > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
  .st-key-hero > [data-testid="stHorizontalBlock"]{flex-direction:column!important}
  .st-key-hero [data-testid="stColumn"]{flex:none!important;width:100%!important}
  .metode{grid-template-columns:1fr;padding:28px 22px}
  .sh-main{grid-template-columns:1fr}
  .sh-body{grid-template-columns:1fr}
  .sh-body .blk+.blk{border-left:0;border-top:1.5px dashed var(--line)}
}
@media (max-width:600px){
  .g3{grid-template-columns:1fr}
  .st-key-tiles_keluhan,.st-key-tiles_lab{grid-template-columns:repeat(2,1fr)}
  [class*="st-key-card"]{padding:20px;border-radius:24px}
}
@media (max-width:480px){
  [data-testid="stMainBlockContainer"]{padding-left:14px!important;padding-right:14px!important}
  .st-key-nav{padding:10px 0 8px}
  .st-key-nav > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],.st-key-nav > [data-testid="stHorizontalBlock"]{padding:6px 6px 6px 14px}
  .st-key-nav button[data-testid^="stBaseButton"]{padding:8px 10px;font-size:.84rem}
  .st-key-hero{padding:28px 18px;border-radius:26px}
  .fan{--s:.85;height:214px}
  .sh-main,.blk{padding-left:18px;padding-right:18px}.sh-top{padding:12px 18px}
  .chart{gap:6px}
}
@media (max-width:420px){.brand .bt{display:none}}
"""


def _css_kode_gejala(kode_list):
    """Label kode (G1, G2, ...) pada tile gejala, dibuat per kode."""

    return "\n".join(
        f'.st-key-gejala_{k} label::before{{content:"{k}"}}' for k in kode_list
    )


def terapkan(kode_gejala=(), tab_aktif=0):
    """Menyuntikkan CSS tema ke halaman."""

    css = (
        CSS.replace("CHECK_URI", _uri_svg("check", "#03045E"))
        .replace("CHEVRON_URI", _uri_svg("chevron-down", "#03045E"))
        .replace("SEARCH_URI", _uri_svg("search", "#4E6182"))
    )
    st.markdown(
        f"<style>{css}\n{_css_kode_gejala(kode_gejala)}\n"
        f".st-key-nav .st-key-nav_{tab_aktif} button[data-testid^='stBaseButton']"
        "{background:var(--bright-teal-blue)!important;color:#fff!important}</style>",
        unsafe_allow_html=True,
    )
