import React, { useState, useEffect } from 'react';
import './App.css';
import Header from "./component/Header";
import Loader from './component/Loader';
import Header2 from './component/Header2';
import Feature from "./component/Feature"
import ProgressBar from './component/ProgressBar';
import { FiAlignJustify } from "react-icons/fi";
import { FaChartSimple } from "react-icons/fa6";
import { MdOutlineAnalytics } from "react-icons/md";
import { HiTrophy } from "react-icons/hi2";
import { BsPersonFillExclamation } from "react-icons/bs";
import { PiAddressBookFill } from "react-icons/pi";
import { MdOutlineQrCodeScanner } from "react-icons/md";
import axios from 'axios';

function App() {
  const [selectedButton, setSelectedButton] = useState(null);
  const [commentKey, setCommentKey] = useState(0);
  const [videoInfo, setVideoInfo] = useState(null);
  const [progressValue, setProgressValue] = useState(0);
  const [reloadCount, setReloadCount] = useState(0);

  const handleButtonClick = (button) => {
    setSelectedButton(button);
    setCommentKey(prevKey => prevKey + 1);
  };

  const handleReload = () => {
    setReloadCount(reloadCount + 1);
  };

  const handleVideoInfoChange = (info) => {
    setVideoInfo(info);
  };

  const handleCommentError = (error) => {
    alert(error);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setVideoInfo(prevInfo => ({ ...prevInfo }));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:3001/api/data');
        let dataLines = 0;

        if (response.data.length > 1) {
          dataLines = response.data.length;
        }

        let percentProgress = 0;

        if (videoInfo && videoInfo.comment_count !== null && videoInfo.comment_count !== 1) {
          percentProgress = (dataLines / videoInfo.comment_count) * 100;
          percentProgress = Math.round(percentProgress);
        }

        setProgressValue(percentProgress);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const interval = setInterval(fetchData, 500);

    return () => clearInterval(interval);

  }, [videoInfo]);

  return (
    <div className="App">
      <div className="mainApp">
        <div className="mainButton">
          <button className='topmainBt'>
            <FiAlignJustify size={35} color='#fff'/>
          </button>
          <button className='mainBt' onClick={() => handleButtonClick(5)}>
            <PiAddressBookFill size={35} color='#fff'/>
          </button>
          <button className='mainBt' onClick={() => handleButtonClick(1)}>
            <MdOutlineAnalytics size={35} color='#fff'/>
          </button>
          <button className='mainBt' onClick={() => handleButtonClick(2)}>
            <FaChartSimple size={35} color='#fff'/>
          </button>
          <button className='mainBt' onClick={() => handleButtonClick(3)}>
            <HiTrophy size={35} color='#fff'/>
          </button>
          <button className='mainBt' onClick={() => handleButtonClick(4)}>
            <BsPersonFillExclamation size={35} color='#fff'/>
          </button>
          <button className='mainBt' onClick={() => handleButtonClick(6)}>
            <MdOutlineQrCodeScanner size={35} color='#fff'/>
          </button>
        </div>
        <div className='detailApp'>
          <div className="charts">
            <Header classNamec='c1' onVideoInfoChange={handleVideoInfoChange}/>
            {progressValue < 100 && videoInfo && videoInfo.title && (
              <>
                <Loader></Loader>
                <ProgressBar videoInfo={videoInfo}/>
              </>
            )}
            {progressValue >= 100 && videoInfo && videoInfo.video_url && (
                <Feature className='c2' selectedButton={selectedButton} commentKey={commentKey} setCommentKey={setCommentKey} onCommentError={handleCommentError} videoInfo={videoInfo} onReload={handleReload} reloadCount={reloadCount}/>
            )}
          </div>
          <div className='profileApp'>
              {videoInfo && videoInfo.title && <Header2 videoInfo={videoInfo}/>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;