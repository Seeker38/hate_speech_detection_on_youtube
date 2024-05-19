const axios = require('axios');

const fetchData = async () => {
  try {
    const response = await axios.get('http://localhost:3001/api/data');
    console.log('Data retrieved:', response.data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

fetchData();
