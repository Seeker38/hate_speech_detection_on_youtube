from Google import Create_Service
import sys
import json
from pymongo import MongoClient

# from googleapiclient.discovery import build


# YouTube Data API v3 constants
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# OAuth 2.0 details
CLIENT_SECRETS_FILE = "D:/final/client_secret_148935655409-4n4t3telal25ikp5r34n69l8pmti05sj.apps.googleusercontent.com.json"
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtubepartner',
]
service = Create_Service(CLIENT_SECRETS_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)


def delete_record(comment_id):
    # Đọc nội dung từ tệp comments.txt và lưu vào danh sách
    with open('D:\\final\\comments.txt', 'r', encoding='utf-8') as file:
        comments = file.readlines()

    # Tạo danh sách mới để lưu các bản ghi đã cập nhật
    updated_comments = []

    # Xóa bản ghi có comment_id tương ứng khỏi danh sách
    for comment in comments:
        comment_data = json.loads(comment)
        if comment_data.get('comment_id') != comment_id:
            updated_comments.append(comment)

    # Ghi lại danh sách dữ liệu đã được cập nhật vào tệp comments.txt
    with open('D:\\final\\comments.txt', 'w', encoding='utf-8') as file:
        file.writelines(updated_comments)
        
def delete_record_mongo(db_name, collection_name, comment_id):
    try:
        # Kết nối tới MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client[db_name]
        collection = db[collection_name]
        
        # Xóa tài liệu có comment_id trùng với giá trị biến truyền vào
        result = collection.delete_one({'comment_id': comment_id})
        if result.deleted_count > 0:
            print(f"Đã xóa tài liệu có comment_id: {comment_id}")
        else:
            print(f"Không tìm thấy tài liệu có comment_id: {comment_id}")
    except Exception as e:
        print(f"Lỗi: {e}")


def reject_comment(comment_id):
    # Cập nhật trạng thái kiểm duyệt của bình luận thành 'published'
    service.comments().setModerationStatus(
        id=comment_id,
        moderationStatus='rejected',
        banAuthor=False
    ).execute()
    delete_record(comment_id)
    delete_record_mongo('youtube_comment', 'youtube_comment', comment_id)



def reject_comments(comment_ids):
    for comment_id in comment_ids:
        try:
            reject_comment(comment_id)
            print(f"successfully rejected comment: {comment_id}")
        except Exception as e:
            print(f"Fail to reject comment {comment_id}. Error: {str(e)}")

if __name__ == "__main__":
    try:
        arg = sys.argv[1]
        # Kiểm tra nếu arg là một list phân tách bằng dấu phẩy
        if ',' in arg:
            comment_ids = arg.split(',')
            comment_ids = [comment_id.strip() for comment_id in comment_ids]  # Loại bỏ khoảng trắng thừa
            reject_comments(comment_ids)
        else:
            reject_comment(arg)
        print("Successfully processed comment(s)")
    except Exception as e:
        print("Failed to process comment(s). Error: " + str(e))