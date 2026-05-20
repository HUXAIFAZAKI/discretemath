"""Central CSS / HTML chrome for the Discrete Academy app."""

import streamlit as st

# ---------------------------------------------------------------------------
# Floating Math Particle System + Aurora Layer (injected once via JS guard)
# ---------------------------------------------------------------------------
PARTICLES_JS = """
<script>
(function(){
  if(window._daParticlesInit) return;
  window._daParticlesInit = true;

  /* ── Aurora blobs ── */
  var aStyle = document.createElement('style');
  aStyle.textContent = `
    @keyframes auroraA { 0%,100%{transform:translate(-50%,-50%) scale(1) rotate(0deg);}
      33%{transform:translate(-50%,-50%) scale(1.18) rotate(120deg);}
      66%{transform:translate(-50%,-50%) scale(.88) rotate(240deg);} }
    @keyframes auroraB { 0%,100%{transform:translate(-50%,-50%) scale(1) rotate(0deg);}
      50%{transform:translate(-50%,-50%) scale(1.25) rotate(180deg);} }
    @keyframes auroraC { 0%,100%{transform:translate(-50%,-50%) scale(1.1) rotate(0deg);}
      50%{transform:translate(-50%,-50%) scale(.9) rotate(-150deg);} }
    .da-aurora-blob {
      position:fixed;border-radius:50%;pointer-events:none;z-index:0;mix-blend-mode:screen;filter:blur(72px);
    }
  `;
  document.head.appendChild(aStyle);

  function mkBlob(top,left,w,h,color,anim,dur){
    var b=document.createElement('div');
    b.className='da-aurora-blob';
    b.style.cssText='top:'+top+';left:'+left+';width:'+w+';height:'+h+
      ';background:'+color+';animation:'+anim+' '+dur+' ease-in-out infinite;';
    document.body.appendChild(b);
  }
  mkBlob('5%','10%','520px','340px','radial-gradient(ellipse,rgba(64,138,113,.13),transparent 70%)','auroraA','22s');
  mkBlob('55%','70%','480px','300px','radial-gradient(ellipse,rgba(40,90,72,.10),transparent 70%)','auroraB','28s');
  mkBlob('30%','45%','380px','260px','radial-gradient(ellipse,rgba(176,228,204,.06),transparent 70%)','auroraC','18s');

  /* ── Math symbol particles ── */
  var canvas = document.createElement('canvas');
  canvas.id = 'da-particle-canvas';
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;opacity:0.18;';
  document.body.appendChild(canvas);
  var ctx = canvas.getContext('2d');
  var syms = ['\u2227','\u2228','\u2200','\u2203','\u2229','\u222a','\u2286','\u2208','\u2234','\u2211','\u2192','\u2194','\u00ac','\u2295','\u2205','\u2261','\u21d2','\u2115'];
  var W = canvas.width = window.innerWidth;
  var H = canvas.height = window.innerHeight;
  var pts = [];
  for(var i=0;i<28;i++){
    pts.push({
      x:Math.random()*W, y:Math.random()*H,
      vx:(Math.random()-.5)*.18, vy:(Math.random()-.5)*.18,
      sym:syms[Math.floor(Math.random()*syms.length)],
      sz:8+Math.random()*13,
      a:.04+Math.random()*.12,
      hue: Math.random() > .5 ? '#408A71' : '#B0E4CC'
    });
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    for(var i=0;i<pts.length;i++){
      var p=pts[i];
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<-30)p.x=W+30; if(p.x>W+30)p.x=-30;
      if(p.y<-30)p.y=H+30; if(p.y>H+30)p.y=-30;
      ctx.save();
      ctx.globalAlpha=p.a;
      ctx.fillStyle=p.hue;
      ctx.font=p.sz+'px "JetBrains Mono",monospace';
      ctx.fillText(p.sym,p.x,p.y);
      ctx.restore();
    }
    requestAnimationFrame(draw);
  }
  window.addEventListener('resize',function(){
    W=canvas.width=window.innerWidth;
    H=canvas.height=window.innerHeight;
  });
  draw();
})();
</script>
"""

# ---------------------------------------------------------------------------
# CSS factory
# ---------------------------------------------------------------------------
def _make_css(theme: str) -> str:
    L = theme == "light"

    # ── Palette ──────────────────────────────────────────────────────────
    # Dark:  #091413  #285A48  #408A71  #B0E4CC
    # Light: inverted — near-white bg, dark teal accents
    bg          = "#F2FAF6"                    if L else "#091413"
    bg_card     = "rgba(255,255,255,0.97)"     if L else "rgba(10,24,21,0.97)"
    bg_nav_top  = "rgba(242,250,246,0.95)"     if L else "rgba(9,20,19,0.95)"
    sidebar_bg  = ("linear-gradient(165deg,#FAFDF9 0%,#EEF8F3 100%)"
                   if L else
                   "linear-gradient(165deg,#0B1A17 0%,#071110 100%)")
    accent      = "#285A48"                    if L else "#408A71"
    accent2     = "#408A71"                    if L else "#B0E4CC"
    ag          = "rgba(40,90,72,.12)"         if L else "rgba(64,138,113,.16)"
    am          = "rgba(40,90,72,.07)"         if L else "rgba(64,138,113,.08)"
    text        = "#091413"                    if L else "#B0E4CC"
    text_s      = "#285A48"                    if L else "#6EADA0"
    text_d      = "#B0D4C4"                    if L else "#1E3A30"
    bdr         = "rgba(40,90,72,.14)"         if L else "rgba(64,138,113,.12)"
    bdr_b       = "rgba(40,90,72,.42)"         if L else "rgba(64,138,113,.42)"
    scr         = "#A8C8B8"                    if L else "#1E3830"
    lnk_c       = "#408A71"                    if L else "#6EADA0"
    lnk_ac      = "#285A48"                    if L else "#408A71"
    lnk_abg     = "rgba(40,90,72,.08)"         if L else "rgba(64,138,113,.10)"
    h_c         = "#091413"                    if L else "#B0E4CC"
    q_bg        = "rgba(242,250,246,.96)"      if L else "rgba(9,22,20,.94)"
    q_bdr       = "rgba(64,138,113,.30)"       if L else "rgba(40,90,72,.55)"
    form_bg     = "rgba(250,253,251,.98)"      if L else "rgba(8,18,16,.97)"
    res_bg      = "rgba(244,252,248,.97)"      if L else "rgba(6,14,12,.97)"
    formula_bg  = "rgba(40,90,72,.06)"         if L else "rgba(64,138,113,.07)"

    return f"""
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{ font-family: 'Space Grotesk', sans-serif; }}
.stApp {{ background: {bg} !important; color: {text}; }}

/* ── Animated dot-grid ── */
body::before {{
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image: radial-gradient(circle, {accent}22 1px, transparent 1px);
  background-size: 44px 44px;
  animation: gridDrift 50s linear infinite;
}}
@keyframes gridDrift {{
  from {{ background-position: 0 0; }}
  to   {{ background-position: 44px 44px; }}
}}

/* ── Shimmer keyframe (reused by cards) ── */
@keyframes shimmer {{
  0%   {{ transform: translateX(-120%) skewX(-18deg); }}
  100% {{ transform: translateX(220%) skewX(-18deg); }}
}}
@keyframes borderPulse {{
  0%,100% {{ box-shadow: 0 0 0 0 {ag}; }}
  50%     {{ box-shadow: 0 0 0 4px {ag}; }}
}}
@keyframes scanLine {{
  0%   {{ top: -8%; }}
  100% {{ top: 108%; }}
}}

/* Kill Streamlit chrome */
header[data-testid="stHeader"],
header[data-testid="stHeader"] > *,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu, footer {{ display: none !important; height: 0 !important; }}
section[data-testid="stSidebar"],
button[data-testid="collapsedControl"],
div[data-testid="collapsedControl"] {{ display: none !important; width: 0 !important; }}

.main .block-container {{
  padding-top: 82px !important;
  padding-left: 2.5rem !important;
  padding-right: 2.5rem !important;
  max-width: 1160px !important;
  position: relative; z-index: 1;
}}

/* ── Hamburger ── */
#ds-nav-toggle {{ display: none; }}
#ds-hamburger {{
  display: flex; flex-direction: column; justify-content: center;
  align-items: center; gap: 5px; flex-shrink: 0;
  width: 36px; height: 36px;
  background: {am}; border: 1px solid {bdr};
  border-radius: 8px; cursor: pointer;
  transition: border-color .22s, box-shadow .22s;
}}
#ds-hamburger:hover {{ border-color: {bdr_b}; box-shadow: 0 2px 14px {ag}; }}
#ds-hamburger .h-bar {{
  display: block; width: 16px; height: 1.5px;
  background: {accent}; border-radius: 2px;
  transition: transform .3s cubic-bezier(.4,0,.2,1), opacity .22s, width .25s;
}}
#ds-nav-toggle:checked ~ #ds-topbar #ds-hamburger .h-bar:nth-child(1) {{ transform: translateY(6.5px) rotate(45deg); }}
#ds-nav-toggle:checked ~ #ds-topbar #ds-hamburger .h-bar:nth-child(2) {{ opacity: 0; width: 0; }}
#ds-nav-toggle:checked ~ #ds-topbar #ds-hamburger .h-bar:nth-child(3) {{ transform: translateY(-6.5px) rotate(-45deg); }}

/* ── Overlay ── */
#ds-overlay {{
  position: fixed; inset: 0;
  background: rgba(9,20,19,.72); z-index: 100000;
  opacity: 0; pointer-events: none;
  transition: opacity .35s; backdrop-filter: blur(6px); cursor: pointer;
}}
#ds-nav-toggle:checked ~ #ds-overlay {{ opacity: 1; pointer-events: all; }}

/* ── Sidebar ── */
#ds-sidenav {{
  position: fixed; top: 0; left: -312px; width: 290px; height: 100vh;
  background: {sidebar_bg}; z-index: 100001;
  border-right: 1px solid {bdr};
  box-shadow: 12px 0 60px rgba(9,20,19,.7);
  transition: left .38s cubic-bezier(.4,0,.2,1);
  display: flex; flex-direction: column;
  overflow-y: auto; overflow-x: hidden;
}}
#ds-nav-toggle:checked ~ #ds-sidenav {{ left: 0; }}
#ds-sidenav::-webkit-scrollbar {{ width: 2px; }}
#ds-sidenav::-webkit-scrollbar-thumb {{ background: {scr}; border-radius: 2px; }}

.sn-header {{
  padding: 1.5rem 1.5rem 1.1rem;
  border-bottom: 1px solid {bdr}; flex-shrink: 0;
  position: relative; overflow: hidden;
}}
.sn-header::after {{
  content: ''; position: absolute; bottom: 0; left: 10%; right: 10%; height: 1px;
  background: linear-gradient(90deg, transparent, {accent}55, transparent);
}}
.sn-logo {{
  font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 800;
  color: {accent}; letter-spacing: -.01em; white-space: nowrap;
}}
.sn-logo span {{ color: {text_d}; font-weight: 400; }}
.sn-tagline {{
  font-family: 'JetBrains Mono', monospace; font-size: .58rem;
  color: {text_d}; letter-spacing: .16em; margin-top: .3rem;
}}
.sn-group {{
  font-family: 'JetBrains Mono', monospace; font-size: .53rem;
  color: {text_d}; letter-spacing: .22em; text-transform: uppercase;
  padding: 1.1rem 1.5rem .35rem; flex-shrink: 0;
}}
.sn-links {{ padding: .35rem .7rem; flex: 1; }}
.sn-links a {{
  display: flex; align-items: center; gap: .7rem;
  padding: .6rem .78rem; border-radius: 9px; margin-bottom: 2px;
  text-decoration: none; color: {lnk_c};
  font-family: 'Space Grotesk', sans-serif; font-size: .84rem; font-weight: 500;
  transition: all .2s; position: relative; border: 1px solid transparent;
}}
.sn-links a:hover {{ background: {am}; color: {text}; border-color: {bdr}; }}
.sn-links a.sn-active {{
  background: {lnk_abg}; color: {lnk_ac}; font-weight: 600; border-color: {bdr};
}}
.sn-links a.sn-active::before {{
  content: ''; position: absolute; left: -1px; top: 18%; height: 64%; width: 3px;
  background: linear-gradient(180deg, {accent}, {accent2}55);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 8px {accent}88;
}}
.sn-icon {{ font-size: .9rem; width: 20px; text-align: center; flex-shrink: 0; }}
.sn-label {{ flex: 1; line-height: 1.25; }}
.sn-sub {{ font-size: .64rem; color: {text_d}; display: block; margin-top: 1px; font-weight: 400; }}
a.sn-active .sn-sub {{ color: {accent}88; }}
.sn-week {{
  font-family: 'JetBrains Mono', monospace; font-size: .54rem;
  color: {text_d}; background: {am}; padding: .1rem .38rem; border-radius: 3px; flex-shrink: 0;
}}
a.sn-active .sn-week {{ color: {accent}; }}
.sn-footer {{
  padding: .9rem 1.5rem; border-top: 1px solid {bdr};
  font-family: 'JetBrains Mono', monospace; font-size: .58rem;
  color: {text_d}; line-height: 1.65; flex-shrink: 0;
}}

/* ── Top bar ── */
#ds-topbar {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 99999;
  height: 58px; display: flex; align-items: center;
  padding: 0 1.4rem;
  background: {bg_nav_top};
  backdrop-filter: blur(24px) saturate(160%); -webkit-backdrop-filter: blur(24px) saturate(160%);
  border-bottom: 1px solid {bdr}; box-sizing: border-box; gap: .75rem;
}}
/* Subtle animated accent line under topbar */
#ds-topbar::after {{
  content: ''; position: absolute; bottom: -1px; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent 0%, {accent}66 30%, {accent2}55 70%, transparent 100%);
  animation: topbarLine 6s ease-in-out infinite alternate;
}}
@keyframes topbarLine {{
  0%  {{ opacity: .4; background-position: 0% 50%; }}
  100%{{ opacity: 1;  background-position: 100% 50%; }}
}}
.tb-logo {{
  font-family: 'Syne', sans-serif; font-size: .98rem; font-weight: 800;
  color: {text}; letter-spacing: -.01em; white-space: nowrap;
}}
.tb-logo span {{ color: {accent}; }}
.tb-sep {{ color: {text_d}; font-size: 1rem; user-select: none; }}
.tb-page {{
  font-family: 'Space Grotesk', sans-serif; font-size: .8rem;
  color: {text_s}; font-weight: 500;
}}
.tb-spacer {{ flex: 1; }}
.tb-pill {{
  font-family: 'JetBrains Mono', monospace; font-size: .58rem;
  color: {accent}; border: 1px solid {bdr};
  padding: .18rem .7rem; border-radius: 20px; background: {am}; letter-spacing: .1em;
}}
.tb-theme-btn {{
  display: flex; align-items: center; justify-content: center;
  font-size: .9rem; cursor: pointer; text-decoration: none;
  width: 32px; height: 32px; border-radius: 8px;
  border: 1px solid {bdr}; background: {am}; transition: all .2s; color: {text};
}}
.tb-theme-btn:hover {{ border-color: {bdr_b}; background: {ag}; }}

/* ── Typography ── */
h1, h2, h3,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {{
  font-family: 'Syne', sans-serif; font-weight: 700; color: {h_c} !important;
}}
h2 {{ font-size: 1.75rem; letter-spacing: -.03em; margin-bottom: .3rem; }}
h3 {{ font-size: 1.22rem; letter-spacing: -.02em; }}

.hero-title {{
  font-family: 'Syne', sans-serif; font-size: 3.3rem; font-weight: 800;
  line-height: 1.04; letter-spacing: -.04em; color: {h_c};
}}
.hero-title em {{
  font-style: normal;
  background: linear-gradient(120deg, {accent} 0%, {accent2} 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.hero-sub {{
  font-family: 'Space Grotesk', sans-serif; font-size: 1.02rem;
  color: {text_s}; line-height: 1.72;
  max-width: 590px; margin: 1rem auto 0 !important; text-align: center !important;
  display: block; width: 100%;
}}
.hero-wrapper {{
  position: relative; text-align: center;
  padding: 4.2rem 1rem 2.8rem; overflow: hidden;
}}
.hero-glow {{
  position: absolute; top: -25%; left: 50%; transform: translateX(-50%);
  width: 740px; height: 440px;
  background: radial-gradient(ellipse at center, {ag} 0%, transparent 65%);
  pointer-events: none; border-radius: 50%; filter: blur(2px);
  animation: heroGlowPulse 5s ease-in-out infinite;
}}
@keyframes heroGlowPulse {{
  0%,100% {{ opacity: .7; transform: translateX(-50%) scale(1); }}
  50%      {{ opacity: 1;  transform: translateX(-50%) scale(1.08); }}
}}
.hero-glow-2 {{
  position: absolute; top: 12%; left: 18%; width: 220px; height: 220px;
  background: radial-gradient(ellipse, {am} 0%, transparent 72%);
  pointer-events: none; border-radius: 50%;
}}
.hero-inner {{ position: relative; z-index: 1; }}
.hero-eyebrow {{
  display: inline-flex; align-items: center; gap: .5rem;
  font-family: 'JetBrains Mono', monospace; font-size: .65rem;
  color: {accent}; letter-spacing: .2em;
  border: 1px solid {bdr}; padding: .3rem 1.1rem; border-radius: 20px;
  background: {am}; margin-bottom: 1.7rem;
}}
.hero-eyebrow::before {{
  content: ''; display: inline-block; width: 7px; height: 7px;
  background: {accent}; border-radius: 50%; box-shadow: 0 0 8px {accent};
  animation: pulseGlow 2.2s ease-in-out infinite;
}}
@keyframes pulseGlow {{
  0%,100% {{ box-shadow: 0 0 6px {accent}; opacity: .8; }}
  50%      {{ box-shadow: 0 0 18px {accent}, 0 0 32px {accent2}66; opacity: 1; }}
}}
.hero-stats {{
  display: flex; align-items: center; justify-content: center;
  gap: 1.6rem; margin-top: 2.3rem;
}}
.hero-stat {{ display: flex; flex-direction: column; align-items: center; gap: .1rem; }}
.hero-stat-num {{
  font-family: 'Syne', sans-serif; font-size: 1.65rem; font-weight: 800;
  color: {accent}; line-height: 1;
}}
.hero-stat-label {{
  font-family: 'JetBrains Mono', monospace; font-size: .57rem;
  color: {text_d}; letter-spacing: .14em; text-transform: uppercase;
}}
.hero-stat-sep {{ color: {text_d}; font-size: 1.2rem; margin-bottom: .5rem; }}
.hero-symbols {{
  font-family: 'JetBrains Mono', monospace; font-size: .68rem;
  color: {text_d}; letter-spacing: .28em; margin-top: 2.5rem;
}}
.page-header {{
  margin-bottom: 1.8rem; padding-bottom: 1.1rem; border-bottom: 1px solid {bdr};
}}
.page-header h2 {{ margin-bottom: .25rem; }}
.page-desc {{ font-size: .88rem; color: {text_s}; line-height: 1.68; }}
.accent {{ color: {accent}; }}
.mono {{ font-family: 'JetBrains Mono', monospace; }}

/* ── Cards ── */
.card {{
  background: {bg_card};
  border: 1px solid {bdr};
  border-radius: 14px; padding: 1.4rem; margin-bottom: 1rem;
  position: relative; overflow: hidden;
  transition: border-color .25s, box-shadow .25s, transform .25s;
  animation: fadeUp .45s ease both;
  backdrop-filter: blur(8px);
}}
/* Left accent bar */
.card::before {{
  content: ''; position: absolute; top: 14%; left: 0; height: 72%; width: 3px;
  background: linear-gradient(180deg, transparent, {accent} 40%, {accent2}88 80%, transparent);
  border-radius: 0 2px 2px 0;
}}
/* Shimmer sweep on hover */
.card::after {{
  content: ''; position: absolute; top: 0; left: -80%; width: 60%; height: 100%;
  background: linear-gradient(105deg, transparent 40%, {accent}14 50%, transparent 60%);
  pointer-events: none;
  transition: none;
}}
.card:hover::after {{
  animation: shimmer .65s ease forwards;
}}
.card:hover {{
  border-color: {bdr_b}; transform: translateY(-3px);
  box-shadow: 0 8px 38px {ag}, 0 0 0 1px {bdr_b};
}}
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.topic-card {{
  background: {bg_card}; border: 1px solid {bdr};
  border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: .6rem;
  position: relative; overflow: hidden;
  transition: border-color .22s, transform .22s, box-shadow .22s;
  animation: fadeUp .45s ease both;
  backdrop-filter: blur(6px);
}}
.topic-card:hover {{
  border-color: {bdr_b}; transform: translateY(-2px);
  box-shadow: 0 8px 36px {ag};
}}

/* ── Study mode ── */
.study-card {{
  background: {bg_card}; border: 1px solid {bdr};
  border-radius: 14px; padding: 1.6rem; margin-bottom: 1.2rem;
  position: relative; overflow: hidden;
  backdrop-filter: blur(8px);
}}
.study-card::after {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, {accent} 35%, {accent2} 65%, transparent);
}}

/* ── Progress bar ── */
.progress-bar-bg {{
  background: {am}; border-radius: 6px; height: 8px;
  overflow: hidden; border: 1px solid {bdr};
}}
.progress-bar-fill {{
  height: 100%; border-radius: 6px;
  background: linear-gradient(90deg, {accent}, {accent2});
  transition: width .6s cubic-bezier(.4,0,.2,1);
  box-shadow: 0 0 12px {ag};
  position: relative;
}}
/* Shimmer sweep on progress fill */
.progress-bar-fill::after {{
  content:''; position:absolute; top:0; left:-80%; width:60%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);
  animation: shimmer 2.2s ease infinite;
}}

/* ── Roadmap ── */
.roadmap-container {{
  max-width: 680px; margin: 0 auto;
}}
.roadmap-phase-label {{
  font-family: 'JetBrains Mono', monospace; font-size: .6rem;
  color: {accent}; letter-spacing: .22em; text-transform: uppercase;
  margin: .6rem 0 .6rem; opacity: .8; text-align: center;
}}
.roadmap-row {{
  display: flex; align-items: center; flex-wrap: wrap; gap: .5rem;
  margin-bottom: .4rem; justify-content: center;
}}
.roadmap-phase-connector {{
  display: flex; justify-content: center; align-items: center;
  margin: .1rem 0; color: {accent}55; font-size: 1.1rem; letter-spacing: .3em;
}}
.roadmap-node {{
  background: {bg_card}; border: 1px solid {bdr};
  border-radius: 12px; padding: .9rem 1.1rem;
  text-align: center; flex: 1; min-width: 120px; max-width: 170px;
  transition: all .22s; position: relative; overflow: hidden;
  backdrop-filter: blur(4px);
}}
.roadmap-node.mastered {{
  border-color: {accent}; background: {am};
  box-shadow: 0 0 20px {ag};
  animation: borderPulse 3s ease-in-out infinite;
}}
.roadmap-node.mastered::after {{
  content: '\u2713'; position: absolute; top: 4px; right: 7px;
  font-size: .65rem; color: {accent}; font-weight: 700;
}}
.roadmap-node.in-progress {{ border-color: {accent}66; }}
.roadmap-node.locked {{ opacity: .42; }}
.roadmap-node-icon {{ font-size: 1.15rem; margin-bottom: .25rem; display: block; }}
.roadmap-node-title {{
  font-family: 'Space Grotesk', sans-serif; font-size: .78rem; font-weight: 600;
  color: {text}; line-height: 1.25;
}}
.roadmap-node-week {{
  font-family: 'JetBrains Mono', monospace; font-size: .55rem;
  color: {text_d}; margin-top: .2rem; letter-spacing: .08em;
}}
.roadmap-node.mastered .roadmap-node-title {{ color: {accent}; }}
.roadmap-arrow {{ color: {accent}66; font-size: 1rem; flex-shrink: 0; padding: 0 .2rem; }}
.roadmap-node-bar {{
  margin-top: .5rem; background: {bdr}; border-radius: 3px; height: 4px; overflow: hidden;
}}
.roadmap-node-bar-fill {{
  height: 100%; border-radius: 3px;
  background: linear-gradient(90deg, {accent}, {accent2});
  transition: width .5s ease;
}}

/* ── Status / achievement badges ── */
.status-badge {{
  display: inline-flex; align-items: center; gap: .3rem;
  font-family: 'JetBrains Mono', monospace; font-size: .58rem;
  letter-spacing: .1em; padding: .2rem .6rem; border-radius: 20px;
}}
.status-badge.done    {{ color: {accent}; background: {am}; border: 1px solid {bdr}; }}
.status-badge.partial {{ color: {accent2}; background: rgba(176,228,204,.07); border: 1px solid rgba(176,228,204,.22); }}
.status-badge.new     {{ color: {text_d}; background: transparent; border: 1px solid {text_d}44; }}
.achievement {{
  display: inline-flex; align-items: center; gap: .4rem;
  font-family: 'Space Grotesk', sans-serif; font-size: .75rem; font-weight: 600;
  color: {text}; background: {bg_card};
  border: 1px solid {bdr}; border-radius: 20px;
  padding: .3rem .85rem; margin: .2rem; transition: all .2s;
}}
.achievement.earned {{
  border-color: {accent}; color: {accent}; background: {am};
  box-shadow: 0 0 14px {ag};
}}

/* ── Stat box ── */
.stat-box {{
  background: {bg_card}; border: 1px solid {bdr};
  border-radius: 14px; padding: 1.3rem 1.5rem; text-align: center;
  position: relative; overflow: hidden; transition: all .22s;
  backdrop-filter: blur(8px);
}}
.stat-box::before {{
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, {am} 0%, transparent 55%);
  pointer-events: none;
}}
.stat-box:hover {{ border-color: {bdr_b}; box-shadow: 0 4px 32px {ag}; transform: translateY(-2px); }}
.stat-box-num {{
  font-family: 'Syne', sans-serif; font-size: 2.1rem; font-weight: 800;
  color: {accent}; line-height: 1; position: relative;
}}
.stat-box-label {{
  font-family: 'Space Grotesk', sans-serif; font-size: .78rem;
  color: {text_s}; margin-top: .3rem; font-weight: 500; position: relative;
}}

/* ── CTA banner ── */
.cta-banner {{
  background: linear-gradient(130deg, {am} 0%, {bg_card} 100%);
  border: 1px solid {bdr}; border-radius: 14px;
  padding: 1.5rem 1.9rem; margin-bottom: 1.8rem;
  display: flex; align-items: center; gap: 1.3rem;
  position: relative; overflow: hidden;
  transition: border-color .22s, box-shadow .22s;
  backdrop-filter: blur(8px);
}}
.cta-banner:hover {{ border-color: {bdr_b}; box-shadow: 0 4px 36px {ag}; }}
.cta-banner::after {{
  content: ''; position: absolute; top: 0; right: 0;
  width: 160px; height: 100%;
  background: linear-gradient(90deg, transparent, {ag});
  pointer-events: none;
}}

/* ── Quiz options ── */
.quiz-option {{
  background: {q_bg}; border: 1px solid {q_bdr};
  border-radius: 10px; padding: .82rem 1.15rem; margin-bottom: .5rem;
  cursor: pointer; transition: all .18s; color: {text};
  font-family: 'Space Grotesk', sans-serif; font-size: .88rem;
}}
.quiz-option:hover {{ border-color: {bdr_b}; background: {am}; }}
.quiz-correct {{ border-color: #4ADE80 !important; background: rgba(74,222,128,.07) !important; color: #4ADE80 !important; }}
.quiz-wrong   {{ border-color: #EF5350 !important; background: rgba(239,83,80,.07) !important; color: #EF5350 !important; }}

/* ── Steps, formulas, results ── */
.problem-step {{
  border-left: 2px solid {bdr_b}; padding-left: 1rem; margin: .6rem 0;
  font-family: 'JetBrains Mono', monospace; font-size: .82rem; color: {text_s};
}}
.problem-step .step-num {{
  color: {accent}; font-weight: 600; font-size: .68rem;
  letter-spacing: .1em; display: block; margin-bottom: .2rem;
}}
.formula {{
  font-family: 'JetBrains Mono', monospace; font-size: .8rem;
  background: {formula_bg}; border: 1px solid {bdr};
  padding: .42rem .9rem; color: {accent}; border-radius: 6px;
  margin: .55rem 0; display: inline-block;
}}
.result-box {{
  background: {res_bg}; border: 1px solid {bdr};
  border-radius: 10px; padding: 1.05rem 1.1rem;
  font-family: 'JetBrains Mono', monospace; font-size: .82rem;
  color: {text_s}; margin-top: .8rem; white-space: pre-wrap;
  max-height: 420px; overflow-y: auto;
}}
.result-box::-webkit-scrollbar {{ width: 3px; }}
.result-box::-webkit-scrollbar-thumb {{ background: {scr}; border-radius: 3px; }}
.result-box .highlight {{ color: {accent}; font-weight: 600; }}
.result-box .err {{ color: #EF5350; }}

/* ── Team cards ── */
.team-grid {{ display: flex; flex-wrap: wrap; gap: .8rem; margin: 1.5rem 0; }}
.team-card {{
  background: {bg_card}; border: 1px solid {bdr};
  padding: .85rem 1.2rem; min-width: 188px;
  border-left: 3px solid {accent}; border-radius: 10px;
  transition: box-shadow .2s, transform .2s;
  backdrop-filter: blur(6px);
}}
.team-card:hover {{ box-shadow: 0 4px 24px {ag}; transform: translateY(-2px); }}
.team-id {{ font-family: 'JetBrains Mono', monospace; font-size: .62rem; color: {accent}; }}
.team-name {{ font-size: .88rem; font-weight: 600; color: {text}; margin-top: .22rem; }}
.team-num {{ font-family: 'JetBrains Mono', monospace; font-size: .64rem; color: {text_s}; margin-top: .1rem; }}

/* ── Forms ── */
.stTextInput > div > div > input, .stNumberInput > div > div > input,
input[type="text"], input[type="number"] {{
  background: {form_bg} !important; color: {text} !important;
  border: 1px solid {bdr} !important; border-radius: 8px !important;
  font-family: 'Space Grotesk', sans-serif !important; font-size: .86rem !important;
  caret-color: {accent} !important;
  transition: border-color .2s, box-shadow .2s !important;
}}
.stTextInput > div > div > input:focus, input[type="text"]:focus {{
  border-color: {accent} !important; box-shadow: 0 0 0 3px {ag} !important;
}}
textarea {{
  background: {form_bg} !important; color: {text} !important;
  border: 1px solid {bdr} !important; border-radius: 8px !important;
  font-family: 'Space Grotesk', sans-serif !important; font-size: .86rem !important;
  caret-color: {accent} !important;
  transition: border-color .2s, box-shadow .2s !important;
}}
textarea:focus {{ border-color: {accent} !important; box-shadow: 0 0 0 3px {ag} !important; }}
input::placeholder, textarea::placeholder {{ color: {text_d}88 !important; }}
div[data-testid="stSelectbox"] > div > div {{
  background: {form_bg} !important; border: 1px solid {bdr} !important;
  color: {text} !important; border-radius: 8px !important;
}}
div[data-testid="stSelectbox"] > div > div:focus-within {{
  border-color: {accent} !important; box-shadow: 0 0 0 3px {ag} !important;
}}

/* ── Tabs ── */
div[data-testid="stTabs"] button[role="tab"] {{
  font-family: 'Space Grotesk', sans-serif !important; font-size: .82rem !important;
  font-weight: 500 !important; color: {text_s} !important;
  border-radius: 8px 8px 0 0 !important; padding: .5rem 1.2rem !important;
  transition: all .2s !important;
}}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
  color: {accent} !important; background: {am} !important;
  border-bottom-color: {accent} !important;
}}
div[data-testid="stTabs"] button[role="tab"]:hover {{ color: {text} !important; }}

/* ── Buttons ── */
.stButton > button {{
  font-family: 'Space Grotesk', sans-serif !important;
  /* Fixed dark→mid teal gradient — readable in BOTH light and dark themes */
  background: linear-gradient(135deg, #1E4535 0%, #285A48 40%, #408A71 100%) !important;
  color: #E8F5EE !important;
  border: 1px solid rgba(64,138,113,.55) !important;
  font-weight: 700 !important;
  letter-spacing: .03em !important;
  padding: .55rem 1.65rem !important;
  border-radius: 9px !important;
  transition: transform .16s, box-shadow .22s, filter .18s !important;
  box-shadow: 0 2px 14px rgba(40,90,72,.45), inset 0 1px 0 rgba(255,255,255,.08) !important;
  font-size: .86rem !important;
  position: relative !important; overflow: hidden !important;
  text-shadow: 0 1px 2px rgba(0,0,0,.35) !important;
}}
.stButton > button::before {{
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,.10) 0%, transparent 60%);
  pointer-events: none; border-radius: 9px;
}}
.stButton > button::after {{
  content: ''; position: absolute; top: 0; left: -80%; width: 60%; height: 100%;
  background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,.15) 50%, transparent 60%);
  pointer-events: none;
}}
.stButton > button:hover {{
  background: linear-gradient(135deg, #285A48 0%, #408A71 55%, #52A888 100%) !important;
  box-shadow: 0 6px 28px rgba(64,138,113,.55), inset 0 1px 0 rgba(255,255,255,.12) !important;
  transform: translateY(-2px) !important;
  border-color: rgba(64,138,113,.8) !important;
}}
.stButton > button:hover::after {{ animation: shimmer .55s ease forwards; }}
.stButton > button:active {{
  transform: translateY(0) !important;
  box-shadow: 0 2px 8px rgba(40,90,72,.4) !important;
  filter: brightness(.96) !important;
}}
/* Ensure Streamlit doesn't override button text color */
.stButton > button p,
.stButton > button span,
.stButton > button div {{
  color: #E8F5EE !important;
  text-shadow: 0 1px 2px rgba(0,0,0,.35) !important;
}}

/* ── Secondary buttons (quiz options, soft actions) ── */
.stButton > button[kind="secondary"] {{
  background: {bg_card} !important;
  color: {text} !important;
  border: 1px solid {bdr} !important;
  box-shadow: none !important;
  text-shadow: none !important;
  font-weight: 500 !important;
  letter-spacing: .01em !important;
}}
.stButton > button[kind="secondary"]:hover {{
  background: {am} !important;
  border-color: {bdr_b} !important;
  color: {accent} !important;
  box-shadow: 0 2px 14px {ag} !important;
  transform: translateY(-1px) !important;
}}
.stButton > button[kind="secondary"]:active {{
  transform: translateY(0) !important;
  filter: brightness(.96) !important;
}}
.stButton > button[kind="secondary"] p,
.stButton > button[kind="secondary"] span,
.stButton > button[kind="secondary"] div {{
  color: inherit !important;
  text-shadow: none !important;
}}

/* ── Truth table ── */
.tt {{
  border-collapse: collapse; font-family: 'JetBrains Mono', monospace;
  font-size: .78rem; width: 100%; margin-top: .6rem;
}}
.tt th {{
  color: {accent}; text-align: center; padding: .42rem .8rem;
  border-bottom: 1px solid {bdr}; font-weight: 600; letter-spacing: .08em;
}}
.tt td {{
  text-align: center; padding: .3rem .8rem; color: {text_s};
  border-bottom: 1px solid {bdr}22;
}}
.tt tr:last-child td {{ border-bottom: none; }}
.tt .T {{ color: {accent}; font-weight: 600; }}
.tt .F {{ color: #EF5350; }}

/* ── Misc ── */
.divider {{
  height: 1px;
  background: linear-gradient(90deg, transparent, {bdr} 20%, {accent}44 50%, {bdr} 80%, transparent);
  margin: 2.2rem 0;
}}
.sec-tag {{
  font-family: 'JetBrains Mono', monospace; font-size: .62rem;
  color: {accent}; letter-spacing: .18em; opacity: .72; margin-bottom: .45rem;
}}
.badge {{
  font-family: 'JetBrains Mono', monospace; font-size: .68rem;
  color: {accent}; border: 1px solid {bdr};
  padding: .28rem 1rem; border-radius: 20px;
  background: {am}; display: inline-block;
  margin-bottom: 1.4rem; letter-spacing: .12em;
}}
.score-badge {{
  display: inline-flex; align-items: center; gap: .4rem;
  font-family: 'JetBrains Mono', monospace; font-size: .72rem;
  color: {accent}; border: 1px solid {bdr};
  padding: .22rem .8rem; border-radius: 20px; background: {am};
}}
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {scr}; border-radius: 4px; }}
.stRadio > div {{ gap: .4rem; }}
.stRadio label {{ color: {text_s} !important; font-size: .86rem !important; cursor: pointer; }}
.stRadio label p {{ color: {text_s} !important; }}
.stRadio label:hover {{ color: {text} !important; }}
.stRadio label:hover p {{ color: {text} !important; }}
details summary {{
  font-family: 'Space Grotesk', sans-serif; font-size: .9rem; color: {text_s}; cursor: pointer;
}}
details[open] summary {{ color: {accent}; }}
div[data-testid="stAlert"] {{ border-radius: 10px !important; border-left-width: 3px !important; }}

@media (max-width: 768px) {{
  .main .block-container {{ padding-left: 1rem !important; padding-right: 1rem !important; }}
  .hero-title {{ font-size: 2rem; }}
  .hero-stats {{ flex-wrap: wrap; gap: 1rem; }}
}}

/* ═══════════════════════════════════════════════════════════
   STREAMLIT NATIVE WIDGET OVERRIDES — full teal palette
   ═══════════════════════════════════════════════════════════ */

/* ── Slider ── */
[data-testid="stSlider"] [role="slider"] {{
  background: {accent} !important;
  border-color: {accent} !important;
  box-shadow: 0 0 0 4px {ag} !important;
  transition: box-shadow .18s !important;
}}
[data-testid="stSlider"] [role="slider"]:focus {{
  box-shadow: 0 0 0 6px {ag} !important;
}}
/* Slider filled track (baseweb inner bar) */
[data-baseweb="slider"] [class*="inner"] > div:first-child > div:first-child {{
  background: {accent} !important;
}}
[data-testid="stSlider"] div[class*="Thumb"] {{
  background: {accent} !important;
  border-color: {accent} !important;
}}
/* Slider tick / mark */
[data-baseweb="slider"] [class*="Tick"],
[data-baseweb="slider"] [class*="Mark"] {{
  background: {bdr_b} !important;
}}
/* Slider label / value text */
[data-testid="stSlider"] p,
[data-testid="stSlider"] div[class*="ValueLabel"] {{
  color: {accent} !important;
  font-family: 'JetBrains Mono', monospace !important;
}}

/* ── Radio ── */
/* Only kill the pill/box highlight Streamlit adds — leave circles alone */
[data-testid="stRadio"] div[role="radiogroup"] > div {{
  background: transparent !important;
  box-shadow: none !important;
}}
[data-baseweb="radio"] [class*="Root"] {{
  background: transparent !important;
  box-shadow: none !important;
}}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label div:first-child {{
  border-color: {bdr_b} !important;
  background: transparent !important;
  border-radius: 4px !important;
}}
[data-testid="stCheckbox"] label:has(input:checked) div:first-child {{
  background: {accent} !important;
  border-color: {accent} !important;
}}
[data-testid="stCheckbox"] p {{ color: {text_s} !important; }}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
  background: {am} !important;
  border: 1px solid {bdr_b} !important;
  border-radius: 6px !important;
}}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{ color: {accent} !important; }}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] button {{ color: {accent} !important; }}
[data-testid="stMultiSelect"] [role="option"][aria-selected="true"] {{
  background: {am} !important;
  color: {accent} !important;
}}
[data-testid="stMultiSelect"] [role="option"]:hover {{ background: {ag} !important; }}

/* ── Select dropdown options ── */
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"]:hover {{
  background: {am} !important;
}}
[data-baseweb="popover"] [role="option"][aria-selected="true"],
[data-baseweb="menu"] [role="option"][aria-selected="true"] {{
  background: {am} !important;
  color: {accent} !important;
}}
[data-baseweb="popover"],
[data-baseweb="menu"] {{
  background: {form_bg} !important;
  border: 1px solid {bdr} !important;
  border-radius: 8px !important;
}}
[data-baseweb="popover"] li, [data-baseweb="menu"] li {{
  color: {text} !important;
}}

/* ── Native st.progress ── */
[data-testid="stProgress"] > div {{
  background: {am} !important;
  border-radius: 6px !important;
}}
[data-testid="stProgress"] > div > div {{
  background: linear-gradient(90deg, {accent}, {accent2}) !important;
  border-radius: 6px !important;
  box-shadow: 0 0 8px {ag} !important;
}}

/* ── Metric ── */
[data-testid="stMetricLabel"] p {{
  color: {text_s} !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .62rem !important;
  letter-spacing: .12em !important;
  text-transform: uppercase !important;
}}
[data-testid="stMetricValue"] {{
  color: {accent} !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 800 !important;
}}
[data-testid="stMetricDelta"] svg {{ fill: {accent2} !important; }}
[data-testid="stMetricDelta"] p {{ color: {accent2} !important; }}
[data-testid="metric-container"] {{
  background: {bg_card} !important;
  border: 1px solid {bdr} !important;
  border-radius: 12px !important;
  padding: 1rem 1.2rem !important;
  transition: box-shadow .2s !important;
}}
[data-testid="metric-container"]:hover {{
  box-shadow: 0 4px 22px {ag} !important;
  border-color: {bdr_b} !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
  border: 1px solid {bdr} !important;
  border-radius: 10px !important;
  overflow: hidden !important;
  background: {bg_card} !important;
  transition: border-color .2s, box-shadow .2s !important;
  margin-bottom: .5rem !important;
}}
[data-testid="stExpander"]:hover {{
  border-color: {bdr_b} !important;
  box-shadow: 0 2px 18px {ag} !important;
}}
[data-testid="stExpander"] summary {{
  color: {text_s} !important;
  background: {bg_card} !important;
  padding: .75rem 1rem !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: .88rem !important;
  font-weight: 500 !important;
}}
[data-testid="stExpander"] details[open] > summary {{
  color: {accent} !important;
  border-bottom: 1px solid {bdr} !important;
  font-weight: 600 !important;
}}
[data-testid="stExpander"] details {{
  background: {bg_card} !important;
}}
[data-testid="stExpander"] details > div {{
  background: {bg_card} !important;
  color: {text} !important;
  padding: .7rem 1rem !important;
}}
[data-testid="stExpander"] details > div * {{ color: {text} !important; }}
[data-testid="stExpander"] details > div p {{ color: {text_s} !important; }}
/* Expander chevron icon */
[data-testid="stExpander"] svg {{
  fill: {accent} !important;
  stroke: {accent} !important;
}}

/* ── Alerts (st.info / st.success / st.warning / st.error) ── */
div[data-testid="stAlert"] {{
  border-radius: 10px !important;
  background: {am} !important;
  border: 1px solid {bdr} !important;
  border-left-width: 3px !important;
}}
div[data-testid="stAlert"] p, div[data-testid="stAlert"] * {{ color: {text} !important; }}
/* Keep success green, error red, warning amber */
div[data-testid="stAlert"][data-type="success"] {{ border-left-color: #4ADE80 !important; background: rgba(74,222,128,.06) !important; }}
div[data-testid="stAlert"][data-type="error"] {{ border-left-color: #EF5350 !important; background: rgba(239,83,80,.06) !important; }}
div[data-testid="stAlert"][data-type="warning"] {{ border-left-color: #FFC107 !important; background: rgba(255,193,7,.06) !important; }}
div[data-testid="stAlert"][data-type="info"] {{ border-left-color: {accent} !important; }}

/* ── Code / pre blocks ── */
.stCode > div, [data-testid="stCode"] {{
  background: {res_bg} !important;
  border: 1px solid {bdr} !important;
  border-radius: 8px !important;
}}
code:not([class]) {{
  background: {am} !important;
  color: {accent} !important;
  padding: .1em .35em !important;
  border-radius: 4px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .84em !important;
}}
pre code {{ background: transparent !important; color: {accent2} !important; }}

/* ── Number input buttons ── */
[data-testid="stNumberInput"] button {{
  background: {am} !important;
  border-color: {bdr} !important;
  color: {accent} !important;
  transition: background .18s !important;
}}
[data-testid="stNumberInput"] button:hover {{
  background: {ag} !important;
  border-color: {bdr_b} !important;
}}

/* ── Dataframe / table ── */
[data-testid="stDataFrame"] {{
  border: 1px solid {bdr} !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}}
[data-testid="stDataFrame"] th {{
  background: {am} !important;
  color: {accent} !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .74rem !important;
  letter-spacing: .06em !important;
}}
[data-testid="stDataFrame"] td {{ color: {text_s} !important; }}
[data-testid="stDataFrame"] tr:hover td {{ background: {am} !important; }}

/* ── Spinner ── */
[data-testid="stSpinner"] svg circle {{ stroke: {accent} !important; }}

/* ── Date input / time input ── */
[data-baseweb="datepicker"] [role="button"],
[data-baseweb="timepicker"] [role="button"] {{
  background: {form_bg} !important;
  border-color: {bdr} !important;
  color: {text} !important;
}}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {{
  background: {am} !important;
  color: {accent} !important;
  border: 1px solid {bdr} !important;
  font-family: 'Space Grotesk', sans-serif !important;
  border-radius: 9px !important;
  font-weight: 600 !important;
  transition: all .18s !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
  background: {ag} !important;
  border-color: {bdr_b} !important;
  transform: translateY(-1px) !important;
}}

/* ── Toast notifications ── */
[data-testid="toastContainer"] > div {{
  background: {bg_card} !important;
  border: 1px solid {bdr_b} !important;
  border-radius: 10px !important;
  color: {text} !important;
  box-shadow: 0 8px 32px {ag} !important;
}}

/* ── Tabs bottom border line ── */
div[data-testid="stTabs"] [role="tablist"] {{
  border-bottom: 1px solid {bdr} !important;
}}

/* ── Selectbox dropdown arrow ── */
[data-testid="stSelectbox"] svg {{ fill: {accent} !important; }}

/* ── st.columns vertical rule ── */
[data-testid="column"] + [data-testid="column"] {{
  border-left: none !important;
}}

/* ── General Streamlit body text overrides ── */
[data-testid="stMarkdownContainer"] p {{ color: {text_s}; line-height: 1.72; }}
[data-testid="stMarkdownContainer"] strong {{ color: {text} !important; }}
[data-testid="stMarkdownContainer"] a {{ color: {accent} !important; }}
[data-testid="stMarkdownContainer"] a:hover {{ color: {accent2} !important; }}

/* ── Horizontal rule ── */
hr {{ border: none; border-top: 1px solid {bdr} !important; margin: 1.5rem 0 !important; }}

@media (max-width: 768px) {{
  .main .block-container {{ padding-left: 1rem !important; padding-right: 1rem !important; }}
  .hero-title {{ font-size: 2rem; }}
  .hero-stats {{ flex-wrap: wrap; gap: 1rem; }}
}}
"""


# ---------------------------------------------------------------------------
# Nav pages
# ---------------------------------------------------------------------------
NAV_PAGES = [
    ("home",          "\u2302",  "Home",                   "",       ""),
    ("sets",          "\u2229",  "Set Theory",              "W2\u20133",   "Sets \u00b7 Venn \u00b7 Identities"),
    ("relations",     "\u2194",  "Relations",               "W4\u20138",   "Properties \u00b7 Closures \u00b7 Posets"),
    ("logic",         "\u2227",  "Propositional Logic",     "W9\u201311",  "Truth Tables \u00b7 Predicates"),
    ("inference",     "\u2234",  "Rules of Inference",      "W12\u201313", "Modus Ponens \u00b7 Arguments"),
    ("proofs",        "\u25a1",  "Proof Methods",            "W14\u201315", "Direct \u00b7 Contradiction"),
    ("induction",     "\u2211",  "Mathematical Induction",   "W16",    "Base Case \u00b7 Inductive Step"),
    ("sequences",     "\u224b",  "Sequences",                "W8",     "Arithmetic \u00b7 Fibonacci"),
    ("combinatorics", "\u2295",  "Combinatorics",             "",       "Perms \u00b7 Combinations"),
    ("graphs",        "\u25c7",  "Graph Theory",             "",       "Vertices \u00b7 Eulerian Paths"),
    ("ai",            "\u26a1",  "AI Problem Solver",        "",       "Ask Anything"),
    ("study",         "\U0001f4da", "Study Hub",             "",       "Learn \u00b7 Quiz \u00b7 Track Progress"),
]


def inject_css(theme: str = "dark") -> None:
    css = _make_css(theme)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(PARTICLES_JS, unsafe_allow_html=True)


def render_nav(current_section: str, theme: str = "dark") -> None:
    current_label = next((lbl for k, _, lbl, *__ in NAV_PAGES if k == current_section), "Home")

    tp = f"&theme={theme}" if theme == "light" else ""
    links_html = ""
    for k, ic, lb, wk, sb in NAV_PAGES:
        ac = "sn-active" if current_section == k else ""
        wk_html = f'<span class="sn-week">{wk}</span>' if wk else ""
        sb_html = f'<span class="sn-sub">{sb}</span>' if sb else ""
        links_html += (
            f'<a href="?page={k}{tp}" class="{ac}" target="_self">'
            f'<span class="sn-icon">{ic}</span>'
            f'<span class="sn-label">{lb}{sb_html}</span>'
            f'{wk_html}</a>'
        )

    other_theme = "light" if theme == "dark" else "dark"
    theme_icon  = "\u2600\ufe0f" if theme == "dark" else "\U0001f319"
    otp = f"&theme={other_theme}" if other_theme == "light" else ""

    st.markdown(f"""
<input type="checkbox" id="ds-nav-toggle">
<label for="ds-nav-toggle" id="ds-overlay"></label>
<nav id="ds-sidenav">
  <div class="sn-header">
    <div class="sn-logo">discrete<span>\u00b7</span>academy</div>
    <div class="sn-tagline">MASTER DISCRETE MATHEMATICS</div>
  </div>
  <div class="sn-group">Course Modules</div>
  <div class="sn-links">{links_html}</div>
  <div class="sn-footer">\u2200x\u2208\U0001d54c [ Study(x) \u2192 Excel(x) ]<br>BSAI \u00b7 CS Department</div>
</nav>
<div id="ds-topbar">
  <label for="ds-nav-toggle" id="ds-hamburger">
    <span class="h-bar"></span><span class="h-bar"></span><span class="h-bar"></span>
  </label>
  <div class="tb-logo">discrete<span>\u00b7</span>academy</div>
  <span class="tb-sep">/</span>
  <div class="tb-page">{current_label}</div>
  <div class="tb-spacer"></div>
  <a href="?page={current_section}{otp}" class="tb-theme-btn" target="_self" title="Toggle theme">{theme_icon}</a>
  <div class="tb-pill">\u2200x\u2208\U0001d54c</div>
</div>
""", unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style='text-align:center;padding:2rem 0 1.2rem;'>
  <div style='font-family:"Syne",sans-serif;font-size:1.05rem;font-weight:800;
  background:linear-gradient(120deg,#408A71,#B0E4CC);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-.01em;'>
    discrete \u00b7 academy
  </div>
  <div style='font-family:"JetBrains Mono",monospace;font-size:.58rem;
  color:#408A71;margin-top:.5rem;letter-spacing:.1em;opacity:.7;'>
    MASTERING THE MATHEMATICS THAT POWERS COMPUTATION
  </div>
  <div style='font-family:"Space Grotesk",sans-serif;font-size:.74rem;color:#6EADA0;margin-top:.9rem;'>
    <span style='color:#B0E4CC;opacity:.8;'>Farhan Haroon</span> \u00b7 FA25-BSAI-0060 &nbsp;|&nbsp;
    <span style='color:#B0E4CC;opacity:.8;'>Huzaifa Zaki</span> \u00b7 FA25-BSAI-0051 &nbsp;|&nbsp;
    <span style='color:#B0E4CC;opacity:.8;'>Bissam ul Haq</span> \u00b7 FA25-BSAI-0076 &nbsp;|&nbsp;
    <span style='color:#B0E4CC;opacity:.8;'>Aaleen</span> \u00b7 FA25-BSAI-0077
  </div>
  <div style='margin-top:.9rem;font-size:.62rem;color:#285A48;'>
    \u2200x [ Discrete(x) \u2192 Beautiful(x) ] \u2014 BSAI \u00b7 CS Department
  </div>
</div>
""", unsafe_allow_html=True)
