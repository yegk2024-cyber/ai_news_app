import streamlit as st
import asyncio
import edge_tts
from gtts import gTTS
import os

st.set_page_config(page_title="AI News Anchor (TH / Hmong)", page_icon="🎙️")

st.title("🎙️ แอปสร้างเสียงพากย์ข่าว AI")
st.caption("แปลงบทข่าวเป็นเสียงพากย์ภาษาไทย และ ภาษา Hmong (ม้ง)")

# เลือกภาษา
lang_choice = st.selectbox(
    "เลือกภาษาของเสียงพากย์:",
    [
        ("ภาษาไทย - เสียงนักข่าวมืออาชีพ", "th-pro"),
        ("ภาษา Hmong (ม้ง)", "hmn")
    ],
    format_func=lambda x: x[0]
)

news_text = st.text_area("วางเนื้อหาข่าวที่นี่:", height=200, placeholder="ก๊อปปี้ข้อความข่าวมาวางตรงนี้...")

if lang_choice[1] == "th-pro":
    th_voice = st.selectbox(
        "เลือกผู้ประกาศข่าว:",
        [
            ("นักข่าวชาย (เสียง นิวัฒน์)", "th-TH-NiwatNeural"),
            ("นักข่าวหญิง (เสียง เปรมวดี)", "th-TH-PremwateeNeural")
        ],
        format_func=lambda x: x[0]
    )

if st.button("🚀 สร้างไฟล์เสียงพากย์", type="primary"):
    if not news_text.strip():
        st.warning("กรุณากรอกข้อความข่าวก่อนครับ")
    else:
        with st.spinner("กำลังสร้างไฟล์เสียง..."):
            output_file = "news_voice.mp3"
            try:
                if lang_choice[1] == "th-pro":
                    voice_id = th_voice[1]
                    async def generate_audio():
                        communicate = edge_tts.Communicate(news_text, voice_id)
                        await communicate.save(output_file)
                    asyncio.run(generate_audio())
                elif lang_choice[1] == "hmn":
                    tts = gTTS(text=news_text, lang='hmn', slow=False)
                    tts.save(output_file)

                st.success("สร้างไฟล์เสียงสำเร็จ!")
                audio_bytes = open(output_file, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(label="📥 ดาวน์โหลดไฟล์เสียง (.mp3)", data=audio_bytes, file_name="news_voice.mp3", mime="audio/mp3")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")