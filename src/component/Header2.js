import React, { useState, useEffect } from 'react';
import "./Header2.css"

const Header2 = ({ videoInfo, reloadCount}) => {
  useEffect(() => {
  }, [reloadCount]);

  return (
    <div key={reloadCount}>
      {videoInfo && (
        <div className='info'>
          <h2>Thông tin video</h2>
          <img src={videoInfo.thumbnail_url} alt="Thumbnail" />
          <p>{videoInfo.title}</p>
          <p>Người đăng: {videoInfo.uploader}</p>
          <p>Số bình luận: {videoInfo.comment_count}</p>
        </div>
      )}
    </div>
  );
};

export default Header2;
