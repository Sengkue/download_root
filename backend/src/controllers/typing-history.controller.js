import { TypingHistory } from '../models/TypingHistory.js';

export const saveHistory = async (req, res) => {
  try {
    const { lessonTitle, wpm, cpm, accuracy, timeSeconds } = req.body;
    
    if (!lessonTitle) {
      return res.status(400).json({ error: 'Lesson Title is required' });
    }

    const history = await TypingHistory.create({
      userId: req.userId,
      lessonTitle,
      wpm: wpm || 0,
      cpm: cpm || 0,
      accuracy: accuracy || 0,
      timeSeconds
    });

    res.json({ success: true, data: history });
  } catch (err) {
    console.error('Save typing history error:', err);
    res.status(500).json({ error: 'Server error while saving typing history' });
  }
};

export const getHistory = async (req, res) => {
  try {
    const history = await TypingHistory.findAll({
      where: { userId: req.userId },
      order: [['createdAt', 'DESC']]
    });
    
    res.json(history);
  } catch (err) {
    console.error('Get typing history error:', err);
    res.status(500).json({ error: 'Server error while fetching typing history' });
  }
};
