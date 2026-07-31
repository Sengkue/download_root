export const searchImages = async (req, res) => {
  try {
    const { key, q, image_type, per_page, page, video } = req.query;
    
    if (!key || !q) {
        return res.status(400).json({ error: 'Pixabay API key and search query are required.' });
    }

    let url = '';
    if (video === 'true') {
        url = `https://pixabay.com/api/videos/?key=${key}&q=${encodeURIComponent(q)}&per_page=${per_page || 30}&page=${page || 1}`;
    } else {
        url = `https://pixabay.com/api/?key=${key}&q=${encodeURIComponent(q)}&image_type=${image_type || 'photo'}&per_page=${per_page || 30}&page=${page || 1}`;
    }

    const response = await fetch(url);
    if (!response.ok) {
        return res.status(response.status).json({ error: `Pixabay API Connection Error: ${response.statusText}` });
    }

    const data = await response.json();
    return res.json(data);
  } catch (error) {
    console.error('Search proxy error:', error);
    res.status(500).json({ error: 'Backend failed to proxy the search request to Pixabay.' });
  }
};
