import express from 'express';
import { getAuthUrl, authCallback, getConnectedChannels, uploadVideo } from '../controllers/tiktok.controller.js';

const router = express.Router();

router.get('/auth', getAuthUrl);
router.get('/callback', authCallback);
router.get('/channels', getConnectedChannels);
router.post('/upload', uploadVideo);

export default router;
