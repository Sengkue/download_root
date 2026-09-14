import express from 'express';
import authRoutes from './auth.routes.js';
import postRoutes from './post.routes.js';
import webviewRoutes from './webview.routes.js';
import chatRoutes from './chat.routes.js';
import downloadRoutes from './download.routes.js';
import searchRoutes from './search.routes.js';
import lyricsRoutes from './lyrics.routes.js';
import typingRoutes from './typing.routes.js';
import editorRoutes from './editor.routes.js';
import videoMixerRoutes from './video-mixer.routes.js';
import typingHistoryRoutes from './typing-history.routes.js';
import learningVideosRoutes from './learningVideos.routes.js';

const router = express.Router();

router.use('/auth', authRoutes);
router.use('/posts', postRoutes);
router.use('/webview-links', webviewRoutes);
router.use('/chat', chatRoutes);
router.use('/search', searchRoutes);
router.use('/lyrics', lyricsRoutes);
router.use('/editor', editorRoutes);
router.use('/video-mixer', videoMixerRoutes);
router.use('/typing-history', typingHistoryRoutes);
router.use('/learning-videos', learningVideosRoutes);

// These routers define top-level /api endpoints (e.g. /api/download, /api/info, /api/typing-lessons)
router.use('/', downloadRoutes);
router.use('/', typingRoutes);

export default router;
