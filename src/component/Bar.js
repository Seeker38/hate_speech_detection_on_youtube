import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './Bar.css'

const ColumnChart = ({ labelOccurrences }) => {
  const data = [
    { label: 'Tích cực', value: labelOccurrences.label0, fill: '#9acd32' },
    { label: 'Trung bình', value: labelOccurrences.label1, fill: 'rgb(255, 170, 0)' },
    { label: 'Tiêu cực', value: labelOccurrences.label2, fill: '#ff0000' }
  ];

  return (
    <div className='bar'>
      <h1>Biểu đồ thống kê</h1>
      <BarChart width={450} height={270} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="label" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="fill" />
      </BarChart>
    </div>
  );
};

export default ColumnChart;
