
import streamlit as st
import asyncio
import edge_tts
import os

st.set_page_config(page_title="AI News Anchor Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ ระบบสร้างเสียงพากย์และกรอบข่าว AI")
st.caption("รองรับภาษา Hmong (ม้ง) | ภาษาลาว (Lao) | ภาษาไทย (Thai)")

# ตัวเลือกเสียงพากย์ (เพิ่มเสียงผู้ชายภาษาม้งให้แล้วครับ)
VOICE_OPTIONS = {
    "ภาษา Hmong (ม้ง) - เสียงผู้ชาย (Yunfan)": "hmn-CN-YunfanNeural",
    "ภาษา Hmong (ม้ง) - เสียงผู้หญิง (Wanida)": "hmn-CN-WanidaNeural",
    "ภาษาลาว (Lao) - เสียงผู้ชาย (Keomany)": "lo-LA-KeomanyNeural",
    "ภาษาลาว (Lao) - เสียงผู้หญิง (Chanthavong)": "lo-LA-ChanthavongNeural",
    "ภาษาไทย - เสียงผู้ชาย (Niwat)": "th-TH-NiwatNeural",
    "ภาษาไทย - เสียงผู้หญิง (Premwatee)": "th-TH-PremwateeNeural"
}

selected_voice_label = st.selectbox("เลือกล็อคเสียงและภาษาพากย์:", list(VOICE_OPTIONS.keys()))
voice_id = VOICE_OPTIONS[selected_voice_label]

news_text = st.text_area("กรอกบทข่าวที่นี่:", height=180, placeholder="พิมพ์หรือวางบทข่าวภาษาม้ง ลาว หรือไทย...")

if st.button("🚀 สร้างไฟล์เสียงพากย์ (MP3)", type="primary"):
    if not news_text.strip():
        st.warning("กรุณากรอกข้อความข่าวซะก่อนครับ")
    else:
        with st.spinner("กำลังประมวลผลเสียงพากย์..."):
            output_file = "news_voice.mp3"
            
            async def generate_audio():
                communicate = edge_tts.Communicate(news_text, voice_id)
                await communicate.save(output_file)

            try:
                asyncio.run(generate_audio())
                st.success("สร้างไฟล์เสียงสำเร็จแล้ว!")
                
                # เล่นเสียง
                st.audio(output_file, format="audio/mp3")
                
                # ปุ่มดาวน์โหลด
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📥 ดาวน์โหลดไฟล์เสียง (.mp3) ลงเครื่อง",
                        data=f,
                        file_name="news_voice.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
