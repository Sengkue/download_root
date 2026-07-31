import { getGoogleSheetLinks, addGoogleSheetLink, deleteGoogleSheetLink, updateGoogleSheetLink } from '../config/googleSheets.js';
import { WebviewLink } from '../models/WebviewLink.js';

export const getLinks = async (req, res) => {
  try {
    const googleLinks = await getGoogleSheetLinks();
    if (googleLinks) {
      return res.json(googleLinks);
    }
    const links = await WebviewLink.findAll({ order: [['createdAt', 'DESC']] });
    res.json(links);
  } catch (err) {
    console.error('Fetch webview links error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const createLink = async (req, res) => {
  try {
    const { title, url } = req.body;
    if (!title || !url) return res.status(400).json({ error: 'Title and URL are required' });

    const googleLink = await addGoogleSheetLink(title, url);
    if (googleLink) {
      return res.json(googleLink);
    }

    const newLink = await WebviewLink.create({ title, url });
    res.json(newLink);
  } catch (err) {
    console.error('Create webview link error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const deleteLink = async (req, res) => {
  try {
    const { id } = req.params;
    
    const isGoogleDeleted = await deleteGoogleSheetLink(id);
    if (isGoogleDeleted) {
      return res.json({ success: true });
    }

    const deleted = await WebviewLink.destroy({ where: { id } });
    if (!deleted) return res.status(404).json({ error: 'Link not found in SQLite' });
    res.json({ success: true });
  } catch (err) {
    console.error('Delete webview link error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

export const updateLink = async (req, res) => {
  try {
    const { id } = req.params;
    const { title, url } = req.body;
    
    if (!title || !url) return res.status(400).json({ error: 'Title and URL are required' });

    const isGoogleUpdated = await updateGoogleSheetLink(id, title, url);
    if (isGoogleUpdated) {
      return res.json({ success: true, link: { id: parseInt(id), title, url } });
    }

    const link = await WebviewLink.findByPk(id);
    if (!link) return res.status(404).json({ error: 'Link not found in SQLite' });
    
    link.title = title;
    link.url = url;
    await link.save();
    
    res.json({ success: true, link });
  } catch (err) {
    console.error('Update webview link error:', err);
    res.status(500).json({ error: 'Server error' });
  }
};
