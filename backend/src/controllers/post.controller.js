import { Post } from '../models/Post.js';
import { User } from '../models/User.js';

export const createPost = async (req, res) => {
  try {
    const { description } = req.body;
    if (!req.file) return res.status(400).json({ error: 'Image file is required' });

    const post = await Post.create({
      userId: req.userId,
      image: `/uploads/${req.file.filename}`,
      description: description || ''
    });

    // Fetch the post with user details
    const newPost = await Post.findByPk(post.id, {
      include: [{ model: User, as: 'user', attributes: ['name', 'gender', 'location', 'profileImage'] }]
    });

    res.json({ post: newPost });
  } catch (err) {
    console.error('Upload error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const getLocalPosts = async (req, res) => {
  try {
    const posts = await Post.findAll({
      include: [{ model: User, as: 'user', attributes: ['name', 'gender', 'location', 'profileImage'] }],
      order: [['createdAt', 'DESC']]
    });
    res.json({ posts });
  } catch (err) {
    console.error('Fetch local posts error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};
