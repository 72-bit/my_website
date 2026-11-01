const express = require('express');
const app = express();
const PORT = 3000;

// Cho phép server đọc dữ liệu dạng JSON từ client gửi lên
app.use(express.json());

// Phục vụ file HTML giao diện
app.use(express.static('public'));

// API nhận tín hiệu khi nút được nhấn
app.post('/api/click', (req, res) => {
    console.log('Đã nhận được tín hiệu nhấn nút từ client!');
    
    // Bạn có thể lấy thêm dữ liệu nếu client gửi kèm
    const { time } = req.body;
    console.log(`Thời gian bấm: ${time}`);

    // Phản hồi lại cho client
    res.json({ 
        status: 'success', 
        message: 'Server đã ghi nhận cú click thành công!' 
    });
});

app.listen(PORT, () => {
    console.log(`Server đang chạy tại: http://localhost:${PORT}`);
});
