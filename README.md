# 📂 FileEase – Django File Compression Tool

A Django-based web application for file compression and decompression using **Huffman Coding**.  
Users can upload files, compress them, and download the compressed versions via a clean and responsive UI.

---

## 🚀 Features
- 🔒 **Lossless Compression** using Huffman Coding  
- 📥 **Upload → Compress → Download** workflow  
- 📄 Supports multiple file types (e.g., `.txt`)  
- 🎨 Clean Django templates with responsive design  
- 💾 File storage system:
  - `/uploads/` → stores uploaded files  
  - `/compressed/` → stores compressed files  
- 🗄️ SQLite database to keep track of file operations  

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)  
- **Algorithm:** Huffman Coding  
- **Frontend:** HTML, CSS, Django Templates  
- **Static Handling:** Django Staticfiles (`/static/`)  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/FileEase.git
cd FileEase
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
# Activate venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Apply Migrations
```bash
python manage.py migrate
```
### 5️⃣ Run Server
```bash
python manage.py runserver
```
👉 Open http://127.0.0.1:8000/ in your browser.

## 📊 Example Workflow

**Input:** `"hello world"`

- **Frequency:** `{h:1, e:1, l:3, o:2, w:1, r:1, d:1}`
- **Huffman Codes:** `l=00, o=01, h=100, e=101, …`
- **Output Binary:** `10010100000101111100...`

✅ File size reduced by ~40% (varies with content).

---

## 📈 Future Enhancements
- Add support for more algorithms 
- Add user accounts to save compression history  
- Deploy live demo (Heroku/Render)  
