import streamlit as st
import random, time

st.set_page_config(page_title="Kéo Búa Bao", page_icon="✂️")
st.title("✂️ Kéo – Búa – Bao 🎮")

images = {
    "kéo": "https://openmoji.org/data/color/svg/2702.svg",
    "búa": "https://cdn-icons-png.flaticon.com/512/2983/2983656.png",
    "bao": "https://img.icons8.com/emoji/96/roll-of-paper.png"
}
choices = list(images.keys())

player_choice = st.radio("👉 Bạn chọn:", choices)
if st.button("Chơi ngay!"):
    computer_choice = random.choice(choices)

    st.write("🤖 Máy đang chọn...")
    placeholder = st.empty()

    # Hiệu ứng nháy nháy
    for i in range(6):  # nháy 6 lần
        if i % 2 == 0:
            placeholder.image(images[computer_choice], width=120)
        else:
            placeholder.empty()
        time.sleep(0.2)

    # Sau khi nháy xong → hiện kết quả
    st.write(f"🤖 Máy chọn: **{computer_choice}**")
    st.image(images[computer_choice], width=120)

    if player_choice == computer_choice:
        st.info("Kết quả: Hòa 🤝")
    elif (player_choice == "kéo" and computer_choice == "bao") or \
         (player_choice == "búa" and computer_choice == "kéo") or \
         (player_choice == "bao" and computer_choice == "búa"):
        st.success("Bạn **THẮNG 🎉**")
    else:
        st.error("Bạn **THUA 😢**")


