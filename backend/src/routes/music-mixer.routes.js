import express from 'express';
import multer from 'multer';
import { mixVideo } from '../controllers/musicMixer.controller.js';

const router = express.Router();

const upload = multer({
  dest: 'tmp/uploads/',
  limits: { fileSize: 1000 * 1024 * 1024 }, // 1GB limit
});

router.post('/mix', upload.fields([
  { name: 'video', maxCount: 10 },
  { name: 'audio', maxCount: 50 },
  { name: 'logo', maxCount: 1 }
]), mixVideo);

export default router;
