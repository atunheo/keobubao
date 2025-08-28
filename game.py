import streamlit as st
import random

st.set_page_config(page_title="Kéo Búa Bao", page_icon="✂️")

st.title("✂️ Kéo – Búa – Bao 🎮")

# Ảnh online
images = {
    "kéo": "https://openmoji.org/data/color/svg/2702.svg",
    "búa": "https://cdn-icons-png.flaticon.com/512/2983/2983656.png",
    "bao": "https://img.icons8.com/emoji/96/roll-of-paper.png"
}

choices = list(images.keys())

# CSS animation: nhấp nháy khi hover
st.markdown("""
    <style>
    .choice-img {
        width: 120px;
        transition: transform 0.2s;
    }
    .choice-img:hover {
        animation: flash 0.5s infinite alternate;
        cursor: pointer;
        transform: scale(1.1);
    }
    @keyframes flash {
        from { opacity: 1; }
        to { opacity: 0.5; }
    }
    </style>
""", unsafe_allow_html=True)

# Hiển thị ảnh chọn
cols = st.columns(3)
player_choice = None
for i, choice in enumerate(choices):
    with cols[i]:
        if st.button(f"{choice}", key=choice):
            player_choice = choice
        st.markdown(
            f'<img src="{images[choice]}" class="choice-img"/>',
            unsafe_allow_html=True
        )

# Xử lý chọn
if player_choice:
    computer_choice = random.choice(choices)
    st.subheader("Kết quả:")
    st.write("🤖 Máy chọn:")
    st.image(images[computer_choice], width=120)

    if player_choice == computer_choice:
        st.info("Hòa 🤝")
    elif (player_choice == "kéo" and computer_choice == "bao") or \
         (player_choice == "búa" and computer_choice == "kéo") or \
         (player_choice == "bao" and computer_choice == "búa"):
        st.success("Bạn **THẮNG 🎉**")
    else:
        st.error("Bạn **THUA 😢**")
