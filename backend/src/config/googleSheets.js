import { GoogleSpreadsheet } from 'google-spreadsheet';
import { JWT } from 'google-auth-library';
import fs from 'fs';
import path from 'path';

let doc = null;
let isConnected = false;

export const connectGoogleSheets = async () => {
  try {
    const sheetId = process.env.GOOGLE_SHEET_ID;
    let clientEmail = process.env.GOOGLE_CLIENT_EMAIL;
    let privateKey = process.env.GOOGLE_PRIVATE_KEY;

    // Fallback to google-credentials.json if .env variables are not set
    if (!clientEmail || !privateKey) {
      const credsPath = path.join(process.cwd(), 'google-credentials.json');
      if (!fs.existsSync(credsPath)) {
        console.log('⚠️ Google credentials not found in .env or google-credentials.json. Falling back to SQLite for Webview Links.');
        return false;
      }
      const creds = JSON.parse(fs.readFileSync(credsPath, 'utf8'));
      clientEmail = creds.client_email;
      privateKey = creds.private_key;
    }

    const serviceAccountAuth = new JWT({
      email: clientEmail,
      key: privateKey.replace(/\\n/g, '\n'), // handle newlines in .env
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    doc = new GoogleSpreadsheet(sheetId, serviceAccountAuth);
    await doc.loadInfo();
    console.log(`✅ Connected to Google Sheet: ${doc.title}`);
    isConnected = true;

    // Setup Typing Test Sheets
    try {
      let typingLessonsSheet = doc.sheetsByTitle['TypingLessons'];
      if (!typingLessonsSheet) {
        typingLessonsSheet = await doc.addSheet({ title: 'TypingLessons', headerValues: ['LessonID', 'Title', 'Content'] });
        await typingLessonsSheet.addRows([
          { LessonID: '1', Title: 'ບົດຮຽນທີ 1: ນິ້ວຊີ້ ແລະ ນິ້ວກາງຊ້າຍ (ກ ດ ເ)', Content: 'ກດເ ກດ ເດກ ກເ ດກ ດເ ກເດ ດເດ ກກເ ກດເ ດກເ ເດກ ກກດ ເເດ ກເດ' },
          { LessonID: '2', Title: 'ບົດຮຽນທີ 2: ນິ້ວຊີ້ ແລະ ນິ້ວກາງຂວາ (້ ່ າ)', Content: '້າ ່້ ່າ້ ້່າ ່່າ ້າ່ ້່ າ້ າ່ ້້່ ່້າ ້່າ າ້່ ່່າ' },
          { LessonID: '3', Title: 'ບົດຮຽນທີ 3: ປະສົມນິ້ວຊີ້-ກາງ (Home Row Core)', Content: 'ກ້າ ດ່ ເກ ດາ ເ້ ກ່ ດ້ ດ່າ ເກ້ ກດາ ເ່າ ດກ້ ເ້າ ກດ່ ດ່າ ເ້ກ' },
          { LessonID: '4', Title: 'ບົດຮຽນທີ 4: ນິ້ວນາງ ແລະ ນິ້ວກ້ອຍ (ັ ຫ ສ ວ ງ)', Content: 'ຫສ ວງ ັສ ກວ ຫງ ດສ ເວ ຫກ ດວ ສງ ັວ ຫສ ດງ ກສ ເຫ ວັ' },
          { LessonID: '5', Title: 'ບົດຮຽນທີ 5: ເອື້ອມນິ້ວແຖວເທິງ (ພ ະ ິ ີ ຮ ນ)', Content: 'ພະ ິີ ຮນ ຍບ ລພ ະິ ີຮ ນຍ ບລ ພິ ະຍ ະຮ ນບ ລີ ພບ ລນ ຍຮ' },
          { LessonID: '6', Title: 'ບົດຮຽນທີ 6: ປະສົມພະຍັນຊະນະ ແລະ ສະຫຼະ', Content: 'ກະ ກາ ກິ ກີ ກຶ ກື ກຸ ກູ ຂະ ຂາ ຂິ ຂີ ຂຶ ຂື ຂຸ ຂູ' }
        ]);
        console.log('✅ Created TypingLessons sheet with default Lao lessons.');
      }

      let typingResultsSheet = doc.sheetsByTitle['TypingResults'];
      if (!typingResultsSheet) {
        typingResultsSheet = await doc.addSheet({ title: 'TypingResults', headerValues: ['Date', 'LessonTitle', 'CPM', 'WPM', 'Accuracy'] });
        console.log('✅ Created TypingResults sheet.');
      }
    } catch (sheetErr) {
      console.error('⚠️ Could not setup Typing Test sheets (might be permission issue):', sheetErr.message);
    }

    return true;
  } catch (error) {
    console.error('❌ Failed to connect to Google Sheets:', error);
    return false;
  }
};

export const getGoogleSheetLinks = async () => {
  if (!isConnected) return null;
  const sheet = doc.sheetsByIndex[0];
  const rows = await sheet.getRows();
  return rows.map((row, index) => ({
    id: index,
    title: row.get('Title'),
    url: row.get('URL'),
  }));
};

export const addGoogleSheetLink = async (title, url) => {
  if (!isConnected) return null;
  const sheet = doc.sheetsByIndex[0];
  const row = await sheet.addRow({ Title: title, URL: url });
  const rows = await sheet.getRows();
  return { id: rows.length - 1, title, url };
};

export const deleteGoogleSheetLink = async (id) => {
  if (!isConnected) return false;
  const sheet = doc.sheetsByIndex[0];
  const rows = await sheet.getRows();
  if (rows[id]) {
    await rows[id].delete();
    return true;
  }
  return false;
};

export const updateGoogleSheetLink = async (id, title, url) => {
  if (!isConnected) return false;
  const sheet = doc.sheetsByIndex[0];
  const rows = await sheet.getRows();
  if (rows[id]) {
    rows[id].set('Title', title);
    rows[id].set('URL', url);
    await rows[id].save();
    return true;
  }
  return false;
};

// --- Typing Test Functions ---

export const getTypingLessons = async () => {
  if (!isConnected) return [];
  const sheet = doc.sheetsByTitle['TypingLessons'];
  if (!sheet) return [];
  const rows = await sheet.getRows();
  return rows.map(row => ({
    id: row.get('LessonID'),
    title: row.get('Title'),
    content: row.get('Content'),
  }));
};

export const saveTypingResult = async (lessonTitle, cpm, wpm, accuracy) => {
  if (!isConnected) return false;
  const sheet = doc.sheetsByTitle['TypingResults'];
  if (!sheet) return false;
  
  const date = new Date().toISOString();
  await sheet.addRow({ Date: date, LessonTitle: lessonTitle, CPM: cpm, WPM: wpm, Accuracy: accuracy });
  return true;
};

export const addTypingLesson = async (title, content) => {
  if (!isConnected) return null;
  const sheet = doc.sheetsByTitle['TypingLessons'];
  if (!sheet) return null;
  
  const rows = await sheet.getRows();
  const nextId = rows.length > 0 ? String(parseInt(rows[rows.length - 1].get('LessonID') || '0') + 1) : '1';
  
  const row = await sheet.addRow({ LessonID: nextId, Title: title, Content: content });
  return { id: nextId, title, content };
};
