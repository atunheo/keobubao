import streamlit as st
import time
from datetime import datetime, timezone
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, initialize_app

# ---------- CONFIG ----------
st.set_page_config(page_title="Kéo Búa Bao Online", page_icon="✂️")

# ---------- INIT FIREBASE FROM SECRETS ----------
# Lưu service account JSON vào secrets (xem phần 3)
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase_service_account"])
    initialize_app(cred)
db = firestore.Client()

CHOICES = ["kéo", "búa", "bao"]

# ---------- HELPERS ----------
def room_ref(room_id):
    return db.collection("rps_rooms").document(room_id)

def now_ts():
    return datetime.now(timezone.utc)

@firestore.transactional
def submit_move_txn(transaction, ref, player, move):
    snap = ref.get(transaction=transaction)
    data = snap.to_dict() if snap.exists else {}

    players = data.get("players", {})
    moves   = data.get("moves", {})
    locked  = data.get("locked", {})
    revealed = data.get("revealed", False)

    # tạo room nếu chưa có
    players[player] = True
    moves[player] = move
    locked[player] = True  # khóa ngay khi bấm

    # nếu đã có đủ 2 người và cả hai đã locked -> reveal
    if len(locked) >= 2 and all(locked.values()):
        revealed = True

    transaction.set(ref, {
        "players": players,
        "moves": moves,
        "locked": locked,
        "revealed": revealed,
        "updated_at": firestore.SERVER_TIMESTAMP,
    }, merge=True)

def reset_room(ref):
    ref.set({
        "moves": {},
        "locked": {},
        "revealed": False,
        "updated_at": firestore.SERVER_TIMESTAMP,
    }, merge=True)

def judge(a, b):
    if a == b: return "Hòa 🤝"
    win = (a=="kéo" and b=="bao") or (a=="búa" and b=="kéo") or (a=="bao" and b=="búa")
    return "Bạn THẮNG 🎉" if win else "Bạn THUA 😢"

# ---------- UI ----------
st.title("✂️ Kéo – Búa – Bao Online (Firebase)")

colA, colB = st.columns(2)
with colA:
    room_id = st.text_input("🧩 Mã phòng", value="phong1")
with colB:
    player  = st.text_input("👤 Tên của bạn", value="PlayerA")

st.caption("Mẹo: 2 người mở cùng link app, nhập **cùng mã phòng** nhưng **tên khác nhau**.")

if not room_id or not player:
    st.stop()

# auto refresh 2 giây để “real-time”
st_autorefresh = st.experimental_rerun  # alias ngắn
st_autorefresh = st.autorefresh if hasattr(st, "autorefresh") else None
if st_autorefresh:
    st_autorefresh(interval=2000, key="poll")  # 2s

ref = room_ref(room_id)
doc = ref.get()
data = doc.to_dict() if doc.exists else None

if not data:
    # Tạo room rỗng lần đầu
    ref.set({
        "players": {player: True},
        "moves": {},
        "locked": {},
        "revealed": False,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP,
    }, merge=True)
    data = ref.get().to_dict()

moves   = data.get("moves", {})
locked  = data.get("locked", {})
revealed = data.get("revealed", False)
players = list(data.get("players", {}).keys())

st.subheader(f"📦 Phòng: {room_id}")
st.write("👥 Người trong phòng:", ", ".join(players) if players else "—")

# --- Chọn nước đi ---
st.markdown("### 👉 Chọn nước đi (chỉ bạn thấy cho đến khi cả hai khóa)")
choice = st.segmented_control("Lựa chọn", CHOICES, key="choice_seg")  # Streamlit >= 1.41
lock_col1, lock_col2, lock_col3 = st.columns([1,1,2])

with lock_col1:
    lock_btn = st.button("🔒 Khóa lựa chọn")
with lock_col2:
    reset_btn = st.button("♻️ Reset phòng")

if reset_btn:
    reset_room(ref)
    st.success("Đã reset phòng.")
    st.stop()

# Gởi move (ẩn) và lock
if lock_btn:
    if choice not in CHOICES:
        st.warning("Hãy chọn Kéo / Búa / Bao trước khi khóa.")
    else:
        transaction = db.transaction()
        submit_move_txn(transaction, ref, player, choice)
        st.success("Đã khóa lựa chọn. Chờ đối thủ…")

# Reload state sau khi submit
doc = ref.get()
data = doc.to_dict() if doc.exists else {}
moves   = data.get("moves", {})
locked  = data.get("locked", {})
revealed = data.get("revealed", False)
players = list(data.get("players", {}).keys())

# --- Trạng thái ---
st.markdown("### ⏳ Trạng thái")
me_locked = bool(locked.get(player))
others = [p for p in players if p != player]
other = others[0] if others else None
other_locked = bool(locked.get(other)) if other else False

st.write(f"🔒 Bạn: {'ĐÃ KHÓA' if me_locked else 'chưa'}")
st.write(f"🔒 Đối thủ: {'ĐÃ KHÓA' if other_locked else 'chưa' if other else 'chưa vào phòng'}")

# --- Reveal nếu đã đủ điều kiện ---
if not revealed:
    # Nếu cả hai đã locked, server sẽ đặt revealed=True trong transaction.
    # Ở client, chỉ hiển thị gợi ý chờ.
    st.info("Chờ cả hai người khóa lựa chọn để mở kết quả…")
    st.stop()

# --- Hiện kết quả khi revealed=True ---
st.markdown("### 🎯 Kết quả")
my_move = moves.get(player)
opp_move = moves.get(other) if other else None

if other is None or my_move is None or opp_move is None:
    st.warning("Thiếu dữ liệu nước đi. Có thể đối thủ vừa rời phòng hoặc chưa có đối thủ.")
else:
    c1 = my_move
    c2 = opp_move

    img_map = {
        "kéo": "https://openmoji.org/data/color/svg/2702.svg",
        "búa": "https://cdn-icons-png.flaticon.com/512/2983/2983656.png",
        "bao": "https://img.icons8.com/emoji/96/roll-of-paper.png"
    }

    a, b = st.columns(2)
    with a:
        st.write(f"👤 Bạn: **{c1}**")
        st.image(img_map[c1], width=120)
    with b:
        st.write(f"👤 {other}: **{c2}**")
        st.image(img_map[c2], width=120)

    # Chấm điểm từ phía "bạn"
    result = judge(c1, c2)
    if "THẮNG" in result:
        st.success(result)
    elif "Hòa" in result:
        st.info(result)
    else:
        st.error(result)

st.caption("Dùng Firestore để đồng bộ: mỗi lần 2s app tự tải lại trạng thái phòng.")
