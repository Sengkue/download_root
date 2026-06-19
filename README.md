# 📚 ຄູ່ມືການນຳໃຊ້ໂປຣເຈັກ Webview Manager (MeDownloader)

ຍິນດີຕ້ອນຮັບສູ່ໂປຣເຈັກ Webview Manager! ນີ້ຄືຄູ່ມືແນະນຳຂັ້ນຕອນການຕິດຕັ້ງ ແລະ ການນຳໃຊ້ໂປຣເຈັກຂອງທ່ານ.

## 1. ແນະນຳໂປຣເຈັກ (Introduction)
ໂປຣເຈັກນີ້ແມ່ນລະບົບຈັດການລີ້ງເວັບໄຊຕ໌ (Webview Links) ເຊິ່ງປະກອບມີລະບົບ Frontend ສຳລັບໜ້າຈໍຜູ້ໃຊ້ ແລະ Backend ສຳລັບການປະມວນຜົນ. 
ຈຸດເດັ່ນຂອງໂປຣເຈັກນີ້ແມ່ນການສາມາດບັນທຶກຂໍ້ມູນລົງໃນ **Google Sheets** ໄດ້ໂດຍອັດຕະໂນມັດ (Real-time sync). ແຕ່ຖ້າຫາກບໍ່ໄດ້ຕັ້ງຄ່າ Google Sheets, ລະບົບກໍ່ຍັງສາມາດເຮັດວຽກໄດ້ປົກກະຕິ ໂດຍການບັນທຶກຂໍ້ມູນລົງໃນຖານຂໍ້ມູນ **SQLite** ແທນ.

## 2. ໂຄງສ້າງໂປຣເຈັກ (Project Structure)
- `frontend/`: ສ່ວນຕິດຕໍ່ຜູ້ໃຊ້ (UI) ພັດທະນາດ້ວຍ **Nuxt 3** (Vue.js) ແລະ Vuetify.
- `backend/`: ສ່ວນປະມວນຜົນ API ພັດທະນາດ້ວຍ **Node.js**, **Express**, ແລະ **Sequelize**.

---

## 3. ວິທີການຕິດຕັ້ງ (Installation)
ກ່ອນອື່ນໝົດ, ກະລຸນາກວດສອບວ່າທ່ານໄດ້ຕິດຕັ້ງ Node.js ໄວ້ໃນເຄື່ອງຄອມພິວເຕີຂອງທ່ານແລ້ວ.

**👉 ສຳລັບ Backend:**
1. ເປີດ Terminal ແລ້ວເຂົ້າໄປທີ່ໂຟນເດີ backend: `cd backend`
2. ຕິດຕັ້ງ Packages ຕ່າງໆ: `npm install`

**👉 ສຳລັບ Frontend:**
1. ເປີດ Terminal ແລ້ວເຂົ້າໄປທີ່ໂຟນເດີ frontend: `cd frontend`
2. ຕິດຕັ້ງ Packages ຕ່າງໆ: `npm install`

---

## 4. ວິທີການເປີດໃຊ້ງານ (How to Run)
ເພື່ອໃຫ້ແອັບພລິເຄຊັນເຮັດວຽກໄດ້ສົມບູນ, ທ່ານຕ້ອງເປີດທັງ Backend ແລະ Frontend ພ້ອມກັນ.

**ເປີດ Backend:**
ເຂົ້າໄປທີ່ໂຟນເດີ `backend` ແລ້ວພິມຄຳສັ່ງລຸ່ມນີ້ ເພື່ອສະຕາດເຊີບເວີ:
```bash
npm run dev
```
*(Backend ຈະເລີ່ມເຮັດວຽກຢູ່ທີ່ພອດ `http://localhost:3001`)*

**ເປີດ Frontend:**
ເຂົ້າໄປທີ່ໂຟນເດີ `frontend` ແລ້ວພິມຄຳສັ່ງ:
```bash
npm run dev
```
*(Frontend ຈະເລີ່ມເຮັດວຽກຢູ່ທີ່ພອດ `http://localhost:3000`)*

ເມື່ອເປີດສຳເລັດແລ້ວ, ທ່ານສາມາດເຂົ້າໄປທີ່ບຣາວເຊີ (Browser) ແລ້ວພິມ `http://localhost:3000/webview-manager` ເພື່ອເລີ່ມຕົ້ນນຳໃຊ້ໄດ້ເລີຍ!

---

## 5. ການຕັ້ງຄ່າ Google Sheets (Google Sheets Setup)
ຖ້າທ່ານຕ້ອງການໃຫ້ລະບົບບັນທຶກລີ້ງຕ່າງໆລົງໃນ Google Sheets ຂອງທ່ານໂດຍກົງ, ກະລຸນາປະຕິບັດຕາມຂັ້ນຕອນດັ່ງນີ້:

1. **ສ້າງ Google Sheet:** ສ້າງ Sheet ໃໝ່ ແລ້ວພິມຫົວຂໍ້ **Title** ຢູ່ຫ້ອງ `A1` ແລະ **URL** ຢູ່ຫ້ອງ `B1`.
2. **ແກ້ໄຂໄຟລ໌ `.env`:** ເຂົ້າໄປທີ່ໂຟນເດີ `backend/` ແລ້ວເປີດໄຟລ໌ `.env`.
3. **ໃສ່ Sheet ID:** ກັອບປີ້ ID ຂອງ Sheet (ຈາກ URL ດ້ານເທິງຂອງ Browser) ມາໃສ່ໃນຊ່ອງ `GOOGLE_SHEET_ID`.
4. **ໃສ່ Credentials:** ນຳເອົາ Email ຂອງ Service Account ມາໃສ່ໃນ `GOOGLE_CLIENT_EMAIL` ແລະ ນຳເອົາ Private Key (ທີ່ໄດ້ຈາກໄຟລ໌ JSON) ມາໃສ່ໃນ `GOOGLE_PRIVATE_KEY`.
5. **ແຊຣ໌ Sheet:** **(ສຳຄັນທີ່ສຸດ)** ຢ່າລືມກົດປຸ່ມ **Share** ຢູ່ໜ້າ Google Sheet ຂອງທ່ານ ແລ້ວນຳເອົາ Email ຂອງ Service Account ເຂົ້າໄປ ພ້ອມທັງກຳນົດສິດໃຫ້ເປັນ **Editor**.
6. **ເປີດໃຊ້ API:** ກວດສອບໃຫ້ແນ່ໃຈວ່າທ່ານໄດ້ກົດປຸ່ມ Enable ເພື່ອເປີດໃຊ້ງານ **Google Sheets API** ແລ້ວໃນ Google Cloud Console.

ເມື່ອຕັ້ງຄ່າສຳເລັດແລ້ວ, ເຊີບເວີຈະແຈ້ງເຕືອນວ່າ `✅ Connected to Google Sheet` ເຊິ່ງໝາຍຄວາມວ່າພ້ອມນຳໃຊ້ແລ້ວ!
