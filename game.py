import streamlit as st
import random

st.set_page_config(page_title="Kéo Búa Bao", page_icon="✂️")

st.title("✂️ Kéo – Búa – Bao 🎮")

# Mapping: tên -> file ảnh
images = {
    "kéo": "keo.png",
    "búa": "bua.png",
    "bao": "bao.png"
}

choices = list(images.keys())

# Lưu bảng điểm
if "win" not in st.session_state:
    st.session_state.win = 0
if "lose" not in st.session_state:
    st.session_state.lose = 0
if "draw" not in st.session_state:
    st.session_state.draw = 0

st.subheader("👉 Bạn chọn:")

# Hiển thị 3 cột, mỗi cột 1 hình
cols = st.columns(3)
player_choice = None

for i, choice in enumerate(choices):
    with cols[i]:
        st.image(images[choice], width=120)
        if st.button(choice.capitalize()):
            player_choice = choice

# Khi có lựa chọn
if player_choice:
    computer_choice = random.choice(choices)

    st.subheader("Kết quả:")
    st.write("🤖 Máy chọn:")
    st.image(images[computer_choice], width=120)

    if player_choice == computer_choice:
        st.info("Hòa 🤝")
        st.session_state.draw += 1
    elif (player_choice == "kéo" and computer_choice == "bao") or \
         (player_choice == "búa" and computer_choice == "kéo") or \
         (player_choice == "bao" and computer_choice == "búa"):
        st.success("Bạn **THẮNG 🎉**")
        st.session_state.win += 1
    else:
        st.error("Bạn **THUA 😢**")
        st.session_state.lose += 1

    st.subheader("📊 Bảng điểm")
    st.write(f"✅ Thắng: {st.session_state.win}")
    st.write(f"❌ Thua: {st.session_state.lose}")
    st.write(f"🤝 Hòa: {st.session_state.draw}")
