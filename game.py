import streamlit as st
import random, time

st.set_page_config(page_title="Kéo Búa Bao", page_icon="✂️")
st.title("✂️ Kéo – Búa – Bao 🎮")

# Hình ảnh
images = {
    "kéo": "https://openmoji.org/data/color/svg/2702.svg",
    "búa": "https://cdn-icons-png.flaticon.com/512/2983/2983656.png",
    "bao": "https://img.icons8.com/emoji/96/roll-of-paper.png"
}
choices = list(images.keys())

# Người chơi chọn
player_choice = st.radio("👉 Bạn chọn:", choices)

if st.button("Chơi ngay!"):
    st.write("🤖 Máy đang chọn...")
    placeholder = st.empty()

    # Slot machine effect: random hiển thị 10 lần
    for i in range(10):
        temp_choice = random.choice(choices)
        placeholder.image(images[temp_choice], width=120)
        time.sleep(0.15)

    # Kết quả chính thức
    computer_choice = random.choice(choices)
    placeholder.image(images[computer_choice], width=120)
    st.write(f"🤖 Máy chọn: **{computer_choice}**")

    # So kết quả
    if player_choice == computer_choice:
        st.info("Kết quả: Hòa 🤝")
    elif (player_choice == "kéo" and computer_choice == "bao") or \
         (player_choice == "búa" and computer_choice == "kéo") or \
         (player_choice == "bao" and computer_choice == "búa"):
        st.success("Bạn **THẮNG 🎉**")
    else:
        st.error("Bạn **THUA 😢**")
