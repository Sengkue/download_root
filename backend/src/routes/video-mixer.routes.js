import express from 'express';
import { mixVideo } from '../controllers/videoMixer.controller.js';
import { upload } from '../middlewares/upload.middleware.js';

const router = express.Router();

router.post('/', upload.fields([
  { name: 'video', maxCount: 50 },
  { name: 'audio', maxCount: 1 }
]), mixVideo);

export default router;
