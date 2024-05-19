const axios = require('axios');

const deleteAllComments = async () => {
    try {
        const response = await axios.delete('http://localhost:5000/api/deleteCommentsAll');
        if (response.data.success) {
            console.log('Thực hiện thành công');
        } else {
            console.error('Lỗi khi thực hiện:', response.data.error);
        }
    } catch (error) {
        console.error('Lỗi khi thực hiện:', error.message);
    }
};

deleteAllComments();
