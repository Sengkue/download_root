import { 
  getTypingLessons as fetchLessons, 
  addTypingLesson, 
  saveTypingResult, 
  getTypingLeaderboard as fetchLeaderboard,
  updateTypingLesson as updateLessonSheet, 
  deleteTypingLesson as deleteLessonSheet 
} from '../config/googleSheets.js';

export const getTypingLessons = async (req, res) => {
  try {
    const lessons = await fetchLessons();
    res.json(lessons);
  } catch (err) {
    console.error('Fetch typing lessons error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const createTypingLesson = async (req, res) => {
  try {
    const { title, content } = req.body;
    if (!title || !content) return res.status(400).json({ error: 'Title and content are required' });
    
    const newLesson = await addTypingLesson(title, content);
    if (newLesson) {
      res.json(newLesson);
    } else {
      res.status(500).json({ error: 'Failed to save lesson to Google Sheets' });
    }
  } catch (err) {
    console.error('Create typing lesson error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const postTypingResult = async (req, res) => {
  try {
    const { username, lessonTitle, cpm, wpm, accuracy, timeSeconds } = req.body;
    if (!lessonTitle) return res.status(400).json({ error: 'Lesson Title is required' });
    
    const success = await saveTypingResult(username, lessonTitle, cpm, wpm, accuracy, timeSeconds);
    if (success) {
      res.json({ success: true });
    } else {
      res.status(500).json({ error: 'Failed to save to Google Sheets' });
    }
  } catch (err) {
    console.error('Save typing result error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const getTypingLeaderboard = async (req, res) => {
  try {
    const { lessonTitle } = req.query;
    const leaderboard = await fetchLeaderboard(lessonTitle);
    res.json(leaderboard);
  } catch (err) {
    console.error('Fetch typing leaderboard error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const updateTypingLesson = async (req, res) => {
  try {
    const { id } = req.params;
    const { title, content } = req.body;
    if (!id || !title || !content) return res.status(400).json({ error: 'ID, title and content are required' });
    
    const success = await updateLessonSheet(id, title, content);
    if (success) {
      res.json({ success: true, id, title, content });
    } else {
      res.status(500).json({ error: 'Failed to update lesson in Google Sheets' });
    }
  } catch (err) {
    console.error('Update typing lesson error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const deleteTypingLesson = async (req, res) => {
  try {
    const { id } = req.params;
    if (!id) return res.status(400).json({ error: 'ID is required' });
    
    const success = await deleteLessonSheet(id);
    if (success) {
      res.json({ success: true, id });
    } else {
      res.status(500).json({ error: 'Failed to delete lesson from Google Sheets' });
    }
  } catch (err) {
    console.error('Delete typing lesson error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};
