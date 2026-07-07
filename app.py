import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).parent
HTML_PATH = BASE_DIR / "index.html"
IMAGE_PATH = BASE_DIR / "assets" / "cosmax_products.jpg"
SESSION_JS_PATH = BASE_DIR / "data" / "session.js"

st.set_page_config(
    page_title="니즈오션 | 마케팅 실무자들의 바다",
    page_icon="🌊",
    layout="wide",
)

# Streamlit 기본 여백/메뉴를 숨겨서 랜딩페이지가 화면 전체를 채우도록 함
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header[data-testid="stHeader"] {display: none;}
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100% !important;
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_html() -> str:
    """index.html을 읽어와서, 상대경로로 참조하던 이미지/스크립트를
    components.html(iframe srcdoc)에서도 동작하도록 인라인으로 치환한다."""
    html = HTML_PATH.read_text(encoding="utf-8")

    # 1) 배경 이미지를 base64 data URI로 인라인 처리
    if IMAGE_PATH.exists():
        img_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("utf-8")
        html = html.replace(
            "url('assets/cosmax_products.jpg')",
            f"url('data:image/jpeg;base64,{img_b64}')",
        )

    # 2) 외부 session.js 파일을 인라인 <script>로 치환
    if SESSION_JS_PATH.exists():
        session_js = SESSION_JS_PATH.read_text(encoding="utf-8")
        html = html.replace(
            '<script src="data/session.js"></script>',
            f"<script>\n{session_js}\n</script>",
        )

    return html


html_content = load_html()

# 페이지 전체 높이를 대략적으로 지정 (필요시 값 조정)
components.html(html_content, height=3200, scrolling=True)
