import express from 'express';
import { getVideos, addVideo, updateVideo, deleteVideo } from '../controllers/learningVideos.controller.js';

const router = express.Router();

router.get('/', getVideos);
router.post('/', addVideo);
router.put('/:id', updateVideo);
router.delete('/:id', deleteVideo);

export default router;
