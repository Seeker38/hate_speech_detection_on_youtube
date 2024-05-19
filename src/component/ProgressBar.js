import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProgressBar = ({ videoInfo }) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:3001/api/data');
        let dataLines = 0; // Mặc định dataLines là 0

        if (response.data.length > 1) {
          dataLines = response.data.length; // Gán giá trị của dataLines nếu response.data.length lớn hơn 1
        }

        let percentProgress = 0;

        // Kiểm tra nếu videoInfo.comment_count không null và không bằng 1 trước khi tính toán phần trăm tiến độ
        if (videoInfo && videoInfo.comment_count !== null && videoInfo.comment_count !== 1) {
          percentProgress = (dataLines / videoInfo.comment_count) * 100;
          percentProgress = Math.round(percentProgress); // Làm tròn phần trăm tiến độ
        }

        setProgress(percentProgress); // Cập nhật giá trị tiến độ
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const interval = setInterval(fetchData, 500); // Lấy dữ liệu mỗi 0.5 giây

    return () => clearInterval(interval); // Hủy bỏ interval khi component bị unmount

  }, [videoInfo]);

  return (
    <div className="progress-bar">
      <div className="progress" style={{ width: `${progress}%` }}>
        {progress}%
      </div>
    </div>
  );
};

export default ProgressBar;
