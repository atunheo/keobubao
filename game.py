import streamlit as st
import random

st.set_page_config(page_title="Kéo Búa Bao", page_icon="✂️")

st.title("✂️ Kéo – Búa – Bao 🎮")

choices = ["kéo", "búa", "bao"]

# Lưu bảng điểm trong session_state
if "win" not in st.session_state:
    st.session_state.win = 0
if "lose" not in st.session_state:
    st.session_state.lose = 0
if "draw" not in st.session_state:
    st.session_state.draw = 0

player = st.radio("👉 Bạn chọn:", choices)

if st.button("Chơi ngay!"):
    computer = random.choice(choices)
    st.write(f"🤖 Máy chọn: **{computer}**")

    if player == computer:
        st.info("Kết quả: **Hòa 🤝**")
        st.session_state.draw += 1
    elif (player == "kéo" and computer == "bao") or \
         (player == "búa" and computer == "kéo") or \
         (player == "bao" and computer == "búa"):
        st.success("Bạn **THẮNG 🎉**")
        st.session_state.win += 1
    else:
        st.error("Bạn **THUA 😢**")
        st.session_state.lose += 1

st.subheader("📊 Bảng điểm")
st.write(f"✅ Thắng: {st.session_state.win}")
st.write(f"❌ Thua: {st.session_state.lose}")
st.write(f"🤝 Hòa: {st.session_state.draw}")
