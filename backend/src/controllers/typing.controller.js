import { getTypingLessons as fetchLessons, addTypingLesson, saveTypingResult } from '../config/googleSheets.js';

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
    const { lessonTitle, cpm, wpm, accuracy } = req.body;
    if (!lessonTitle) return res.status(400).json({ error: 'Lesson Title is required' });
    
    const success = await saveTypingResult(lessonTitle, cpm, wpm, accuracy);
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
