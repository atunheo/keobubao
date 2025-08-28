import streamlit as st
import random

st.set_page_config(page_title="Kéo Búa Bao", page_icon="🎮")

st.title("✂️ Kéo – Búa – Bao 🎮")

choices = ["kéo", "búa", "bao"]

# Người chơi chọn
player = st.radio("Chọn của bạn:", choices)

# Nút chơi
if st.button("Chơi ngay!"):
    computer = random.choice(choices)

    st.write(f"🤖 Máy chọn: **{computer}**")

    if player == computer:
        st.info("Kết quả: **Hòa 🤝**")
    elif (player == "kéo" and computer == "bao") or \
         (player == "búa" and computer == "kéo") or \
         (player == "bao" and computer == "búa"):
        st.success("Bạn **THẮNG 🎉**")
    else:
        st.error("Bạn **THUA 😢**")
