const { GoogleSpreadsheet } = require('google-spreadsheet');
const { JWT } = require('google-auth-library');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function updateSheet() {
  try {
    let clientEmail = process.env.GOOGLE_CLIENT_EMAIL;
    let privateKey = process.env.GOOGLE_PRIVATE_KEY;

    if (!clientEmail || !privateKey) {
      const credsPath = path.join(process.cwd(), 'google-credentials.json');
      if (!fs.existsSync(credsPath)) {
        console.error('Credentials not found!');
        return;
      }
      const creds = JSON.parse(fs.readFileSync(credsPath, 'utf8'));
      clientEmail = creds.client_email;
      privateKey = creds.private_key;
    }

    const serviceAccountAuth = new JWT({
      email: clientEmail,
      key: privateKey.replace(/\\n/g, '\n'),
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    const doc = new GoogleSpreadsheet(process.env.GOOGLE_SHEET_ID, serviceAccountAuth);
    await doc.loadInfo();

    let typingLessonsSheet = doc.sheetsByTitle['TypingLessons'];
    if (typingLessonsSheet) {
      await typingLessonsSheet.clear();
      await typingLessonsSheet.setHeaderRow(['LessonID', 'Title', 'Content']);
      await typingLessonsSheet.addRows([
          { LessonID: '1', Title: 'ບົດຮຽນທີ 1: ນິ້ວຊີ້ ແລະ ນິ້ວກາງຊ້າຍ (ກ ດ ເ)', Content: 'ກດເ ກດ ເດກ ກເ ດກ ດເ ກເດ ດເດ ກກເ ກດເ ດກເ ເດກ ກກດ ເເດ ກເດ' },
          { LessonID: '2', Title: 'ບົດຮຽນທີ 2: ນິ້ວຊີ້ ແລະ ນິ້ວກາງຂວາ (້ ່ າ)', Content: '້າ ່້ ່າ້ ້່າ ່່າ ້າ່ ້່ າ້ າ່ ້້່ ່້າ ້່າ າ້່ ່່າ' },
          { LessonID: '3', Title: 'ບົດຮຽນທີ 3: ປະສົມນິ້ວຊີ້-ກາງ (Home Row Core)', Content: 'ກ້າ ດ່ ເກ ດາ ເ້ ກ່ ດ້ ດ່າ ເກ້ ກດາ ເ່າ ດກ້ ເ້າ ກດ່ ດ່າ ເ້ກ' },
          { LessonID: '4', Title: 'ບົດຮຽນທີ 4: ນິ້ວນາງ ແລະ ນິ້ວກ້ອຍ (ັ ຫ ສ ວ ງ)', Content: 'ຫສ ວງ ັສ ກວ ຫງ ດສ ເວ ຫກ ດວ ສງ ັວ ຫສ ດງ ກສ ເຫ ວັ' },
          { LessonID: '5', Title: 'ບົດຮຽນທີ 5: ເອື້ອມນິ້ວແຖວເທິງ (ພ ະ ິ ີ ຮ ນ)', Content: 'ພະ ິີ ຮນ ຍບ ລພ ະິ ີຮ ນຍ ບລ ພິ ະຍ ະຮ ນບ ລີ ພບ ລນ ຍຮ' },
          { LessonID: '6', Title: 'ບົດຮຽນທີ 6: ປະສົມພະຍັນຊະນະ ແລະ ສະຫຼະ', Content: 'ກະ ກາ ກິ ກີ ກຶ ກື ກຸ ກູ ຂະ ຂາ ຂິ ຂີ ຂຶ ຂື ຂຸ ຂູ' }
      ]);
      console.log('Successfully updated TypingLessons sheet with Advanced Drills!');
    } else {
        console.log('TypingLessons sheet not found');
    }
  } catch (err) {
    console.error('Error updating sheet:', err);
  }
}

updateSheet();
