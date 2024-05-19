import React, { useState } from 'react';
import axios from 'axios';
import "./Header.css"

const Header = ({ onVideoInfoChange }) => {
  const [url, setUrl] = useState(localStorage.getItem('savedUrl') || '');

  const handleChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSequentialRequests = async (url) => {
    try {
      await axios.get('http://localhost:5000/api/runOtherRequest');
      alert('Yêu cầu khác đã được gửi đến Flask thành công!');
  
      const response = await axios.post('http://localhost:5000/api/getInfo', { url });
      onVideoInfoChange(response.data);

      setInterval(async () => {
        try {
          const dataResponse = await axios.get('http://localhost:5000/api/data');
          console.log('Data response from Flask:', dataResponse.data);
        } catch (error) {
          console.error('Error fetching data from Flask:', error);
          alert('Đã xảy ra lỗi khi lấy dữ liệu từ Flask.');
        }
      }, 5000);
  
      await axios.post('http://localhost:5000/api/processUrl', { url }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      alert('Đường link đã được chuyển đến Flask thành công!');
      
      // Lưu giá trị đường dẫn vào Local Storage
      localStorage.setItem('savedUrl', url);

  
    } catch (error) {
      console.error('Error sending/receiving data from Flask:', error);
      alert('Đã xảy ra lỗi khi gửi yêu cầu đến Flask.');
    }
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (url.trim() !== '') {
      handleSequentialRequests(url);
    } else {
      alert('Vui lòng nhập đường link YouTube.');
    }
  };

  return (
    <div className='link'>
      <form onSubmit={handleSubmit}>
        <input type="text" value={url} onChange={handleChange} placeholder="Nhập đường link YouTube" />
        <button type="submit">Xác nhận</button>
      </form>
    </div>
  );
};

export default Header;