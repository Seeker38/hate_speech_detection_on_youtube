import React from 'react';
import QRCode from 'qrcode.react';
import './QR.css'

const QR = ({ videoInfo }) => {
  return (
    <div className='qr'>
      <h2>Mong mọi người ủng hộ</h2>
      <p>URL: {videoInfo.video_url}</p>
      <QRCode value={videoInfo.video_url} size={175}/>
    </div>
  );
}

export default QR;
