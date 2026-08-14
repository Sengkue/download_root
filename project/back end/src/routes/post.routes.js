import express from 'express';
import { createPost, getLocalPosts } from '../controllers/post.controller.js';
import { authMiddleware } from '../middlewares/auth.middleware.js';
import { upload } from '../middlewares/upload.middleware.js';

const router = express.Router();

router.post('/upload', authMiddleware, upload.single('image'), createPost);
router.get('/local', getLocalPosts);

export default router;
