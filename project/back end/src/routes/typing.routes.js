import express from 'express';
import { getTypingLessons, createTypingLesson, postTypingResult } from '../controllers/typing.controller.js';

const router = express.Router();

router.get('/typing-lessons', getTypingLessons);
router.post('/typing-lessons', createTypingLesson);
router.post('/typing-results', postTypingResult);

export default router;
