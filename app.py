import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import os
import time
import pandas as pd
from datetime import datetime

# ==========================
# 1. Load Model & Labels
# ==========================
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("cnn_best_ga_pso.h5")
    labels = np.load("labels.npy", allow_pickle=True)
    return model, labels

model, labels = load_model()

# ==========================
# 2. Helper Functions
# ==========================
def predict_frame(frame):
    """Resize + normalisasi + prediksi 1 frame"""
    img = cv2.resize(frame, (64,64))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img, verbose=0)
    idx = np.argmax(preds)
    return labels[idx], preds[0][idx]

def save_history(action, content):
    """Simpan aktivitas ke Excel"""
    file = "history.xlsx"
    log = pd.DataFrame([[datetime.now(), action, content]],
                       columns=["timestamp", "action", "content"])
    if os.path.exists(file):
        old = pd.read_excel(file)
        log = pd.concat([old, log], ignore_index=True)
    log.to_excel(file, index=False)

# ==========================
# 3. Sidebar Menu
# ==========================
st.sidebar.title("📌 Menu")
page = st.sidebar.radio("Pilih halaman:", 
                        ["Welcome", "Translator", "Training Huruf", "Training Kata"])

# ==========================
# 4. Welcome Page
# ==========================
if page == "Welcome":
    st.title("🤟 Welcome to ASL Translator")
    st.markdown("""
    Selamat datang di aplikasi **ASL Translator** 🎉

    - **Translator** → menerjemahkan huruf ASL secara real-time.  
    - **Training Huruf** → latihan mengenali huruf satu per satu.  
    - **Training Kata** → latihan mengeja kata target huruf demi huruf.  

    Semua aktivitas (translate, latihan, delete) otomatis tersimpan ke `history.xlsx`.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3b/ASL_alphabet.png", 
             caption="ASL Alphabet", use_container_width=True)

# ==========================
# 5. Translator
# ==========================
elif page == "Translator":
    st.title("📹 ASL Real-Time Translator")

    run = st.checkbox("Start Webcam")

    if "history" not in st.session_state:
        st.session_state.history = ""

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        # prediksi huruf
        letter, prob = predict_frame(frame)

        # update teks tiap 1 detik
        if time.time() % 1 < 0.05:
            st.session_state.history += letter

        # tampilkan prediksi di frame
        cv2.putText(frame, f"{letter} ({prob:.2f})", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    camera.release()

    st.subheader("Riwayat Terjemahan:")
    st.write(st.session_state.history)

    if st.button("❌ Delete"):
        save_history("delete", st.session_state.history)
        st.warning("Teks dihapus, tapi tersimpan di log.")
        st.session_state.history = ""

# ==========================
# 6. Training Huruf
# ==========================
elif page == "Training Huruf":
    st.title("🔠 Training Huruf")

    huruf = st.selectbox("Pilih huruf untuk latihan:", labels)
    st.write(f"Target huruf: **{huruf}**")

    run = st.checkbox("Mulai Latihan")
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        pred, prob = predict_frame(frame)

        cv2.putText(frame, f"Target: {huruf}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.putText(frame, f"Prediksi: {pred}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if pred == huruf and prob > 0.8:
            st.success(f"✅ Betul! Huruf {huruf}")
            save_history("train_huruf", huruf)
            break

    camera.release()

# ==========================
# 7. Training Kata
# ==========================
elif page == "Training Kata":
    st.title("🔡 Training Kata (Spelling Practice)")

    target = st.text_input("Masukkan kata untuk dieja:", "LOVE").upper()
    st.write(f"Target kata: **{target}**")

    if "index" not in st.session_state:
        st.session_state.index = 0

    run = st.checkbox("Mulai Ejaan")
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run and st.session_state.index < len(target):
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        pred, prob = predict_frame(frame)

        current_char = target[st.session_state.index]
        cv2.putText(frame, f"Target: {current_char}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.putText(frame, f"Prediksi: {pred}", (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if pred == current_char and prob > 0.8:
            st.success(f"✅ Betul! Huruf {current_char}")
            st.session_state.index += 1
            time.sleep(1)

    camera.release()

    if st.session_state.index == len(target):
        st.success(f"🎉 Kata '{target}' selesai dieja!")
        save_history("train_kata", target)
        st.session_state.index = 0
