# 📚 ຄູ່ມືການນຳໃຊ້ໂປຣເຈັກ Webview Manager (MeDownloader)

ຍິນດີຕ້ອນຮັບສູ່ໂປຣເຈັກ Webview Manager! ນີ້ຄືຄູ່ມືແນະນຳຂັ້ນຕອນການຕິດຕັ້ງ ແລະ ການນຳໃຊ້ໂປຣເຈັກຂອງທ່ານ.

## 1. ແນະນຳໂປຣເຈັກ (Introduction)
ໂປຣເຈັກນີ້ແມ່ນລະບົບຈັດການລີ້ງເວັບໄຊຕ໌ (Webview Links) ເຊິ່ງປະກອບມີລະບົບ Frontend ສຳລັບໜ້າຈໍຜູ້ໃຊ້ ແລະ Backend ສຳລັບການປະມວນຜົນ. 
ຈຸດເດັ່ນຂອງໂປຣເຈັກນີ້ແມ່ນການສາມາດບັນທຶກຂໍ້ມູນລົງໃນ **Google Sheets** ໄດ້ໂດຍອັດຕະໂນມັດ (Real-time sync). ແຕ່ຖ້າຫາກບໍ່ໄດ້ຕັ້ງຄ່າ Google Sheets, ລະບົບກໍ່ຍັງສາມາດເຮັດວຽກໄດ້ປົກກະຕິ ໂດຍການບັນທຶກຂໍ້ມູນລົງໃນຖານຂໍ້ມູນ **SQLite** ແທນ.

## 2. ໂຄງສ້າງໂປຣເຈັກ (Project Structure)
- `frontend/`: ສ່ວນຕິດຕໍ່ຜູ້ໃຊ້ (UI) ພັດທະນາດ້ວຍ **Nuxt 3 / Nuxt 4** (Vue.js) ແລະ Vuetify.
- `backend_python/`: ສ່ວນປະມວນຜົນ API ພັດທະນາດ້ວຍ **Python**, **FastAPI**, **SQLAlchemy**, ແລະ **yt-dlp** (ແບບ Modular Architecture).

---

## 3. ວິທີການຕິດຕັ້ງ (Installation)

**👉 ສຳລັບ Backend (Python):**
1. ເປີດ Terminal ແລ້ວເຂົ້າໄປທີ່: `cd backend_python`
2. ສ້າງ Virtual Environment ແລະ ຕິດຕັ້ງ Dependencies:
   ```powershell
   python -m venv venv
   .\venv\Scripts\pip install -r requirements.txt
   ```

**👉 ສຳລັບ Frontend (Node.js):**
1. ເປີດ Terminal ແລ້ວເຂົ້າໄປທີ່: `cd frontend`
2. ຕິດຕັ້ງ Packages ຕ່າງໆ: `npm install`

---

## 4. ວິທີການເປີດໃຊ້ງານ (How to Run)
ເພື່ອໃຫ້ແອັບພລິເຄຊັນເຮັດວຽກໄດ້ສົມບູນ, ທ່ານຕ້ອງເປີດທັງ Backend ແລະ Frontend ພ້ອມກັນ.

**ເປີດ Backend (Python FastAPI):**
- ວິທີທີ 1: ດັບເບິ້ລຄລິກໄຟລ໌ `backend_python/run.bat`
- ວິທີທີ 2: ພິມຄຳສັ່ງ:
  ```powershell
  cd backend_python
  .\venv\Scripts\python.exe main.py
  ```
*(Backend ຈະເລີ່ມເຮັດວຽກຢູ່ທີ່ພອດ `http://localhost:3005` ພ້ອມມີ API Docs ຢູ່ທີ່ `/docs`)*

**ເປີດ Frontend (Nuxt):**
ເຂົ້າໄປທີ່ໂຟນເດີ `frontend` ແລ້ວພິມຄຳສັ່ງ:
```bash
npm run dev
```
*(Frontend ຈະເລີ່ມເຮັດວຽກຢູ່ທີ່ພອດ `http://localhost:3000`)*

ເມື່ອເປີດສຳເລັດແລ້ວ, ທ່ານສາມາດເຂົ້າໄປທີ່ບຣາວເຊີ (Browser) ແລ້ວພິມ `http://localhost:3000` ເພື່ອເລີ່ມຕົ້ນນຳໃຊ້ໄດ້ເລີຍ!

---

## 5. ການຕັ້ງຄ່າ Google Sheets (Google Sheets Setup)
ຖ້າທ່ານຕ້ອງການໃຫ້ລະບົບບັນທຶກລີ້ງຕ່າງໆລົງໃນ Google Sheets ຂອງທ່ານໂດຍກົງ, ກະລຸນາປະຕິບັດຕາມຂັ້ນຕອນດັ່ງນີ້:

1. **ສ້າງ Google Sheet:** ສ້າງ Sheet ໃໝ່ ແລ້ວພິມຫົວຂໍ້ **Title** ຢູ່ຫ້ອງ `A1` ແລະ **URL** ຢູ່ຫ້ອງ `B1`.
2. **ແກ້ໄຂໄຟລ໌ `.env`:** ເຂົ້າໄປທີ່ໂຟນເດີ `backend_python/` ແລ້ວເປີດໄຟລ໌ `.env`.
3. **ໃສ່ Sheet ID:** ກັອບປີ້ ID ຂອງ Sheet (ຈາກ URL ດ້ານເທິງຂອງ Browser) ມາໃສ່ໃນຊ່ອງ `GOOGLE_SHEET_ID`.
4. **ໃສ່ Credentials:** ນຳເອົາ Email ຂອງ Service Account ມາໃສ່ໃນ `GOOGLE_CLIENT_EMAIL` ແລະ ນຳເອົາ Private Key (ທີ່ໄດ້ຈາກໄຟລ໌ JSON) ມາໃສ່ໃນ `GOOGLE_PRIVATE_KEY`.
5. **ແຊຣ໌ Sheet:** **(ສຳຄັນທີ່ສຸດ)** ຢ່າລືມກົດປຸ່ມ **Share** ຢູ່ໜ້າ Google Sheet ຂອງທ່ານ ແລ້ວນຳເອົາ Email ຂອງ Service Account ເຂົ້າໄປ ພ້ອມທັງກຳນົດສິດໃຫ້ເປັນ **Editor**.
6. **ເປີດໃຊ້ API:** ກວດສອບໃຫ້ແນ່ໃຈວ່າທ່ານໄດ້ກົດປຸ່ມ Enable ເພື່ອເປີດໃຊ້ງານ **Google Sheets API** ແລ້ວໃນ Google Cloud Console.

ເມື່ອຕັ້ງຄ່າສຳເລັດແລ້ວ, ເຊີບເວີຈະແຈ້ງເຕືອນວ່າ `✅ Connected to Google Sheet` ເຊິ່ງໝາຍຄວາມວ່າພ້ອມນຳໃຊ້ແລ້ວ!

---

## 6. ຟີເຈີໃໝ່ລ່າສຸດ (Latest Features): Qwen AI Chat & Image Generation
ໂປຣເຈັກໄດ້ມີການອັບເກຣດ ແລະ ເພີ່ມຟີເຈີ AI ໃໝ່ເຂົ້າໄປໃນລະບົບ:
- **Nuxt 4 Upgrade**: ລະບົບ Frontend ໄດ້ຖືກອັບເກຣດເປັນ Nuxt 4 (Compatibility Date: 2024-11-01) ເພື່ອປະສິດທິພາບທີ່ດີຂຶ້ນ.
- **Qwen AI Chat (OpenRouter)**: ເພີ່ມໜ້າຕ່າງແຊັດ AI ອັດສະລິຍະຢູ່ທີ່ເມນູ `/chatai/qwenai` ພ້ອມທັງ Floating Widget.
- **AI Image Generation**: ສາມາດສັ່ງໃຫ້ AI ແຕ້ມຮູບໄດ້ (ຜ່ານ Pollinations AI) ໂດຍການພິມຄຳສັ່ງ `/image [ຊື່ຮູບ]`, ພ້ອມມີລະບົບ Loading Spinner ທີ່ສວຍງາມ.
- **Full-Screen Image Viewer**: ລະບົບເບິ່ງຮູບພາບແບບເຕັມຈໍ (True Full-Screen Modal) ພ້ອມປຸ່ມດາວໂຫຼດຮູບພາບໂດຍກົງ.
- **Full-Screen Chat**: ສາມາດຂະຫຍາຍໜ້າຈໍແຊັດ AI ໃຫ້ເຕັມໜ້າຈໍໄດ້ເພື່ອຄວາມສະດວກໃນການອ່ານ.

*(ໝາຍເຫດ: ສຳລັບການນຳໃຊ້ Qwen AI, ທ່ານຈຳເປັນຕ້ອງມີ OpenRouter API Key ເຊິ່ງສາມາດໄປສ້າງໄດ້ທີ່ openrouter.ai/keys).*
