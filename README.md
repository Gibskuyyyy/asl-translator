# 🤟 ASL Real-Time Translator

Aplikasi real-time untuk menerjemahkan **Bahasa Isyarat Amerika (ASL)** huruf A–Z menggunakan **Convolutional Neural Network (CNN)** dengan integrasi **Streamlit + TensorFlow + OpenCV**.  
Selain menerjemahkan, aplikasi ini juga menyediakan fitur **latihan huruf** dan **latihan mengeja kata** agar pengguna bisa belajar secara interaktif.

---

## 📌 Demo
- **Translator**: Terjemahkan huruf ASL secara real-time via webcam.  
- **Training Huruf**: Latihan mengenali huruf satu per satu.  
- **Training Kata**: Latihan mengeja kata target huruf demi huruf.  


---

## 📂 Dataset & Model
- Dataset: **ASL Alphabet Dataset** (gambar huruf A–Z).  
- Model: **CNN baseline**, dioptimasi dengan GA–PSO (versi Notebook).  
- Output training: `cnn_best_ga_pso.h5` (model) + `labels.npy` (mapping huruf).  

---

## 🚀 Cara Instalasi & Menjalankan
### 1. Clone repository
```bash
git clone https://github.com/Gibskuyyyy/asl-translator.git
cd asl-translator/asl_app
````

### 2. Buat environment (opsional tapi disarankan)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```bash
streamlit run app.py
```

---

## 🖥️ Fitur Aplikasi

1. **Welcome Page** → intro aplikasi + alfabet ASL.
2. **Translator** → webcam real-time + prediksi huruf + riwayat teks.
3. **Training Huruf** → pilih huruf, coba tirukan → feedback benar/salah.
4. **Training Kata** → input kata, eja huruf demi huruf → sistem cek progres.
5. **History Log** → semua aksi (translate, latihan, delete) otomatis tersimpan ke `history.xlsx`.

---

## 📊 Hasil

* Akurasi CNN pada dataset ASL Alphabet: **80–90%**.
* Model real-time dapat mengenali sebagian besar huruf dengan baik dalam kondisi pencahayaan normal.
* Fitur latihan membantu pengguna memahami dan melatih ASL huruf per huruf hingga kata sederhana.

---

## ⚠️ Keterbatasan

* Model masih kesulitan membedakan huruf dengan bentuk tangan mirip (`M`, `N`, `S`).
* Performa real-time sangat bergantung pada pencahayaan & posisi tangan.
* Belum mendukung kalimat penuh → masih fokus huruf & kata sederhana.

---

## 🔮 Rencana Pengembangan

* Tambah dukungan untuk **kata & kalimat langsung** (tanpa ejaan).
* Integrasi **Speech-to-Text / Text-to-Speech** agar lebih interaktif.
* Gunakan **MobileNet / EfficientNet** untuk model ringan & cepat.
* Tambahkan dataset **WLASL** untuk dukungan lebih banyak gesture.

---

## 👨‍💻 Kontributor

* Proyek ini dikembangkan sebagai tugas mata kuliah **Artificial Intelligence (AI)**.
* Dibuat dengan bantuan **TensorFlow, OpenCV, Streamlit**.

