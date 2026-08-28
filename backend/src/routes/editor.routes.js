import express from 'express';
import { mergeMedia, cancelJob } from '../controllers/editor.controller.js';
import { upload } from '../middlewares/upload.middleware.js';

const router = express.Router();

router.post('/merge', upload.fields([
  { name: 'image', maxCount: 50 },
  { name: 'audio', maxCount: 20 }
]), mergeMedia);

router.post('/cancel', cancelJob);

export default router;
