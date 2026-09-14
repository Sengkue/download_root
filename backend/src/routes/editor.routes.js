import express from 'express';
import { mergeMedia, cancelJob } from '../controllers/editor.controller.js';
import { upload } from '../middlewares/upload.middleware.js';

const router = express.Router();

router.post('/merge', upload.fields([
  { name: 'image', maxCount: 500 },
  { name: 'audio', maxCount: 100 }
]), mergeMedia);

router.post('/cancel', cancelJob);

export default router;
