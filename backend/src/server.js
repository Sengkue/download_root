import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { connectDB } from './config/database.js';
import { connectGoogleSheets } from './config/googleSheets.js';
import routes from './routes/index.js';
import path from 'path';
import fs from 'fs';
import { uploadDir } from './middlewares/upload.middleware.js';

const app = express();
const PORT = process.env.PORT || 3001;

// Middlewares
app.use(cors());
app.use(express.json());

// Serve static uploads
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);
app.use('/uploads', express.static(uploadDir));

// Mount main router
app.use('/api', routes);

// Start Server
app.listen(PORT, async () => {
    await connectDB();
    await connectGoogleSheets();
    console.log(`🚀 Dedicated Backend server running on http://localhost:${PORT}`);
});
