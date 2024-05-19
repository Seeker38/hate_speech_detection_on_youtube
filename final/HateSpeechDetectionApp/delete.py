from pymongo import MongoClient

def xoa_noi_dung_file(duong_dan_file):
    try:
        # Mở file ở chế độ ghi để xóa nội dung
        with open(duong_dan_file, 'w') as file:
            # Ghi một chuỗi rỗng để xóa nội dung
            file.write('')
        print("Đã xóa toàn bộ nội dung của file thành công.")
    except Exception as e:
        print(f"Lỗi: {e}")

def xoa_noi_dung_collection(db_name, collection_name):
    try:
        # Kết nối tới MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client[db_name]
        collection = db[collection_name]
        
        # Xóa toàn bộ dữ liệu trong collection
        result = collection.delete_many({})
        print(f"Đã xóa {result.deleted_count} tài liệu trong collection {collection_name}.")
    except Exception as e:
        print(f"Lỗi: {e}")

# Gọi hàm và truyền đường dẫn đến file cần xóa nội dung
duong_dan_file = 'D:/visomecens/comments.txt'  # Thay 'duong_dan_file.txt' bằng đường dẫn thực tế của bạn
xoa_noi_dung_file(duong_dan_file)

# Gọi hàm để xóa toàn bộ dữ liệu trong collection 'youtube_comment' của database 'youtube_comment'
xoa_noi_dung_collection('youtube_comment', 'youtube_comment')
