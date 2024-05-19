import React, { useState } from 'react';

const Header1 = ({ onRequestsSubmit }) => {
  const [url, setUrl] = useState('');

  const handleChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (url.trim() !== '') { // Kiểm tra xem đường link có tồn tại không trước khi gửi yêu cầu
      onRequestsSubmit(url);
    } else {
      alert('Vui lòng nhập đường link YouTube.');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" value={url} onChange={handleChange} placeholder="Nhập đường link YouTube" />
        <button type="submit">Xác nhận</button>
      </form>
    </div>
  );
};

export default Header1;
