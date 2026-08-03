import express from 'express';
import { mergeMedia } from '../controllers/editor.controller.js';
import { upload } from '../middlewares/upload.middleware.js';

const router = express.Router();

router.post('/merge', upload.fields([
  { name: 'image', maxCount: 50 },
  { name: 'audio', maxCount: 1 }
]), mergeMedia);

export default router;
