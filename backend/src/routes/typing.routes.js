import express from 'express';
import { 
  getTypingLessons, 
  createTypingLesson, 
  postTypingResult, 
  getTypingLeaderboard,
  updateTypingLesson, 
  deleteTypingLesson 
} from '../controllers/typing.controller.js';

const router = express.Router();

router.get('/typing-lessons', getTypingLessons);
router.post('/typing-lessons', createTypingLesson);
router.post('/typing-results', postTypingResult);
router.get('/typing-leaderboard', getTypingLeaderboard);
router.put('/typing-lessons/:id', updateTypingLesson);
router.delete('/typing-lessons/:id', deleteTypingLesson);

export default router;
