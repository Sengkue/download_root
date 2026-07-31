import express from 'express';
import { downloadMedia, getInfo, getProgress } from '../controllers/download.controller.js';

const router = express.Router();

router.post('/download', downloadMedia);
router.post('/info', getInfo);
router.get('/progress', getProgress);

export default router;
