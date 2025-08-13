import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
# 운영(Nginx 프록시) 기본은 /api, 로컬 개발은 .env에서 API_BASE=http://127.0.0.1:8000 등으로 덮어쓰기
API_BASE = os.getenv("API_BASE", "")

st.set_page_config(page_title="AI 이미지 생성 & 설명", page_icon="🖼️", layout="centered")
st.title("🖼️ DALL·E 3 이미지 생성 + GPT-4o 한국어 설명")

with st.form("gen_form"):
    prompt = st.text_area("프롬프트", placeholder="예) 바닷가 노을 아래 앉아 있는 고양이")
    size = st.selectbox("사이즈", ["1024x1024", "1024x1792", "1792x1024"], index=0)
    submitted = st.form_submit_button("이미지 생성")

if submitted:
    if not prompt.strip():
        st.warning("프롬프트를 입력하세요.")
    else:
        with st.spinner("이미지 생성 중..."):
            res = requests.post(f"{API_BASE}/generate", json={"prompt": prompt, "size": size}, timeout=60)
            if res.ok:
                st.session_state["image_url"] = res.json()["image_url"]
            else:
                st.error(f"이미지 생성 실패: {res.text}")

if st.session_state.get("image_url"):
    st.image(st.session_state["image_url"], use_column_width=True)
    if st.button("이미지 설명하기"):
        with st.spinner("이미지 설명 중..."):
            res = requests.post(f"{API_BASE}/describe", json={"image_url": st.session_state["image_url"], "style": "detailed"}, timeout=60)
            if res.ok:
                st.write(res.json()["analysis"])
            else:
                st.error(f"설명 실패: {res.text}")