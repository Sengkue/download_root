const { GoogleSpreadsheet } = require('google-spreadsheet');
const { JWT } = require('google-auth-library');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function fixCategory() {
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

    let learningVideosSheet = doc.sheetsByTitle['LearningVideos'];
    if (learningVideosSheet) {
      const rows = await learningVideosSheet.getRows();
      let updated = false;
      for (const row of rows) {
        if (row.get('ID') === 'h2') {
          row.set('Category', 'hmong-video');
          await row.save();
          console.log('Successfully updated Category of h2 to hmong-video');
          updated = true;
          break;
        }
      }
      if (!updated) {
        console.log('Row with ID h2 not found in LearningVideos sheet.');
      }
    } else {
      console.log('LearningVideos sheet not found');
    }
  } catch (err) {
    console.error('Error updating sheet:', err);
  }
}

fixCategory();
