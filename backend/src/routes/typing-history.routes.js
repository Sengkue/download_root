import express from 'express';
import { saveHistory, getHistory } from '../controllers/typing-history.controller.js';
import { authMiddleware } from '../middlewares/auth.middleware.js';

const router = express.Router();

// All typing history routes require authentication
router.use(authMiddleware);

router.post('/', saveHistory);
router.get('/', getHistory);

export default router;
