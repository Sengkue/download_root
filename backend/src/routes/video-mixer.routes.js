import express from 'express';
import { mixVideo } from '../controllers/videoMixer.controller.js';
import { cancelJob } from '../controllers/editor.controller.js';
import { upload } from '../middlewares/upload.middleware.js';

const router = express.Router();

router.post('/', upload.fields([
  { name: 'video', maxCount: 500 },
  { name: 'audio', maxCount: 100 },
  { name: 'logo', maxCount: 1 }
]), mixVideo);

router.post('/cancel', cancelJob);

export default router;
