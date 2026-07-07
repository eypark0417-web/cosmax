import base64
import csv
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).parent
IMAGE_PATH = BASE_DIR / "cosmax_products.jpg"
CSV_PATH = BASE_DIR / "sample_clients.csv"

st.set_page_config(
    page_title="니즈오션 | 마케팅 실무자들의 바다",
    page_icon="🌊",
    layout="wide",
)

# Streamlit 기본 여백/메뉴를 숨기고, 페이지 iframe이 브라우저 화면 전체를 채우도록 함.
# iframe 높이를 100vh로 고정해 스크롤이 iframe 내부에서 일어나게 해야
# sticky 헤더·앵커 이동(#섹션)·등장 애니메이션이 정상 동작한다.
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header[data-testid="stHeader"] {display: none;}
        footer {visibility: hidden;}
        [data-testid="stAppViewContainer"] > .main,
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        .stApp {overflow: hidden;}
        iframe {
            width: 100% !important;
            height: 100vh !important;
            border: none !important;
            display: block;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def esc(value: str) -> str:
    return html.escape(str(value).strip())


@st.cache_data(show_spinner=False)
def load_clients():
    """sample_clients.csv → 고객사 목록. 하나의 웹페이지 각 섹션에서 공용으로 쓴다."""
    clients = []
    if not CSV_PATH.exists():
        return clients
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            raw_name = (row.get("고객사 이름") or "").strip()
            direction = (row.get("고객사 사업보고서") or "").strip()
            products = (row.get("고객사 주요 브랜딩 제품") or "").strip()
            needs = (row.get("고객사 주요 니즈") or "").strip()
            if not raw_name:
                continue

            # "롬앤(rom&nd)" → 한글명 + 영문명 분리
            name_ko, english = raw_name, ""
            if "(" in raw_name and raw_name.endswith(")"):
                name_ko = raw_name.split("(", 1)[0].strip()
                english = raw_name.split("(", 1)[1][:-1].strip()

            clients.append(
                {
                    "id": f"client-{i}",
                    "name": name_ko,
                    "english": english,
                    "direction": direction,
                    "products": [p.strip() for p in products.split(",") if p.strip()],
                    "needs": [n.strip() for n in needs.split(",") if n.strip()],
                }
            )
    return clients


@st.cache_data(show_spinner=False)
def hero_image_uri() -> str:
    if IMAGE_PATH.exists():
        img_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("utf-8")
        return f"data:image/jpeg;base64,{img_b64}"
    return ""


def preview(text: str, length: int = 46) -> str:
    text = text.strip()
    return esc(text if len(text) <= length else text[:length] + "…")


def chevron_svg() -> str:
    return (
        '<svg class="chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'
    )


def initials(name: str) -> str:
    return esc(name[:2])


def build_needs_section(clients) -> str:
    items = []
    for c in clients:
        needs_list = "".join(
            f'<div class="deep-item"><span class="num">{i + 1}</span>'
            f'<div><h4 class="kr">{esc(n)}</h4></div></div>'
            for i, n in enumerate(c["needs"])
        )
        chips = "".join(f"<span>{esc(p)}</span>" for p in c["products"])
        needs_summary = ", ".join(c["needs"])
        items.append(
            f"""
            <details class="acc" data-name="{esc(c['name'])} {esc(c['english'])}">
              <summary>
                <div class="acc-left">
                  <div class="avatar rose">{initials(c['name'])}</div>
                  <div class="acc-title">
                    <h3 class="kr">{esc(c['name'])} <span class="tag sky">{esc(c['english'])}</span></h3>
                    <div class="acc-summary">{preview(needs_summary)}</div>
                  </div>
                </div>
                {chevron_svg()}
              </summary>
              <div class="acc-body">
                <div class="deep-list">{needs_list}</div>
                <div class="product-chips">{chips}</div>
              </div>
            </details>
            """
        )
    return "".join(items)


def build_direction_section(clients) -> str:
    items = []
    for c in clients:
        chips = "".join(f"<span>{esc(p)}</span>" for p in c["products"])
        items.append(
            f"""
            <details class="acc" data-name="{esc(c['name'])} {esc(c['english'])}">
              <summary>
                <div class="acc-left">
                  <div class="avatar sky">{initials(c['name'])}</div>
                  <div class="acc-title">
                    <h3 class="kr">{esc(c['name'])} <span class="tag rose">{esc(c['english'])}</span></h3>
                    <div class="acc-summary">{preview(c['direction'])}</div>
                  </div>
                </div>
                {chevron_svg()}
              </summary>
              <div class="acc-body">
                <p class="direction-full">{esc(c['direction'])}</p>
                <div class="product-chips">{chips}</div>
              </div>
            </details>
            """
        )
    return "".join(items)


def build_ppt_section(clients) -> str:
    cards = []
    clock = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/>'
        '<path d="M12 7v5l3 3"/></svg>'
    )
    for c in clients:
        chips = "".join(f"<span>{esc(p)}</span>" for p in c["products"])
        cards.append(
            f"""
            <div class="ppt-card">
              <div class="ppt-card-head">
                <div class="avatar gold">{initials(c['name'])}</div>
                <h3 class="kr">{esc(c['name'])} <span class="tag rose">{esc(c['english'])}</span></h3>
              </div>
              <div class="ppt-status">{clock}<span>제안서 양식 준비 중입니다</span></div>
              <div class="product-chips">{chips}</div>
            </div>
            """
        )
    return "".join(cards)


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>니즈오션 | 마케팅 실무자들의 바다</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --rose:#C7AEE3; --rose-soft:#F3EEFB; --rose-deep:#8A6BB0;
    --sky:#A9D6EA; --sky-soft:#EDF7FB; --sky-deep:#5F9BBF;
    --gold:#D6C7ED; --gold-soft:#F6F1FB; --gold-deep:#7C79B8;
    --pink:var(--rose); --pink-soft:var(--rose-soft);
    --yellow:var(--gold); --yellow-soft:var(--gold-soft);
    --ink:#2B2B3D; --ink-soft:#6B6B80; --white:#FFFFFF; --cream:#FCFBFF;
    --shadow: 0 10px 30px rgba(43,43,61,0.06);
    --radius-lg: 32px; --radius-md: 20px; --radius-sm: 14px;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  html{scroll-behavior:smooth;overflow-x:hidden;}
  body{
    font-family:'Malgun Gothic','Noto Sans KR','Apple SD Gothic Neo',sans-serif;
    color:var(--ink); background:var(--cream); overflow-x:hidden; max-width:100%;
    -webkit-font-smoothing:antialiased;
  }
  .kr{font-family:'Malgun Gothic','Noto Sans KR','Apple SD Gothic Neo',sans-serif;font-weight:700;}
  img,svg{display:block;max-width:100%;}
  a{text-decoration:none;color:inherit;}
  ul{list-style:none;}
  button{font-family:inherit;border:none;background:none;cursor:pointer;}
  .container{max-width:1180px;margin:0 auto;padding:0 24px;}

  .bubble{position:absolute;border-radius:50%;opacity:0.4;filter:blur(3px);
    animation:float 11s ease-in-out infinite;pointer-events:none;z-index:0;}
  @keyframes float{0%,100%{transform:translateY(0) translateX(0) scale(1);}
    50%{transform:translateY(-26px) translateX(10px) scale(1.06);}}
  @keyframes floatSlow{0%,100%{transform:translateY(0) translateX(0);}
    50%{transform:translateY(-16px) translateX(-14px);}}

  header{position:sticky;top:0;z-index:100;background:rgba(255,252,245,0.9);
    backdrop-filter:blur(10px);border-bottom:1px solid rgba(43,43,61,0.06);}
  .nav-wrap{display:flex;align-items:center;justify-content:space-between;height:76px;}
  .logo{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:700;
    letter-spacing:0.3px;color:var(--ink);}
  .logo span.brand{background:linear-gradient(90deg,var(--rose-deep),var(--gold-deep));
    -webkit-background-clip:text;background-clip:text;color:transparent;}
  nav.main-nav ul{display:flex;gap:34px;align-items:center;}
  nav.main-nav a{font-size:15px;font-weight:600;color:var(--ink-soft);position:relative;
    padding:6px 0;transition:color .2s;}
  nav.main-nav a:hover{color:var(--ink);}
  nav.main-nav a::after{content:'';position:absolute;left:0;bottom:0;width:0;height:2px;
    background:var(--pink);transition:width .25s;}
  nav.main-nav a:hover::after{width:100%;}
  .cta-btn{background:linear-gradient(135deg,var(--rose-deep),var(--gold-deep));color:var(--white);
    font-weight:600;font-size:14.5px;padding:12px 24px;border-radius:999px;
    box-shadow:0 8px 18px rgba(201,122,147,0.28);transition:transform .2s;white-space:nowrap;}
  .cta-btn:hover{transform:translateY(-2px);}
  .hamburger{display:none;flex-direction:column;gap:5px;padding:8px;z-index:101;}
  .hamburger span{width:24px;height:3px;border-radius:3px;background:var(--ink);transition:all .3s;}
  .hamburger.active span:nth-child(1){transform:translateY(8px) rotate(45deg);}
  .hamburger.active span:nth-child(2){opacity:0;}
  .hamburger.active span:nth-child(3){transform:translateY(-8px) rotate(-45deg);}

  .hero{position:relative;padding:72px 0 110px;overflow:hidden;
    background:radial-gradient(circle at 15% 20%, var(--pink-soft) 0%, transparent 45%),
               radial-gradient(circle at 85% 10%, var(--sky-soft) 0%, transparent 45%),
               radial-gradient(circle at 60% 90%, var(--yellow-soft) 0%, transparent 50%),
               var(--cream);}
  .hero-photo{position:absolute;inset:0;background-image:url('__HERO_IMAGE_URI__');
    background-size:cover;background-position:center 30%;opacity:0.55;z-index:0;}
  .hero-photo::after{content:'';position:absolute;inset:0;
    background:radial-gradient(circle at 50% 38%, rgba(252,251,255,0.35) 0%, var(--cream) 96%);}
  .hero-inner{position:relative;z-index:2;text-align:center;max-width:760px;margin:0 auto;}
  .hero-badge{display:inline-flex;align-items:center;gap:8px;background:var(--white);
    border:1px solid var(--rose-soft);padding:8px 20px;border-radius:999px;font-size:13px;
    font-weight:600;color:var(--rose-deep);box-shadow:var(--shadow);margin-bottom:26px;}
  .hero-badge .dot{color:var(--gold-deep);font-size:11px;}
  h1.hero-title{font-size:clamp(26px,4.4vw,46px);line-height:1.4;color:var(--ink);margin-bottom:20px;
    text-shadow:0 0 18px rgba(252,251,255,0.9),0 0 40px rgba(252,251,255,0.7);}
  h1.hero-title .line{display:inline-block;}
  h1.hero-title .highlight{background:linear-gradient(90deg,var(--rose-deep),var(--gold-deep),var(--sky-deep));
    background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;
    animation:gradientShift 5s ease infinite;}
  @keyframes gradientShift{0%{background-position:0% 50%;}50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}}
  .hero-desc{font-size:clamp(15px,1.8vw,18px);color:var(--ink-soft);line-height:1.7;margin-bottom:40px;
    text-shadow:0 0 16px rgba(252,251,255,0.9),0 0 30px rgba(252,251,255,0.7);}
  .hero-search{display:flex;align-items:center;max-width:520px;margin:0 auto 22px;background:var(--white);
    border-radius:999px;padding:6px 6px 6px 22px;box-shadow:0 14px 34px rgba(43,43,61,0.12);
    border:2px solid transparent;transition:border-color .2s;}
  .hero-search:focus-within{border-color:var(--pink);}
  .hero-search input{flex:1;border:none;outline:none;font-size:15px;font-family:inherit;
    padding:12px 8px;background:transparent;color:var(--ink);}
  .hero-search input::placeholder{color:#B8B8C8;}
  .hero-search button{background:linear-gradient(135deg,var(--rose-deep),var(--sky-deep));
    color:var(--white);font-weight:700;font-size:14px;padding:12px 22px;border-radius:999px;
    white-space:nowrap;transition:transform .2s;}
  .hero-search button:hover{transform:scale(1.04);}
  .hero-tags{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:44px;}
  .hero-tags span{font-size:12.5px;font-weight:600;color:var(--ink-soft);background:var(--white);
    padding:6px 14px;border-radius:999px;border:1px solid rgba(43,43,61,0.07);}
  .hero-actions{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
  .btn-outline{padding:14px 28px;border-radius:999px;font-weight:700;font-size:15px;
    border:2px solid var(--ink);color:var(--ink);transition:all .2s;}
  .btn-outline:hover{background:var(--ink);color:var(--white);}
  .btn-primary{padding:14px 28px;border-radius:999px;font-weight:700;font-size:15px;
    background:linear-gradient(135deg,var(--rose-deep),var(--gold-deep));color:var(--white);
    box-shadow:0 10px 24px rgba(201,122,147,0.28);transition:transform .2s;}
  .btn-primary:hover{transform:translateY(-2px);}

  .wave-divider{display:block;width:100%;line-height:0;}
  .wave-divider svg{width:100%;height:auto;}

  section.block{padding:74px 0;}
  section.block.alt{background:var(--white);}
  .section-head{text-align:center;max-width:660px;margin:0 auto 46px;}
  .section-tag{font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
    color:var(--sky-deep);margin-bottom:12px;}
  .section-title{font-size:clamp(26px,3.6vw,38px);margin-bottom:14px;}
  .section-desc{color:var(--ink-soft);font-size:16px;line-height:1.7;}

  .feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;}
  .feature-card{position:relative;border-radius:var(--radius-lg);padding:38px 30px 34px;overflow:hidden;
    box-shadow:var(--shadow);transition:transform .3s, box-shadow .3s;isolation:isolate;}
  .feature-card:hover{transform:translateY(-8px) rotate(-0.4deg);box-shadow:0 20px 40px rgba(43,43,61,0.15);}
  .feature-card.pink{background:linear-gradient(160deg,var(--pink-soft) 0%, #FFF 65%);}
  .feature-card.sky{background:linear-gradient(160deg,var(--sky-soft) 0%, #FFF 65%);}
  .feature-card.yellow{background:linear-gradient(160deg,var(--yellow-soft) 0%, #FFF 65%);}
  .feature-icon{width:60px;height:60px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;margin-bottom:24px;background:var(--white);box-shadow:0 8px 18px rgba(43,43,61,0.08);}
  .feature-icon svg{width:26px;height:26px;}
  .feature-num{position:absolute;top:28px;right:28px;font-family:'Poppins',sans-serif;font-weight:800;
    font-size:14px;color:rgba(43,43,61,0.16);}
  .feature-card h3{font-size:21px;margin-bottom:12px;}
  .feature-card p{color:var(--ink-soft);font-size:14.5px;line-height:1.7;margin-bottom:18px;}
  .feature-list{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}
  .feature-list li{font-size:13.5px;color:var(--ink);display:flex;align-items:center;gap:8px;font-weight:600;}
  .feature-list li::before{content:'—';color:var(--gold-deep);font-weight:700;}
  .feature-link{font-weight:700;font-size:14px;color:var(--ink);display:inline-flex;align-items:center;
    gap:6px;transition:gap .2s;}
  .feature-link:hover{gap:10px;}

  .acc-list{max-width:900px;margin:0 auto;}
  .acc{background:var(--white);border-radius:var(--radius-md);box-shadow:var(--shadow);
    margin-bottom:14px;overflow:hidden;}
  .acc summary{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:20px 24px;
    cursor:pointer;list-style:none;}
  .acc summary::-webkit-details-marker{display:none;}
  .acc-left{display:flex;align-items:center;gap:14px;min-width:0;}
  .avatar{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    font-weight:800;font-family:'Poppins',sans-serif;font-size:14px;flex-shrink:0;}
  .avatar.rose{background:var(--rose-soft);color:var(--rose-deep);}
  .avatar.sky{background:var(--sky-soft);color:var(--sky-deep);}
  .avatar.gold{background:var(--gold-soft);color:var(--gold-deep);}
  .acc-title{min-width:0;}
  .acc-title h3{font-size:16px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
  .tag{font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;}
  .tag.sky{color:var(--sky-deep);background:var(--sky-soft);}
  .tag.rose{color:var(--rose-deep);background:var(--rose-soft);}
  .acc-summary{font-size:12.5px;color:var(--ink-soft);margin-top:4px;overflow:hidden;
    text-overflow:ellipsis;white-space:nowrap;}
  .chevron{transition:transform .25s;flex-shrink:0;color:var(--ink-soft);}
  .acc[open] .chevron{transform:rotate(180deg);}
  .acc-body{padding:0 24px 24px;}
  .deep-list{display:flex;flex-direction:column;gap:10px;}
  .deep-item{display:flex;gap:12px;align-items:flex-start;background:var(--cream);border-radius:14px;
    padding:13px 16px;}
  .deep-item .num{font-family:'Poppins',sans-serif;font-weight:800;font-size:12.5px;color:var(--rose-deep);
    background:var(--rose-soft);width:24px;height:24px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;flex-shrink:0;margin-top:1px;}
  .deep-item h4{font-size:14px;}
  .direction-full{font-size:14.5px;line-height:1.85;color:var(--ink);margin-bottom:16px;}
  .product-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;}
  .product-chips span{font-size:12px;font-weight:600;color:var(--ink);background:var(--gold-soft);
    padding:5px 12px;border-radius:999px;}

  .ppt-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;max-width:900px;margin:0 auto;}
  .ppt-card{background:var(--white);border-radius:var(--radius-md);box-shadow:var(--shadow);padding:22px;}
  .ppt-card-head{display:flex;align-items:center;gap:12px;margin-bottom:12px;}
  .ppt-card h3{font-size:15px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
  .ppt-status{display:flex;align-items:center;gap:8px;background:var(--cream);border-radius:12px;
    padding:12px 14px;margin-bottom:12px;}
  .ppt-status svg{width:16px;height:16px;color:var(--gold-deep);flex-shrink:0;}
  .ppt-status span{font-size:12.5px;color:var(--ink-soft);}

  .audience{background:linear-gradient(180deg,var(--cream), var(--sky-soft));position:relative;overflow:hidden;}
  .audience-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;}
  .audience-card{background:var(--white);border-radius:var(--radius-md);padding:28px;display:flex;gap:18px;
    align-items:flex-start;box-shadow:var(--shadow);}
  .audience-badge{width:50px;height:50px;border-radius:14px;flex-shrink:0;display:flex;align-items:center;
    justify-content:center;font-size:11px;font-weight:700;font-family:'Poppins',sans-serif;}
  .audience-badge.rose{background:var(--rose-soft);color:var(--rose-deep);}
  .audience-badge.sky{background:var(--sky-soft);color:var(--sky-deep);}
  .audience-badge.gold{background:var(--gold-soft);color:var(--gold-deep);}
  .audience-card h4{font-size:17px;margin-bottom:6px;}
  .audience-card p{color:var(--ink-soft);font-size:14px;line-height:1.6;}

  .cta-band{margin:0 auto 90px;max-width:1100px;padding:60px 40px;border-radius:var(--radius-lg);
    background:linear-gradient(120deg,var(--rose),var(--sky),var(--gold));background-size:220% 220%;
    animation:gradientShift 10s ease infinite;text-align:center;color:var(--white);
    box-shadow:0 20px 50px rgba(201,122,147,0.28);}
  .cta-band h2{font-size:clamp(24px,3.4vw,34px);margin-bottom:14px;}
  .cta-band p{font-size:15.5px;margin-bottom:28px;opacity:0.95;}
  .cta-band .btn-white{background:var(--white);color:var(--rose-deep);padding:15px 34px;border-radius:999px;
    font-weight:800;font-size:15.5px;display:inline-block;transition:transform .2s;
    box-shadow:0 12px 26px rgba(0,0,0,0.12);}
  .cta-band .btn-white:hover{transform:translateY(-3px) scale(1.02);}

  footer{background:var(--ink);color:#C9C9DA;padding:56px 0 28px;}
  .footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:34px;margin-bottom:40px;}
  .footer-brand .logo{color:var(--white);margin-bottom:12px;}
  .footer-brand p{font-size:13.5px;line-height:1.7;color:#9B9BB0;max-width:280px;}
  .footer-col h5{color:var(--white);font-size:14px;margin-bottom:14px;font-weight:700;}
  .footer-col ul{display:flex;flex-direction:column;gap:10px;}
  .footer-col a{font-size:13.5px;color:#9B9BB0;transition:color .2s;}
  .footer-col a:hover{color:var(--white);}
  .footer-bottom{border-top:1px solid rgba(255,255,255,0.08);padding-top:22px;display:flex;
    justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:12.5px;color:#7A7A90;}

  @media (max-width:900px){
    .feature-grid{grid-template-columns:1fr;}
    .audience-grid{grid-template-columns:1fr;}
    .ppt-grid{grid-template-columns:1fr;}
    .footer-grid{grid-template-columns:1fr 1fr;}
  }
  @media (max-width:760px){
    nav.main-nav{position:fixed;top:76px;left:0;right:0;background:var(--white);flex-direction:column;
      padding:20px 24px 28px;box-shadow:0 12px 24px rgba(43,43,61,0.1);transform:translateY(-130%);
      opacity:0;transition:transform .3s ease, opacity .3s ease;z-index:99;}
    nav.main-nav.open{transform:translateY(0);opacity:1;}
    nav.main-nav ul{flex-direction:column;align-items:flex-start;gap:18px;width:100%;}
    .hamburger{display:flex;}
    .header-cta{display:none;}
    .hero{padding:48px 0 80px;}
    .hero-search{flex-direction:column;align-items:stretch;padding:14px;border-radius:22px;gap:10px;}
    .hero-search button{width:100%;justify-content:center;}
    .cta-band{padding:44px 24px;border-radius:24px;}
    .footer-grid{grid-template-columns:1fr;gap:26px;}
  }
</style>
</head>
<body>

<header>
  <div class="container nav-wrap">
    <a href="#top" class="logo"><span>니즈<span class="brand">오션</span></span></a>
    <nav class="main-nav" id="mainNav">
      <ul>
        <li><a href="#needs">고객사 NEEDS</a></li>
        <li><a href="#direction">사업방향</a></li>
        <li><a href="#ppt">고객사 PPT</a></li>
        <li><a href="#audience">이용대상</a></li>
      </ul>
    </nav>
    <a href="#needs" class="cta-btn header-cta">바로 둘러보기</a>
    <button class="hamburger" id="hamburger" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
  </div>
</header>

<section class="hero" id="top">
  <div class="hero-photo"></div>
  <span class="bubble" style="width:70px;height:70px;background:var(--pink);left:6%;top:18%;"></span>
  <span class="bubble" style="width:40px;height:40px;background:var(--sky);left:80%;top:12%;animation-delay:1.5s;"></span>
  <span class="bubble" style="width:26px;height:26px;background:var(--yellow);left:88%;top:55%;animation-delay:0.8s;"></span>
  <span class="bubble" style="width:54px;height:54px;background:var(--sky);left:12%;top:70%;animation-delay:2.2s;"></span>

  <div class="container hero-inner">
    <span class="hero-badge"><span class="dot">◆</span> 마케팅 실무자를 위한 인사이트 허브</span>
    <h1 class="hero-title kr">
      <span class="line">국내외 고객사의 마음을 담은</span><br>
      <span class="line highlight">마케팅 실무자들의 바다</span>
    </h1>
    <p class="hero-desc">
      고객사의 니즈와 사업방향, PPT 제안 양식까지 —<br>
      흩어져 있던 모든 정보를 니즈오션 하나에 담았습니다.
    </p>

    <form class="hero-search" id="heroSearchForm" autocomplete="off">
      <input type="text" id="heroSearchInput" placeholder="고객사명, 브랜드로 검색해보세요 (예: 롬앤, CLIO)">
      <button type="submit">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" style="display:inline-block;vertical-align:-2px;margin-right:5px;">
          <circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>검색
      </button>
    </form>

    <div class="hero-tags">
      <span>#고객사NEEDS</span><span>#사업방향분석</span><span>#PPT제안양식</span><span>#국내외실무자</span>
    </div>

    <div class="hero-actions">
      <a href="#needs" class="btn-primary">둘러보러 가기 →</a>
      <a href="#audience" class="btn-outline">누가 쓰나요?</a>
    </div>
  </div>
</section>

<div class="wave-divider">
  <svg viewBox="0 0 1440 100" preserveAspectRatio="none">
    <path fill="#FFFFFF" d="M0,40 C240,100 480,0 720,30 C960,60 1200,100 1440,40 L1440,100 L0,100 Z"></path>
  </svg>
</div>

<section class="block alt">
  <div class="container">
    <div class="section-head">
      <div class="section-tag">CORE FEATURES</div>
      <h2 class="section-title kr">니즈오션에 있는 세 가지 파도</h2>
      <p class="section-desc">고객사를 이해하는 순간부터 제안서를 완성하는 순간까지, 실무 흐름 그대로 담았습니다.</p>
    </div>
    <div class="feature-grid">
      <div class="feature-card pink">
        <span class="feature-num">01</span>
        <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="#8A6BB0" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20.5s-7.5-4.6-9.5-9.2C1.2 8.2 3 5 6.3 5c2 0 3.4 1.2 4.2 2.4C11.3 6.2 12.7 5 14.7 5 18 5 19.8 8.2 18.5 11.3 16.5 15.9 12 20.5 12 20.5Z"/></svg></div>
        <h3 class="kr">고객사 NEEDS</h3>
        <p>고객사가 진짜 원하는 것이 무엇인지, 성향과 선호를 한눈에 파악하세요.</p>
        <ul class="feature-list"><li>고객사별 니즈 데이터</li><li>선호 톤앤매너</li><li>주요 브랜딩 제품</li></ul>
        <a href="#needs" class="feature-link">니즈 둘러보기 →</a>
      </div>
      <div class="feature-card sky">
        <span class="feature-num">02</span>
        <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="#5F9BBF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M14.8 9.2 12.9 14.8 9.2 14.8 11.1 9.2Z"/></svg></div>
        <h3 class="kr">고객사 사업방향</h3>
        <p>고객사가 나아가는 방향을 이해하면 제안의 설득력이 달라집니다.</p>
        <ul class="feature-list"><li>사업 전략 요약</li><li>시장 포지셔닝</li><li>카테고리 동향</li></ul>
        <a href="#direction" class="feature-link">방향성 살펴보기 →</a>
      </div>
      <div class="feature-card yellow">
        <span class="feature-num">03</span>
        <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="#7C79B8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="4.5" width="17" height="12" rx="1.6"/><path d="M9 20.5h6M12 16.5v4"/></svg></div>
        <h3 class="kr">고객사 PPT</h3>
        <p>고객사가 선호하는 제안서 양식을 그대로, 바로 활용 가능한 형태로.</p>
        <ul class="feature-list"><li>고객사별 제안서 양식</li><li>국내·해외 구분</li><li>다운로드·편집</li></ul>
        <a href="#ppt" class="feature-link">PPT 양식 보기 →</a>
      </div>
    </div>
  </div>
</section>

<section class="block" id="needs">
  <div class="container">
    <div class="section-head">
      <div class="section-tag">CLIENT NEEDS</div>
      <h2 class="section-title kr">고객사 NEEDS</h2>
      <p class="section-desc">니즈오션에 등록된 고객사들이 지금 가장 필요로 하는 것을 정리했습니다. 항목을 눌러 자세히 확인해보세요.</p>
    </div>
    <div class="acc-list" id="needsList">__NEEDS_ITEMS__</div>
  </div>
</section>

<section class="block alt" id="direction">
  <div class="container">
    <div class="section-head">
      <div class="section-tag">BUSINESS DIRECTION</div>
      <h2 class="section-title kr">고객사 사업방향</h2>
      <p class="section-desc">고객사별 2026년 사업방향과 전략을 정리했습니다. 항목을 눌러 상세 내용을 확인해보세요.</p>
    </div>
    <div class="acc-list" id="directionList">__DIRECTION_ITEMS__</div>
  </div>
</section>

<section class="block" id="ppt">
  <div class="container">
    <div class="section-head">
      <div class="section-tag">PROPOSAL TEMPLATES</div>
      <h2 class="section-title kr">고객사 PPT</h2>
      <p class="section-desc">고객사별 제안서 양식을 준비하고 있습니다. 주요 브랜딩 제품을 참고해 제안을 구성해보세요.</p>
    </div>
    <div class="ppt-grid">__PPT_ITEMS__</div>
  </div>
</section>

<section class="block audience" id="audience">
  <span class="bubble" style="width:36px;height:36px;background:var(--yellow);left:4%;top:14%;animation:floatSlow 7s ease-in-out infinite;"></span>
  <span class="bubble" style="width:50px;height:50px;background:var(--pink);left:92%;top:70%;animation:floatSlow 8s ease-in-out infinite;"></span>
  <div class="container">
    <div class="section-head">
      <div class="section-tag">WHO IT'S FOR</div>
      <h2 class="section-title kr">이런 분들이 니즈오션과 함께합니다</h2>
      <p class="section-desc">국내는 물론 해외 고객사를 상대하는 마케팅 실무자 모두를 위해 만들었습니다.</p>
    </div>
    <div class="audience-grid">
      <div class="audience-card"><span class="audience-badge rose">KR</span><div><h4 class="kr">국내 마케팅 실무자</h4><p>여러 국내 고객사를 동시에 담당하며 각 사의 니즈와 제안 양식을 빠르게 파악해야 하는 담당자에게 꼭 맞습니다.</p></div></div>
      <div class="audience-card"><span class="audience-badge sky">GL</span><div><h4 class="kr">해외 마케팅 실무자</h4><p>해외 고객사의 문화적 성향과 사업방향까지 이해해야 하는 글로벌 담당자를 위한 인사이트를 제공합니다.</p></div></div>
      <div class="audience-card"><span class="audience-badge gold">PPT</span><div><h4 class="kr">제안서 준비 담당자</h4><p>매번 새로 만드는 대신, 고객사가 선호하는 PPT 양식을 그대로 가져와 제안 시간을 단축하세요.</p></div></div>
      <div class="audience-card"><span class="audience-badge rose">NEW</span><div><h4 class="kr">신규 고객사 담당자</h4><p>처음 맡게 된 고객사라도 니즈오션의 데이터를 통해 빠르게 성향을 파악하고 신뢰를 쌓을 수 있습니다.</p></div></div>
    </div>
  </div>
</section>

<div class="container">
  <div class="cta-band">
    <h2 class="kr">지금, 니즈오션과 함께 시작해보세요</h2>
    <p>고객사의 니즈부터 PPT까지, 마케팅 실무의 모든 파도를 니즈오션과 함께 타보세요.</p>
    <a href="#needs" class="btn-white">고객사 둘러보기</a>
  </div>
</div>

<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="#top" class="logo"><span>니즈오션</span></a>
        <p>국내외 고객사의 성향과 니즈, 사업방향, PPT 제안 양식까지 모든 것을 모아둔 마케팅 실무자들의 바다입니다.</p>
      </div>
      <div class="footer-col"><h5>서비스</h5><ul><li><a href="#needs">고객사 NEEDS</a></li><li><a href="#direction">사업방향</a></li><li><a href="#ppt">고객사 PPT</a></li></ul></div>
      <div class="footer-col"><h5>바로가기</h5><ul><li><a href="#top">홈</a></li><li><a href="#audience">이용대상</a></li></ul></div>
      <div class="footer-col"><h5>문의</h5><ul><li><a href="mailto:seoyoon1.park@cosmax.com">이메일 문의</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 NeedsOcean. All rights reserved.</span>
      <span>Crafted for marketing professionals at COSMAX</span>
    </div>
  </div>
</footer>

<script>
  // 모바일 메뉴 토글
  const hamburger = document.getElementById('hamburger');
  const mainNav = document.getElementById('mainNav');
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mainNav.classList.toggle('open');
  });
  mainNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mainNav.classList.remove('open');
    });
  });

  // 검색: 이름이 일치하는 고객사 아코디언을 열고 그 위치로 스크롤
  const heroSearchForm = document.getElementById('heroSearchForm');
  const heroSearchInput = document.getElementById('heroSearchInput');
  heroSearchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = heroSearchInput.value.trim().toLowerCase();
    if (!q) return;
    const items = document.querySelectorAll('#needsList .acc, #directionList .acc');
    let hit = null;
    items.forEach(el => {
      const name = (el.getAttribute('data-name') || '').toLowerCase();
      if (!hit && name.includes(q)) hit = el;
    });
    if (hit) {
      hit.open = true;
      hit.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      document.getElementById('needs').scrollIntoView({ behavior: 'smooth' });
    }
  });

  // 카드 등장 애니메이션
  const revealEls = document.querySelectorAll('.feature-card, .audience-card, .acc, .ppt-card');
  revealEls.forEach(el => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity .6s ease, transform .6s ease';
  });
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = 1;
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealEls.forEach(el => observer.observe(el));
</script>

</body>
</html>
"""


@st.cache_data(show_spinner=False)
def build_page_html() -> str:
    clients = load_clients()
    html_doc = PAGE_TEMPLATE
    html_doc = html_doc.replace("__HERO_IMAGE_URI__", hero_image_uri())
    html_doc = html_doc.replace("__NEEDS_ITEMS__", build_needs_section(clients))
    html_doc = html_doc.replace("__DIRECTION_ITEMS__", build_direction_section(clients))
    html_doc = html_doc.replace("__PPT_ITEMS__", build_ppt_section(clients))
    return html_doc


components.html(build_page_html(), height=900, scrolling=True)
