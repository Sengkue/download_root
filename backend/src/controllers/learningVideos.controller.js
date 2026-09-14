import { getLearningVideos, addLearningVideo, updateLearningVideo, deleteLearningVideo } from '../config/googleSheets.js';

export const getVideos = async (req, res) => {
  try {
    const videos = await getLearningVideos();
    res.json(videos);
  } catch (error) {
    console.error('Error fetching learning videos:', error);
    res.status(500).json({ error: 'Failed to fetch videos' });
  }
};

export const addVideo = async (req, res) => {
  try {
    const data = req.body;
    const newVideo = await addLearningVideo(data);
    if (newVideo) {
      res.status(201).json(newVideo);
    } else {
      res.status(500).json({ error: 'Database not connected' });
    }
  } catch (error) {
    console.error('Error adding learning video:', error);
    res.status(500).json({ error: 'Failed to add video' });
  }
};

export const updateVideo = async (req, res) => {
  try {
    const { id } = req.params;
    const data = req.body;
    const success = await updateLearningVideo(id, data);
    if (success) {
      res.json({ success: true });
    } else {
      res.status(404).json({ error: 'Video not found or database not connected' });
    }
  } catch (error) {
    console.error('Error updating learning video:', error);
    res.status(500).json({ error: 'Failed to update video' });
  }
};

export const deleteVideo = async (req, res) => {
  try {
    const { id } = req.params;
    const success = await deleteLearningVideo(id);
    if (success) {
      res.json({ success: true });
    } else {
      res.status(404).json({ error: 'Video not found or database not connected' });
    }
  } catch (error) {
    console.error('Error deleting learning video:', error);
    res.status(500).json({ error: 'Failed to delete video' });
  }
};
