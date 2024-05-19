import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Comment.css';

function Comment({ videoInfo, onCommentError, onReload, reloadCount }) {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [serverError, setServerError] = useState(null); 
  const [authorSort, setAuthorSort] = useState(null);

  useEffect(() => {
    fetchData();
  }, [reloadCount]);

  const columnNameMap = {
    comment_id: 'ID',
    author: 'Người dùng',
    datetime: 'Thời gian',
    raw_comment: 'Bình luận gốc',
    clean_comment: 'Bình luận sửa',
    label: 'Nhãn'
  };

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:3001/api/data');
      if (Array.isArray(response.data) && response.data.length > 0) {
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

  const deleteRow = async (commentId, videoUrl) => {
    try {
      const response = await axios.delete(`http://localhost:5000/api/deleteComment/${commentId}`, {
        data: {
          videoUrl: videoUrl
        }
      });
      console.log(response.data);
      if (!response.data.success) {
        alert(response.data.error);
      } else {
        window.location.reload(); // Reload trang web ngay lập tức
      }
    } catch (error) {
      console.error('Error deleting comment:', error);
      alert('Error deleting comments. Please try again later.');
      onCommentError('Error deleting comment. Please try again later.'); // Gọi hàm để thông báo lỗi từ Comment
    }
  };

  const sortDataByDateTime = () => {
    const sortedData = [...data].sort((a, b) => {
      return new Date(b.datetime) - new Date(a.datetime);
    });

    if (authorSort) {
      const priorityData = sortedData.filter(item => item.author === authorSort);
      const nonPriorityData = sortedData.filter(item => item.author !== authorSort);
      setFilteredData([...priorityData, ...nonPriorityData]);
    } else {
      setFilteredData(sortedData);
    }
  };

  const handleAuthorClick = (author) => {
    setAuthorSort(author);
    sortDataByDateTime();
  };



  useEffect(() => {
    const timeout = setTimeout(() => {
      sortDataByDateTime();
    }, 100);
    return () => clearTimeout(timeout);
  }, [data, authorSort]);

  return (
    <div className="CommentAll">
      <div className='comment'>  
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>{error}</p>
        ) : (
          <React.Fragment>
            {serverError && <p>{serverError}</p>} 
            <table className='commentTable'>
              <thead className='tableHead'>
                <tr>
                  {Object.keys(data[0]).map((key, index) => (
                    <th key={index} className={`column-${index}`}>
                      {columnNameMap[key] ? columnNameMap[key] : key}
                    </th>
                  ))}
                  <th className='delete'>Loại bỏ</th>
                </tr>
              </thead>
              <tbody className='tableBody'>
                {filteredData.map((item, rowIndex) => (
                  <tr key={rowIndex} className='row'>
                    {Object.entries(item).map(([key, value], colIndex) => (
                      <td key={colIndex} className={`column-${colIndex}`}>
                        {key === 'author' ? (
                          <button className='authorBtn' onClick={() => handleAuthorClick(value)}>
                            {value}
                          </button>
                        ) : (
                          value
                        )}
                      </td>
                    ))}
                    <td className='delete'>
                      <button className='deleteBt' onClick={() => { deleteRow(item.comment_id, videoInfo.video_url); onReload(); }}>Xóa</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </React.Fragment>
        )}
      </div>
    </div>
  );
}

export default Comment;
