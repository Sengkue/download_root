const fs = require('fs');
fetch('http://localhost:3001/api/lyrics/song', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://hmonglyrics.net/lyrics/cia-nws-dhau-mus/' })
})
.then(res => res.json())
.then(data => {
  fs.writeFileSync('C:\\sengkuevang\\coding\\full stack\\MeDownload\\frontend\\app\\pages\\lyrics\\temp_lyrics.json', JSON.stringify(data, null, 2));
});
