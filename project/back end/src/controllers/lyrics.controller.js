import * as cheerio from 'cheerio';

export const getHomeLyrics = async (req, res) => {
  try {
    const response = await fetch('https://hmonglyrics.net/', {
       headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5'
       }
    });

    if (!response.ok) {
        return res.status(response.status).json({ error: `Failed to fetch hmonglyrics homepage: ${response.statusText}` });
    }

    const html = await response.text();
    const $ = cheerio.load(html);

    const featured = [];
    $('#popular-listr li.gradient').each((i, el) => {
        const title = $(el).find('h3 a').text().trim();
        const artist = $(el).find('.item-text > a').text().trim();
        const url = $(el).find('h3 a').attr('href');
        
        let bgStyle = $(el).attr('style') || '';
        let image = '';
        const imgMatch = bgStyle.match(/url\(['"]?(.*?)['"]?\)/);
        if (imgMatch && imgMatch[1]) {
            image = imgMatch[1];
        }

        if (title && url) {
            featured.push({ title, artist, url, image });
        }
    });

    const latest = [];
    $('.latest-lyrics li').each((i, el) => {
        const title = $(el).find('h5 a').text().trim();
        const artist = $(el).find('.lyric-content > a').text().trim();
        const url = $(el).find('h5 a').attr('href');
        
        if (title && url) {
            latest.push({ title, artist, url });
        }
    });

    res.json({ featured, latest });
  } catch (error) {
    console.error('Lyrics home proxy error:', error);
    res.status(500).json({ error: 'Backend failed to proxy the request.' });
  }
};

export const searchLyrics = async (req, res) => {
  try {
    const { q } = req.query;
    if (!q) return res.status(400).json({ error: 'Search query is required' });

    const searchUrl = `https://hmonglyrics.net/?s=${encodeURIComponent(q)}&post_type=lyrics`;
    const response = await fetch(searchUrl, {
       headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5'
       }
    });
    if (!response.ok) throw new Error(`Failed to fetch from hmonglyrics.net: ${response.status}`);
    
    const html = await response.text();
    const $ = cheerio.load(html);
    const results = [];

    $('.list-line').each((i, el) => {
       const titleEl = $(el).find('.col-lg-6 a');
       const artistEl = $(el).find('.col-lg-3').last().find('a');
       
       if (titleEl.length) {
         results.push({
            title: titleEl.text().trim(),
            url: titleEl.attr('href'),
            artist: artistEl.length ? artistEl.text().trim() : 'Unknown'
         });
       }
    });

    res.json({ results });
  } catch (error) {
    console.error('Lyrics search error:', error);
    res.status(500).json({ error: 'Failed to search lyrics' });
  }
};

export const getSongLyrics = async (req, res) => {
  try {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'Song URL is required' });

    const response = await fetch(url, {
       headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5'
       }
    });
    if (!response.ok) throw new Error(`Failed to fetch song from hmonglyrics.net: ${response.status}`);
    
    const html = await response.text();
    const $ = cheerio.load(html);

    const title = $('.lyrics-title h1').text().trim() || 'Unknown Title';
    const artist = $('.lyrics-title h3 a').text().trim() || 'Unknown Artist';

    let backgroundImage = '';
    const bgDiv = $('.background-single-lyrics');
    if (bgDiv.length) {
       const style = bgDiv.attr('style') || '';
       const match = style.match(/background:\s*url\(([^)]+)\)/);
       if (match && match[1]) backgroundImage = match[1].replace(/['"]/g, '');
    }

    let videoUrl = '';
    const iframe = $('.single-lyric-video iframe');
    if (iframe.length) {
       videoUrl = iframe.attr('src') || '';
    }

    const lyricDiv = $('.lyric-text');
    lyricDiv.find('.ads').remove();
    lyricDiv.find('script').remove();
    lyricDiv.find('ins').remove();
    lyricDiv.find('.related-list').remove();
    
    lyricDiv.find('br').replaceWith('\n');
    lyricDiv.find('p').each(function() {
       $(this).replaceWith($(this).text() + '\n\n');
    });

    const rawText = lyricDiv.text().trim();
    const cleanText = rawText.replace(/\n{3,}/g, '\n\n');

    res.json({
       title,
       artist,
       lyrics: cleanText,
       backgroundImage,
       videoUrl
    });
  } catch (error) {
    console.error('Lyrics fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch lyrics' });
  }
};
