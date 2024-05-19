import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ColumnChart from './Bar';
import './Feature.css';
import Comment from './Comment';
import QR from './QR';

const Feature = ({ selectedButton, commentKey, setCommentKey, onCommentError, videoInfo, onReload, reloadCount}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [commentKey, reloadCount]); 

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:3001/api/data');
      if (Array.isArray(response.data)) {
        setData(response.data);
        setLoading(false);
      } else {
        setError('Invalid data format. Please try again later.');
        setLoading(false);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Error fetching data. Please try again later.');
      setLoading(false);
    }
  };

  const countLabelOccurrences = () => {
    const labelCounts = { label0: 0, label1: 0, label2: 0 };
    data.forEach(item => {
      labelCounts[`label${item.label}`]++;
    });
    return labelCounts;
  };

  const findTopUsers = () => {
    const authorCounts = {};
    data.forEach(item => {
      if (!authorCounts[item.author]) {
        authorCounts[item.author] = 1;
      } else {
        authorCounts[item.author]++;
      }
    });

    const sortedAuthors = Object.entries(authorCounts).sort(([, a], [, b]) => b - a);
    const topUsers = sortedAuthors.slice(0, 5);

    return topUsers;
  };

  const findTopUsersWithLabel2 = () => {
    const authorsWithLabel2 = {};
    data.forEach(item => {
      if (item.label === '2' || item.label === '1') {
        if (!authorsWithLabel2[item.author]) {
          authorsWithLabel2[item.author] = 1;
        } else {
          authorsWithLabel2[item.author]++;
        }
      }
    });

    const sortedAuthors = Object.entries(authorsWithLabel2).sort(([, a], [, b]) => b - a);
    const topUsersWithLabel2 = sortedAuthors.slice(0, 3);

    return topUsersWithLabel2;
  };

  const deleteAll = async () => {
    try {
      const response = await axios.delete('http://localhost:5000/api/deleteCommentsAll');
      window.location.reload();
      if (!response.data.success) {
        console.log(response.data.error);
        window.location.reload();
      } else {
        window.location.reload(); // Reload trang web ngay lập tức
      }
    } catch (error) {
      console.error('Error deleting comment:', error);
      //window.location.reload();
      // onCommentError('Error deleting comment. Please try again later.'); // Gọi hàm để thông báo lỗi từ Comment
    }
  };

  const deleteCommentByAuthor = async (author) => {
    try {
      console.log(author)
      const response = await axios.delete(`http://localhost:5000/api/deleteCommentAuthor/${author}`);
      // window.location.reload();
      if (!response.data.success) {
        alert(response.data.error);
      } 
      else {
        window.location.reload(); // Reload trang web ngay lập tức
      }
    } catch (error) {
      console.error('Error deleting comment:', error);
      onCommentError('Error deleting comment. Please try again later.'); 
      window.location.reload();
    }
  };

  const renderSelectedInfo = () => {
    switch (selectedButton) {
      case 1:
        const labelOccurrences1 = countLabelOccurrences();
        return (
          <div className='report'>
            <h1>Thống kê trên số bình luận</h1>
            <p>Tổng số bình luận là: {data.length}</p>
            <p>Số bình luận <span className='fuck1'>tiêu cực</span> là: {labelOccurrences1.label2}</p>
            <p>Số bình luận <span className='fuck2'>trung tính</span> là: {labelOccurrences1.label1}</p>
            <p>Số bình luận <span className='fuck3'>tích cực</span> là: {labelOccurrences1.label0}</p>
          </div>
        );
      case 2:
        const labelOccurrences2 = countLabelOccurrences();
        return (
          <div className='report'>
            <ColumnChart labelOccurrences={labelOccurrences2} />
          </div>
        );
      case 3:
        const topUsers = findTopUsers();
        return (
          <div className='report'>
            <h1>Top người dùng đóng góp </h1>
            {topUsers.map(([author, count], index) => (
              <p key={index}><span className='helper'>{author}</span>: {count} lần ủng hộ</p>
            ))}
          </div>
        );
        case 4:
          const topUsersWithLabel2 = findTopUsersWithLabel2();
          return (
            <div className='report'>
              <h1>Top người dùng gây rối</h1>
              {topUsersWithLabel2.map(([author, count], index) => (
                <div className='block' key={index}>
                  <p><span>{author}</span>: {count} lần gây rối</p>
                  <button onClick={() => { deleteCommentByAuthor(author); onReload(); }}>Chặn {author}</button>
                </div>
              ))}
              <button className='deleteAll' onClick={() => { deleteAll(); onReload(); }}>Xóa toàn bộ</button>
            </div>
          );
        case 5:
          return (
            <div className='statistic'>
              <Comment videoInfo={videoInfo} className='st' onCommentError={onCommentError} onReload={onReload} reloadCount={reloadCount}/> {/* Truyền hàm xử lý thông báo lỗi */}
              <p>{videoInfo.video_url}</p>
            </div>
          );
        case 6:
          return (
            <div className='statistic'>
              <QR videoInfo={videoInfo} className='st' /> 
            </div>
          );
      default:
        return <p>Vui lòng chọn một nút để xem thông tin.</p>;
    }
  };

  return (
    <div className="feature-container">
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>{error}</p>
        ) : (
          renderSelectedInfo()
        )}
    </div>
  );
};

export default Feature;
