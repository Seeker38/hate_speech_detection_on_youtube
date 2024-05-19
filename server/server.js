const express = require('express');
const cors = require('cors');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());

app.get('/api/data', (req, res) => {
  const filePath = "D:/visomecens/comments.txt";

  fs.readFile(filePath, 'utf8', (err, data) => { // Sử dụng mã hóa UTF-8 khi đọc file
    if (err) {
      console.error('Error reading file:', err);
      return res.status(500).json({ error: 'Internal Server Error' });
    }

    try {
      const dataLines = data.trim().split('\n');
      const dataArray = [];
      dataLines.forEach(line => {
        const items = line.trim().split('",').map(item => item.trim());
        const obj = {};
        items.forEach(item => {
          const newLine = item.replace("{", "").replace("}", "")
          const [key, value] = newLine.split('":').map(item => item.trim().replace(/"/g, "").replace('"', ""));
          obj[key] = value;
        });
        dataArray.push(obj);
      });
      res.setHeader('Content-Type', 'application/json; charset=utf-8'); // Đảm bảo gửi dữ liệu JSON với mã hóa UTF-8
      res.json(dataArray);
    } catch (parseError) {
      console.error('Error parsing data:', parseError);
      res.status(500).json({ error: 'Error parsing data' });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
