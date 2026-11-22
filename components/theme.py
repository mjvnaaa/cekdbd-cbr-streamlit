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
import streamlit.components.v1 as components

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
  /* warna */
  --deep-twilight:#03045E;--bright-teal-blue:#0077B6;--turquoise-surf:#00B4D8;
  --frosted-blue:#90E0EF;--light-cyan:#CAF0F8;--white:#fff;--bg:#F3FBFD;
  --ink:#0E1A3D;--mute:#4E6182;--line:#C6E6F0;--err:#C0362C;
  --font:Inter,"Plus Jakarta Sans",system-ui,"Segoe UI",Arial,sans-serif;
  /* skala spasi (kelipatan 4 / 8 px) */
  --sp-1:4px;--sp-2:8px;--sp-3:12px;--sp-4:16px;--sp-5:24px;--sp-6:32px;--sp-7:48px;--sp-8:64px;
  /* skala radius: kontrol < tile < kartu < blok besar */
  --r-ctl:12px;--r-tile:16px;--r-card:24px;--r-hero:32px;
  /* skala tipografi */
  --fs-xs:.8rem;--fs-sm:.875rem;--fs-md:1rem;--fs-lg:1.25rem;--fs-xl:1.5rem;
  --lh-body:1.6;
  /* tinggi minimum kontrol (area sentuh >= 44px) */
  --h-ctl:48px;   /* input & segmented: sama tinggi dengan tombol */
  --h-btn:48px;   /* tombol standar */
  --h-btn-lg:56px;/* tombol CTA hero */
  --h-btn-sm:40px;/* tombol navbar */
}

/* ---------- kerangka Streamlit ---------- */
.stApp{background:var(--bg);color:var(--ink)}
.stApp, .stApp div, .stApp p, .stApp label, .stApp button, .stApp input,
.stApp summary, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp table,
.stApp th, .stApp td, .stApp li, .stApp small, .stApp b{font-family:var(--font)}
[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],
[data-testid="stToolbar"],[data-testid="stDecoration"],footer{display:none!important}
[data-testid="stMainBlockContainer"]{max-width:1120px;padding:0 var(--sp-5) 0!important;margin:0 auto}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]{gap:0}
.stApp p{margin:0;line-height:var(--lh-body)}
/* Streamlit memberi margin-bottom negatif pada kontainer markdown; itu memotong margin bawah elemen kita */
.stApp [data-testid="stMarkdown"],.stApp [data-testid="stMarkdownContainer"]{margin-bottom:0!important}
/* placeholder st.empty() yang kosong tidak boleh menambah celah */
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stEmpty"]:empty){display:none}
.stApp h1,.stApp h2,.stApp h3{color:var(--deep-twilight);margin:0;padding:0;line-height:1.2;letter-spacing:-.03em;font-weight:800}
.ic{flex:none;vertical-align:middle}
.mute{color:var(--mute)}

/* ---------- navbar pil melayang ---------- */
[data-testid="stLayoutWrapper"]:has(> .st-key-nav),
[data-testid="stElementContainer"]:has(> .st-key-nav),
.st-key-nav{position:sticky;top:0;z-index:60}
.st-key-nav{background:var(--bg);padding:var(--sp-4) 0 var(--sp-3);box-shadow:0 0 0 100vmax var(--bg);clip-path:inset(0 -100vmax -16px -100vmax)}
.st-key-nav::after{content:"";position:absolute;left:0;right:0;top:100%;height:16px;background:linear-gradient(var(--bg),rgba(243,251,253,0));pointer-events:none}
.st-key-nav > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
.st-key-nav > [data-testid="stHorizontalBlock"]{
  max-width:720px;margin:0 auto;display:flex!important;flex-wrap:nowrap!important;align-items:center;gap:var(--sp-1)!important;
  background:var(--deep-twilight);border-radius:999px;padding:var(--sp-2) var(--sp-2) var(--sp-2) var(--sp-5);box-shadow:0 10px 30px rgba(3,4,94,.22)}
.st-key-nav [data-testid="stColumn"]{flex:0 0 auto!important;width:auto!important;min-width:0!important}
.st-key-nav [data-testid="stColumn"]:first-child{margin-right:auto}
.st-key-nav [data-testid="stElementContainer"]{width:auto!important}
.st-key-nav [data-testid="stVerticalBlock"],.st-key-nav [data-testid="stMarkdownContainer"]{gap:0!important;margin:0!important;line-height:1}
.brand{display:flex;align-items:center;gap:var(--sp-2);color:#fff;font-weight:800;letter-spacing:-.02em;font-size:var(--fs-md);white-space:nowrap}
.brand .ic{color:var(--turquoise-surf)}
.st-key-nav button[data-testid^="stBaseButton"]{
  background:transparent!important;color:var(--light-cyan)!important;box-shadow:none!important;
  height:var(--h-btn-sm)!important;min-height:var(--h-btn-sm)!important;min-width:0!important;line-height:24px!important;padding:0 var(--sp-4)!important;font-size:var(--fs-sm);font-weight:600;transform:none!important;transition:background .15s}
.st-key-nav button[data-testid^="stBaseButton"]:hover{background:rgba(144,224,239,.2)!important}

/* ---------- tombol ---------- */
.stApp button[data-testid^="stBaseButton"]{
  display:inline-flex;align-items:center;justify-content:center;gap:var(--sp-2);height:var(--h-btn);min-height:var(--h-btn);min-width:160px;line-height:24px;white-space:nowrap;
  padding:0 var(--sp-5);border:0;border-radius:999px;font:600 1rem var(--font);cursor:pointer;transition:transform .15s,background .15s}
.stApp button[data-testid^="stBaseButton"] p{color:inherit;font:inherit;margin:0;line-height:inherit}
.stApp button[data-testid^="stBaseButton"] > div{display:flex;align-items:center;justify-content:center}
.stApp button[data-testid^="stBaseButton"] > div > span{display:flex;align-items:center;justify-content:center;gap:var(--sp-2);flex-direction:row-reverse}
.stApp button[data-testid^="stBaseButton"] [data-testid="stIconMaterial"]{font-size:20px;width:20px;height:20px;color:inherit}
.stApp button[kind="primary"],.stApp button[kind="primaryFormSubmit"]{background:var(--bright-teal-blue);color:#fff}
.stApp button[kind="primary"]:hover,.stApp button[kind="primaryFormSubmit"]:hover{background:var(--deep-twilight);color:#fff;transform:translateY(-2px)}
.stApp button[kind="secondary"],.stApp button[kind="secondaryFormSubmit"]{background:transparent;color:var(--bright-teal-blue);box-shadow:inset 0 0 0 1.5px var(--frosted-blue)}
.stApp button[kind="secondary"]:hover,.stApp button[kind="secondaryFormSubmit"]:hover{background:var(--light-cyan);color:var(--deep-twilight);transform:translateY(-2px)}
.stApp button[data-testid^="stBaseButton"]:focus-visible{outline:3px solid var(--turquoise-surf);outline-offset:2px}
.stApp button[data-testid^="stBaseButton"]:focus:not(:focus-visible){box-shadow:inherit}

/* ---------- ritme halaman ---------- */
.page-top{height:var(--sp-5)}

/* ---------- beranda: hero ---------- */
.st-key-hero{
  background:linear-gradient(120deg,var(--deep-twilight) 0%,var(--bright-teal-blue) 68%,var(--turquoise-surf) 135%);
  color:#fff;border-radius:var(--r-hero);padding:var(--sp-8) var(--sp-7);overflow:hidden;margin-top:var(--sp-5)}
.st-key-hero > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
.st-key-hero > [data-testid="stHorizontalBlock"]{align-items:center;gap:var(--sp-6)}
.stApp .st-key-hero h1{color:#fff;font-size:clamp(1.9rem,5vw,3rem);line-height:1.12;margin:var(--sp-5) 0 var(--sp-4)}
.lead{color:var(--light-cyan);max-width:34em;font-size:1.0625rem;line-height:1.65}
.pill{display:inline-flex;align-items:center;gap:var(--sp-2);padding:var(--sp-2) var(--sp-4);border-radius:99px;background:rgba(144,224,239,.2);color:var(--light-cyan);font-size:var(--fs-xs);font-weight:600;line-height:1.2}
.st-key-cta > [data-testid="stHorizontalBlock"],.st-key-cta{gap:var(--sp-3)}
.st-key-cta{display:flex!important;flex-direction:row!important;flex-wrap:wrap;margin-top:var(--sp-6)}
.st-key-cta [data-testid="stElementContainer"]{width:auto!important}
.st-key-cta button{height:var(--h-btn-lg)!important;min-height:var(--h-btn-lg)!important;padding:0 var(--sp-6)!important;min-width:192px}
.st-key-hero_start button{background:#fff!important;color:var(--deep-twilight)!important;box-shadow:none!important}
.st-key-hero_start button:hover{background:var(--frosted-blue)!important}
.st-key-hero_data button{background:transparent!important;color:#fff!important;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.5)!important}
.st-key-hero_data button:hover{background:rgba(255,255,255,.14)!important}
.fan{--s:1;position:relative;height:250px;width:100%;max-width:380px;margin:0 auto;transform:scale(var(--s));transform-origin:50% 100%}
.fan div{--x:0px;--a:0deg;position:absolute;bottom:0;left:50%;width:118px;height:168px;margin-left:-59px;border-radius:22px;padding:var(--sp-4);display:flex;flex-direction:column;justify-content:space-between;
  transform-origin:50% 130%;transform:translateX(var(--x)) rotate(var(--a));transition:transform .4s cubic-bezier(.2,.8,.2,1);box-shadow:0 14px 28px rgba(3,4,94,.28)}
.fan b{font-size:2.6rem;font-weight:800;line-height:1}.fan small{font-weight:600;font-size:var(--fs-xs);opacity:.8}
.fan div:nth-child(1){--x:-118px;--a:-14deg;background:var(--light-cyan);color:var(--deep-twilight)}
.fan div:nth-child(2){--x:-40px;--a:-5deg;background:var(--frosted-blue);color:var(--deep-twilight)}
.fan div:nth-child(3){--x:40px;--a:5deg;background:var(--turquoise-surf);color:var(--deep-twilight)}
.fan div:nth-child(4){--x:118px;--a:14deg;background:#fff;color:var(--deep-twilight)}
.fan:hover div:nth-child(1){--x:-150px;--a:-19deg}.fan:hover div:nth-child(2){--x:-52px;--a:-7deg}
.fan:hover div:nth-child(3){--x:52px;--a:7deg}.fan:hover div:nth-child(4){--x:150px;--a:19deg}

/* ---------- beranda: seksi ---------- */
.blok{padding-top:var(--sp-8)}
.stApp .blok h2{font-size:1.75rem}
.sec-sub{color:var(--mute);margin:var(--sp-2) 0 var(--sp-5)}
.g3{display:grid;gap:var(--sp-5);grid-template-columns:repeat(3,1fr)}
.st-card{background:#fff;border:1.5px solid var(--line);border-radius:var(--r-card);padding:var(--sp-5) var(--sp-5) 28px;transition:border-color .2s,transform .2s}
.st-card:hover{border-color:var(--turquoise-surf);transform:translateY(-3px)}
.stt{display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--sp-5);color:var(--bright-teal-blue)}
.stt small{font-weight:700;color:var(--mute);font-size:var(--fs-xs);letter-spacing:.02em}
.stApp .st-card h3{font-size:var(--fs-lg);margin-bottom:var(--sp-2)}
.st-card p{color:var(--mute);font-size:.95rem}
.metode{display:grid;gap:var(--sp-7);align-items:center;background:var(--light-cyan);border-radius:var(--r-hero);padding:var(--sp-7);grid-template-columns:1fr 1fr}
.metode p{color:var(--mute)}
.metode h2+p{margin-top:var(--sp-3)}
.bits{display:grid;grid-template-columns:repeat(14,1fr);gap:6px}
.bits i{aspect-ratio:1;border-radius:7px;background:#fff;opacity:.7}
.bits i.on{background:var(--bright-teal-blue);opacity:1}
.bits-cap{color:var(--mute);font-size:var(--fs-sm);margin-top:var(--sp-4)}

/* ---------- kartu, form, split ---------- */
[class*="st-key-card"]{background:#fff;border:1.5px solid var(--line);border-radius:var(--r-card);padding:var(--sp-6);gap:0!important}
.stApp .card-h h2{font-size:var(--fs-xl)}
.stApp .card-h p{margin-top:var(--sp-2);color:var(--mute);font-size:.95rem}
.card-h{margin-bottom:var(--sp-5)}
.stApp .jd{font-size:clamp(1.75rem,4vw,2.5rem)}
.page-sub{margin-top:var(--sp-3);max-width:40em;color:var(--mute)}
[class*="st-key-split_"] > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
[class*="st-key-split_"] > [data-testid="stHorizontalBlock"]{gap:var(--sp-5);align-items:stretch}
/* kartu di kedua kolom dibuat setinggi kolomnya (rantai tinggi 100% sampai ke kartu) */
[class*="st-key-split_"] [data-testid="stColumn"] > [data-testid="stVerticalBlock"]{height:100%}
[class*="st-key-split_"] [data-testid="stColumn"] [data-testid="stLayoutWrapper"]:has(> [class*="st-key-card_"]),
[class*="st-key-split_"] [data-testid="stColumn"] [data-testid="stElementContainer"]:has(> [class*="st-key-card_"]){height:100%}
[class*="st-key-split_"] [class*="st-key-card_"]{height:100%;box-sizing:border-box}
@media (min-width:900px){
.st-key-split_gejala [data-testid="stColumn"]:nth-child(2){order:-1}
.st-key-split_gejala [data-testid="stColumn"]:nth-child(2){flex:0 0 320px!important;width:320px!important}
.st-key-split_gejala [data-testid="stColumn"]:nth-child(1){flex:1 1 0!important;width:auto!important;min-width:0}
.st-key-split_ident [data-testid="stColumn"]:nth-child(1){flex:0 0 320px!important;width:320px!important}
.st-key-split_ident [data-testid="stColumn"]:nth-child(2){flex:1 1 0!important;width:auto!important;min-width:0}
}
.side-h{margin-bottom:var(--sp-5)}
.stApp .side-h h3{font-size:1.0625rem;letter-spacing:-.01em}

/* stepper: geometri dipatok agar garis penghubung selalu pas dengan titik */
.stApp ol.vs{list-style:none!important;margin:0!important;padding:0!important}
.stApp ol.vs li{margin:0!important;padding:var(--sp-3) 0!important;list-style:none!important}
.vs li::marker{content:none}
.vs li{position:relative;display:flex;align-items:center;gap:var(--sp-3)}
.vs li:not(:last-child)::after{content:"";position:absolute;left:15px;top:48px;height:16px;width:2px;background:var(--frosted-blue)}
.vs li.done:not(:last-child)::after{background:var(--turquoise-surf)}
.dt{flex:none;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:var(--light-cyan);color:var(--bright-teal-blue);font-weight:700;font-size:var(--fs-sm);position:relative;z-index:1}
.vs b{display:block;font-size:.9375rem;color:var(--deep-twilight);line-height:16px}
.vs small{display:block;color:var(--mute);font-size:var(--fs-xs);line-height:16px}
.vs li.done .dt{background:var(--turquoise-surf);color:#fff}
.vs li.now .dt{background:var(--bright-teal-blue);color:#fff;box-shadow:0 0 0 4px var(--frosted-blue)}

/* form: label, input, segmented */
[data-testid="stForm"]{border:0!important;padding:0!important;background:transparent!important}
[data-testid="stForm"] > [data-testid="stVerticalBlock"]{gap:var(--sp-5)}
[data-testid="stForm"] [data-testid="stHorizontalBlock"]{gap:var(--sp-5)}
[data-testid="stWidgetLabel"] p{font-weight:600;font-size:var(--fs-sm);color:var(--deep-twilight);margin-bottom:0;line-height:1.4}
[data-testid="stWidgetLabel"]{margin-bottom:var(--sp-2);min-height:0}
[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"]{
  background:#fff;border:1.5px solid var(--line)!important;border-radius:var(--r-ctl)!important;overflow:hidden;transition:border-color .15s,box-shadow .15s}
[data-testid="stTextInputRootElement"]:focus-within,[data-testid="stNumberInputContainer"]:focus-within{border-color:var(--bright-teal-blue)!important;box-shadow:0 0 0 4px rgba(0,180,216,.22)!important}
[data-testid="stTextInputRootElement"],[data-testid="stNumberInputContainer"]{min-height:var(--h-ctl);align-items:center}
[data-testid="stTextInputRootElement"] input,[data-testid="stNumberInputContainer"] input{padding:var(--sp-3) var(--sp-4);font:inherit;font-size:var(--fs-md);color:var(--ink);background:#fff}
[data-testid="stTextInputRootElement"] input::placeholder{color:#8EA0BD}
[data-testid="stNumberInputContainer"] button{background:#fff;color:var(--mute);border:0;border-left:1px solid var(--line)!important;min-height:0;border-radius:0}
[data-testid="stNumberInputContainer"] button:hover{background:var(--light-cyan);color:var(--deep-twilight)}
[data-testid="stElementContainer"]:has(> [data-testid="stRadio"]),[data-testid="stRadio"]{width:100%!important}
[data-testid="stRadioGroup"]{display:grid!important;grid-template-columns:1fr 1fr;gap:0!important;width:100%;border:1.5px solid var(--line);border-radius:var(--r-ctl);overflow:hidden;background:#fff}
[data-testid="stRadioGroup"] > div{margin:0!important;width:100%}
[data-testid="stRadioOption"]{display:flex!important;align-items:center;justify-content:center;width:100%;min-height:calc(var(--h-ctl) - 3px);margin:0!important;padding:0 var(--sp-2);cursor:pointer;text-align:center;transition:background .15s}
[data-testid="stRadioOption"] > div{justify-content:center}
[data-testid="stRadioOption"] > div > div:first-child{display:none!important}
[data-testid="stRadioOption"] p{color:var(--mute)!important;font-weight:600;font-size:var(--fs-md)}
[data-testid="stRadioOption"]:has(input:checked){background:var(--bright-teal-blue)}
[data-testid="stRadioOption"]:has(input:checked) p{color:#fff!important}
[data-testid="stRadioOption"]:has(input:focus-visible){box-shadow:inset 0 0 0 3px var(--turquoise-surf)}
.err{color:var(--err);font-size:.9rem;margin:0;line-height:1.4}

/* ---------- gejala: tile ---------- */
.stApp .gh{margin:var(--sp-6) 0 var(--sp-4);padding:0!important;color:var(--bright-teal-blue);font-size:var(--fs-md);line-height:1.3;letter-spacing:-.01em}
.stApp .card-h + .gh{margin-top:0}
[data-testid="stHeaderActionElements"],.gh a{display:none!important}
.stApp .gh .mute{font-weight:500;font-size:var(--fs-md)}
/* semua tile berukuran sama; baris terakhir yang tidak penuh diratakan di tengah */
.st-key-tiles_keluhan,.st-key-tiles_lab{--cols:4;--gap:var(--sp-3);margin:0!important;display:flex!important;flex-direction:row!important;flex-wrap:wrap;justify-content:center;align-items:flex-start;gap:var(--gap)!important}
.st-key-tiles_keluhan > *,.st-key-tiles_lab > *{flex:0 0 calc((100% - (var(--cols) - 1) * var(--gap)) / var(--cols));width:calc((100% - (var(--cols) - 1) * var(--gap)) / var(--cols))!important;max-width:100%}
.st-key-tiles_keluhan [data-testid="stElementContainer"],.st-key-tiles_lab [data-testid="stElementContainer"]{width:100%!important}
[class*="st-key-gejala_"],[class*="st-key-gejala_"] [data-testid="stCheckbox"]{width:100%;height:96px}
[class*="st-key-gejala_"] label{
  position:relative;display:flex!important;flex-direction:column;align-items:flex-start;justify-content:space-between;gap:var(--sp-4);
  width:100%;height:96px;box-sizing:border-box;margin:0;padding:var(--sp-4);background:#fff;border:1.5px solid var(--line);border-radius:var(--r-tile);cursor:pointer;
  transition:background .15s,border-color .15s,transform .15s}
[class*="st-key-gejala_"] label:hover{border-color:var(--turquoise-surf);transform:translateY(-2px)}
[class*="st-key-gejala_"] label > div:not([data-testid="stWidgetLabel"]){display:none!important}
[class*="st-key-gejala_"] label::before{
  align-self:flex-start;box-sizing:border-box;height:24px;font-size:.75rem;font-weight:700;line-height:20px;padding:2px 10px;border-radius:99px;background:var(--light-cyan);color:var(--bright-teal-blue)}
[class*="st-key-gejala_"] label::after{
  content:"";position:absolute;top:var(--sp-4);right:var(--sp-4);width:24px;height:24px;border-radius:50%;border:2px solid var(--frosted-blue);box-sizing:border-box;transition:all .15s}
[class*="st-key-gejala_"] [data-testid="stWidgetLabel"]{margin:0;visibility:visible!important}
[class*="st-key-gejala_"] [data-testid="stWidgetLabel"] p{font-weight:600;font-size:.9375rem;line-height:1.25;color:var(--ink)}
[class*="st-key-gejala_"] label:has(input:checked){background:var(--bright-teal-blue);border-color:var(--bright-teal-blue)}
[class*="st-key-gejala_"] label:has(input:checked) p{color:#fff}
[class*="st-key-gejala_"] label:has(input:checked)::before{background:rgba(255,255,255,.22);color:#fff}
[class*="st-key-gejala_"] label:has(input:checked)::after{
  background-color:var(--turquoise-surf);border-color:var(--turquoise-surf);
  background-image:CHECK_URI;background-repeat:no-repeat;background-position:center;background-size:14px}
[class*="st-key-gejala_"] label:has(input:focus-visible){outline:3px solid var(--turquoise-surf);outline-offset:2px}

.meter{margin:var(--sp-5) 0 0;padding:var(--sp-5);border-radius:var(--r-tile);background:var(--light-cyan)}
.mn{display:flex;align-items:baseline;gap:var(--sp-2)}
.mn b{font-size:2.5rem;font-weight:800;color:var(--deep-twilight);line-height:1}
.mn span{color:var(--mute);font-size:.9rem}
.mn em{font-style:normal}
.prog{height:8px;margin-top:var(--sp-4);border-radius:99px;background:#fff;overflow:hidden}
.prog i{display:block;height:100%;background:var(--turquoise-surf);border-radius:99px;transition:width .3s}
.st-key-side_actions{gap:var(--sp-3)!important;margin-top:var(--sp-4)}
.st-key-side_actions [data-testid="stElementContainer"],.st-key-side_actions .stButton{width:100%!important}
.st-key-side_actions button{width:100%}
.st-key-side_actions + [data-testid="stElementContainer"]:not(:empty){margin-top:var(--sp-4)}

/* ---------- hasil: lembar laporan ---------- */
.st-key-wrap920{max-width:880px;margin:0 auto;width:100%;gap:0!important}
.sheet{background:#fff;border:1.5px solid var(--line);border-radius:var(--r-card);overflow:hidden}
.sh-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:var(--sp-2);padding:var(--sp-4) var(--sp-6);background:var(--light-cyan);color:var(--deep-twilight);font-size:var(--fs-sm)}
.sh-top .ic{margin-right:var(--sp-2)}
.sh-main{display:grid;gap:var(--sp-6);padding:var(--sp-6);grid-template-columns:1fr auto;align-items:end}
.stApp .lbl{font-size:var(--fs-sm);font-weight:600;color:var(--mute);margin-bottom:var(--sp-2);line-height:1.4}
.big{font-size:clamp(3.2rem,12vw,5.4rem);font-weight:800;letter-spacing:-.045em;color:var(--deep-twilight);line-height:1}
.big.sm{font-size:clamp(1.75rem,5vw,2.5rem);line-height:1.15;letter-spacing:-.03em}
.grade-name{margin-top:var(--sp-3);font-weight:600;color:var(--deep-twilight)}
.nomatch{margin-top:var(--sp-3);color:var(--mute)}
.pct{font-size:clamp(2.2rem,8vw,3.2rem);font-weight:800;letter-spacing:-.04em;color:var(--bright-teal-blue);line-height:1}
.pct-note{margin-top:var(--sp-3);color:var(--mute);font-size:var(--fs-sm)}
.scale{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--sp-2);margin-top:var(--sp-5);max-width:420px}
.scale div{position:relative;padding:var(--sp-3) var(--sp-1);border-radius:var(--r-ctl);background:var(--light-cyan);color:var(--bright-teal-blue);text-align:center;font-weight:800;line-height:1.2}
.scale .on{background:var(--deep-twilight);color:#fff}
.scale .on::after{content:"";position:absolute;bottom:-7px;left:50%;margin-left:-7px;border:7px solid transparent;border-top-color:var(--deep-twilight);border-bottom:0}
.sh-body{border-top:1.5px dashed var(--line);display:grid;grid-template-columns:1fr 1fr}
.sh-body .blk+.blk{border-left:1.5px dashed var(--line)}
.blk{padding:var(--sp-5) var(--sp-6)}.blk h3{margin-bottom:var(--sp-4);font-size:var(--fs-md);letter-spacing:-.01em}
.blk.top{border-top:1.5px dashed var(--line);padding-bottom:var(--sp-6)}
dl{display:grid;grid-template-columns:max-content 1fr;gap:var(--sp-3) var(--sp-5);margin:0;line-height:1.4}
dt{color:var(--mute)}dd{margin:0;font-weight:600}
.tag{display:inline-block;padding:6px 14px;margin:0 var(--sp-2) var(--sp-2) 0;border-radius:99px;background:var(--light-cyan);color:var(--deep-twilight);font-size:var(--fs-sm);font-weight:600;line-height:1.3}
.chart{display:flex;align-items:flex-end;gap:var(--sp-4);height:200px}
.col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;gap:var(--sp-2)}
.area{flex:1;width:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:6px}
.col .v{font-size:var(--fs-xs);font-weight:700;color:var(--deep-twilight);line-height:1.2}
.col .b{width:100%;max-width:72px;height:var(--h);border-radius:14px 14px 4px 4px;background:var(--frosted-blue);animation:grow 1s cubic-bezier(.2,.8,.2,1)}
.col.top .b{background:linear-gradient(0deg,var(--bright-teal-blue),var(--turquoise-surf))}
.col small{font-weight:700;color:var(--mute);font-size:var(--fs-xs);line-height:1.2}.col.top small{color:var(--bright-teal-blue)}
@keyframes grow{from{height:0}}
.note{display:flex;gap:var(--sp-3);align-items:flex-start;margin-top:var(--sp-5);padding:var(--sp-4) var(--sp-5);border-radius:var(--r-tile);background:var(--light-cyan);color:var(--deep-twilight);font-size:.9rem;line-height:1.55}
.note.flat{margin-top:0}
.note .ic{color:var(--bright-teal-blue);margin-top:2px}
.st-key-card_revisi{margin-top:var(--sp-5)}
.st-key-card_revisi{gap:var(--sp-5)!important}
.st-key-card_revisi .card-h{margin-bottom:0}
.st-key-card_revisi [data-testid="stAlert"]{border-radius:var(--r-tile)}
.st-key-card_revisi [data-testid="stAlertContainer"]{padding:var(--sp-4) var(--sp-5)}
.st-key-card_revisi [data-testid="stAlert"] p{font-size:.95rem;line-height:1.55}
.st-key-card_revisi button{align-self:flex-start}

/* expander gaya <details> referensi */
[data-testid="stExpander"]{margin-top:var(--sp-5);background:#fff;border:1.5px solid var(--line)!important;border-radius:var(--r-card)!important;overflow:hidden}
[data-testid="stExpander"] details{border:0!important;background:transparent}
[data-testid="stExpander"] summary{display:flex;align-items:center;gap:var(--sp-3);padding:var(--sp-4) var(--sp-5);min-height:56px;cursor:pointer;font-weight:700;color:var(--deep-twilight);list-style:none}
[data-testid="stExpander"] summary:hover{background:#F1FBFD}
[data-testid="stExpander"] summary [data-testid="stIconMaterial"]{display:none!important}
[data-testid="stExpander"] summary p{font-weight:700;color:var(--deep-twilight);font-size:var(--fs-md)}
[data-testid="stExpander"] summary::after{content:"";margin-left:auto;width:20px;height:20px;flex:none;transition:transform .2s;
  background:CHEVRON_URI no-repeat center/20px}
[data-testid="stExpander"] details[open] > summary::after{transform:rotate(180deg)}
[data-testid="stExpanderDetails"]{padding:0 var(--sp-5) var(--sp-5)!important}
[data-testid="stExpanderDetails"] h4{font-size:var(--fs-md);letter-spacing:-.01em;margin:var(--sp-5) 0 var(--sp-3)}
[data-testid="stExpanderDetails"] code{background:var(--light-cyan);color:var(--deep-twilight);border-radius:8px}
[data-testid="stExpanderDetails"] pre{background:var(--light-cyan)!important;border-radius:var(--r-tile)}

/* tabel (markdown + HTML) */
.scroll{overflow-x:auto}
[data-testid="stMarkdownContainer"] table,.tbl{width:100%;border-collapse:collapse;font-size:.92rem;border:0}
[data-testid="stMarkdownContainer"] th,[data-testid="stMarkdownContainer"] td,.tbl th,.tbl td{padding:var(--sp-3) var(--sp-4);border:0;border-bottom:1px solid var(--line);text-align:center;color:var(--ink);line-height:1.4}
[data-testid="stMarkdownContainer"] th,.tbl th{background:var(--light-cyan);color:var(--deep-twilight);font-weight:700;white-space:nowrap}
[data-testid="stMarkdownContainer"] th:first-child,.tbl th:first-child{border-radius:var(--r-ctl) 0 0 var(--r-ctl);text-align:left}
[data-testid="stMarkdownContainer"] th:last-child,.tbl th:last-child{border-radius:0 var(--r-ctl) var(--r-ctl) 0}
[data-testid="stMarkdownContainer"] td:first-child,.tbl td:first-child{text-align:left}
[data-testid="stMarkdownContainer"] tbody tr:hover td,.tbl tbody tr:hover td{background:#F1FBFD}
.tbl tfoot td{border:0;background:var(--light-cyan);color:var(--deep-twilight)}
.tbl tfoot td:first-child{border-radius:var(--r-ctl) 0 0 var(--r-ctl);font-weight:700}.tbl tfoot td:last-child{border-radius:0 var(--r-ctl) var(--r-ctl) 0}
.tbl.mat{min-width:480px}
.dot{display:inline-block;width:16px;height:16px;border-radius:50%;vertical-align:middle}
.dot.y{background:var(--bright-teal-blue)}.dot.n{border:2px solid var(--frosted-blue)}
.kosong{padding:var(--sp-5);text-align:center;color:var(--mute)}
.mat-wrap{background:#fff;border:1.5px solid var(--line);border-radius:var(--r-card);padding:var(--sp-3)}
.src{margin-top:var(--sp-4);color:var(--mute);font-size:var(--fs-sm)}
.st-key-cari{max-width:360px;margin:var(--sp-5) 0 var(--sp-4);position:relative}
.st-key-cari::before{content:"";position:absolute;left:var(--sp-4);top:50%;transform:translateY(-50%);width:18px;height:18px;z-index:2;pointer-events:none;
  background:SEARCH_URI no-repeat center/18px}
.st-key-cari input{padding-left:44px!important}

.st-key-acts{display:flex!important;flex-direction:row!important;flex-wrap:wrap;align-items:center;gap:var(--sp-3)!important;margin-top:var(--sp-5)}
.st-key-acts [data-testid="stElementContainer"]{width:auto!important}

/* ---------- footer ---------- */
.foot{margin:var(--sp-7) 0 var(--sp-5);background:var(--deep-twilight);color:var(--light-cyan);border-radius:var(--r-card);padding:var(--sp-6);font-size:var(--fs-sm)}
.foot b{color:#fff;font-size:1.0625rem}
.foot p{margin-top:var(--sp-2);max-width:52em;opacity:.85;line-height:1.6}

/* tombol 'kembali': ikon di kiri teks */
.st-key-btn_kembali_identitas button > div > span,.st-key-btn_ubah_gejala button > div > span,.st-key-btn_periksa_lain button > div > span{flex-direction:row!important}

/* ---------- responsif ---------- */
@media (max-width:899px){
  .st-key-tiles_keluhan,.st-key-tiles_lab{--cols:3}
  [class*="st-key-split_"] > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
  [class*="st-key-split_"] > [data-testid="stHorizontalBlock"]{flex-direction:column!important}
  [class*="st-key-split_"] [data-testid="stColumn"]{flex:none!important;width:100%!important;min-width:0!important}
  .st-key-split_gejala [data-testid="stColumn"]:nth-child(2){order:0}
  .st-key-hero{padding:var(--sp-7) var(--sp-5)}
  .st-key-hero > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
  .st-key-hero > [data-testid="stHorizontalBlock"]{flex-direction:column!important}
  .st-key-hero [data-testid="stColumn"]{flex:none!important;width:100%!important}
  .g3{gap:var(--sp-4)}
  .metode{grid-template-columns:1fr;gap:var(--sp-5);padding:var(--sp-6) var(--sp-5)}
  .blok{padding-top:var(--sp-7)}
  .sh-main{grid-template-columns:1fr;gap:var(--sp-5)}
  .sh-body{grid-template-columns:1fr}
  .sh-body .blk+.blk{border-left:0;border-top:1.5px dashed var(--line)}
}
@media (max-width:600px){
  [data-testid="stMainBlockContainer"]{padding-left:var(--sp-4)!important;padding-right:var(--sp-4)!important}
  .g3{grid-template-columns:1fr}
  .st-key-tiles_keluhan,.st-key-tiles_lab{--cols:2;--gap:var(--sp-2)}
  [class*="st-key-gejala_"] label{padding:var(--sp-3)}
  [class*="st-key-gejala_"] label::after{top:var(--sp-3);right:var(--sp-3)}
  [class*="st-key-card"]{padding:var(--sp-5)}
  [data-testid="stForm"] [data-testid="stHorizontalBlock"]{flex-direction:column;gap:var(--sp-5)}
  [data-testid="stForm"] button{width:100%}
  .st-key-acts [data-testid="stElementContainer"],.st-key-acts button{width:100%!important}
  .st-key-cta button{min-width:0}
  .st-key-cta [data-testid="stElementContainer"],.st-key-cta button{width:100%!important}
  .foot{padding:var(--sp-5)}
}
@media (max-width:480px){
  .st-key-nav{padding:var(--sp-3) 0 var(--sp-2)}
  .st-key-nav > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],.st-key-nav > [data-testid="stHorizontalBlock"]{padding:6px 6px 6px var(--sp-4)}
  .st-key-nav button[data-testid^="stBaseButton"]{padding:0 var(--sp-3)!important;font-size:.84rem}
  .st-key-hero{padding:var(--sp-6) var(--sp-4);border-radius:26px}
  .fan{--s:.85;height:214px}
  .sh-main,.blk{padding-left:var(--sp-5);padding-right:var(--sp-5)}.sh-top{padding:var(--sp-3) var(--sp-5)}
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


_JS_GULIR = """
(function () {
  var w = window;
  var d = (w.parent && w.parent !== w) ? w.parent.document : document;
  var p = (w.parent && w.parent !== w) ? w.parent : w;
  function naik() {
    ['[data-testid="stMain"]', 'section.main', '[data-testid="stAppViewContainer"]', '.main'].forEach(function (q) {
      var e = d.querySelector(q);
      if (e && e.scrollTo) { e.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
    });
    p.scrollTo(0, 0);
  }
  naik(); setTimeout(naik, 60); setTimeout(naik, 250);
})();
"""


def gulir_ke_atas():
    """Menggulir halaman ke paling atas (dipanggil sekali setiap berpindah langkah)."""

    st.session_state["_gulir_n"] = st.session_state.get("_gulir_n", 0) + 1
    skrip = f"<script>/* {st.session_state['_gulir_n']} */{_JS_GULIR}</script>"
    try:
        st.html(skrip, unsafe_allow_javascript=True)  # Streamlit versi baru
    except TypeError:
        components.html(skrip, height=0)  # versi lama