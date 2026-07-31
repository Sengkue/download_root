import express from 'express';
import { getHomeLyrics, searchLyrics, getSongLyrics } from '../controllers/lyrics.controller.js';

const router = express.Router();

router.get('/home', getHomeLyrics);
router.get('/search', searchLyrics);
router.post('/song', getSongLyrics);

export default router;
