import os
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import subprocess
import requests
from googleapiclient.discovery import build
import re
import requests
from pymongo import MongoClient
import json
import sys
import codecs


app = Flask(__name__)

# Hàm thêm tiêu đề CORS vào phản hồi
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Cấp quyền truy cập từ mọi nguồn
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE'  # Bao gồm cả DELETE
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Cho phép tiêu đề Content-Type
    return response 

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['youtube_comment']
collection = db['youtube_comment']

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Lấy tất cả các tài liệu từ MongoDB và bỏ qua trường '_id'
        documents = collection.find({}, {'_id': 0})
        
        # Đường dẫn tới file.txt để ghi dữ liệu
        file_path = "D:/final/comments.txt"
        
        # Sử dụng một set để theo dõi các dữ liệu đã xuất hiện
        seen_data = set()
        
        # Mở file.txt trong chế độ ghi với codec 'utf-8'
        with open(file_path, 'w', encoding='utf-8') as file:
            for document in documents:
                # Thay đổi dấu ' thành dấu " trên mỗi document
                modified_document = {k: v.replace("'", '"') if isinstance(v, str) else v for k, v in document.items()}
                json_str = json.dumps(modified_document, ensure_ascii=False)  # Chuyển đổi thành chuỗi JSON, không đảm bảo ASCII
                
                # Kiểm tra nếu dữ liệu đã xuất hiện trước đó
                if json_str not in seen_data:
                    # Ghi dữ liệu vào file.txt
                    file.write(json_str + '\n')
                    # Đánh dấu dữ liệu đã xuất hiện
                    seen_data.add(json_str)

        return jsonify({'success': True, 'message': 'Data written to file.txt successfully'})
    except Exception as e:
        print('Error retrieving data:', e)
        return jsonify({'error': 'Internal Server Error'}), 500



@app.route('/api/deleteComment/<comment_id>', methods=['DELETE'])
def delete_comment_by_id(comment_id):
    # video_url = request.json.get('videoUrl')
    script_path = "D:/final/reject_comment.py"
    
    process = subprocess.Popen(["python", script_path, comment_id], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        return jsonify({'success': False, 'error': error.decode('utf-8')}), 500
    else:
        return jsonify({'success': True, 'message': output.decode('utf-8')})


    
@app.route('/api/deleteCommentAuthor/<author>', methods=['DELETE'])
def delete_comment_by_author(author):
    script_path = "D:/final/reject_user.py"  # Đường dẫn tới file reject_user.py
    
    process = subprocess.Popen(["python", script_path, author], stdout=subprocess.PIPE)

    output, error = process.communicate()
    
    if error:
        return jsonify({'success': False, 'error': error.decode('utf-8')}), 500
    else:
        return jsonify({'success': True, 'message': output.decode('utf-8')})

@app.route('/api/deleteCommentsAll', methods=['DELETE'])
def delete_all_comments():
    script_path = "D:/final/reject_all.py"  # Đường dẫn tới file reject_all.py

    # Đảm bảo rằng stdout sử dụng mã hóa UTF-8
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    
    try:
        process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            return jsonify({'success': False, 'error': error.decode('utf-8')}), 500
        else:
            return jsonify({'success': True, 'message': output.decode('utf-8')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/processUrl', methods=['POST'])  # Thay đổi đường dẫn endpoint
def process_url():
    try:
        url = request.json.get('url')  # Lấy đường link từ request JSON
        current_dir = os.getcwd()  # Lưu thư mục làm việc hiện tại
        os.chdir("D:/visomecens")  # Thay đổi thư mục làm việc hiện tại đến D:\visomecens
        script_path = "./HateSpeechDetectionApp/producer.py"
        print("Đường dẫn thực thi script:", os.path.abspath(script_path))
        process = subprocess.Popen(["python", script_path, url], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return jsonify({'success': False, 'message': 'Error running producer.py'}), 500
        else:
            return jsonify({'success': True, 'message': output.decode('utf-8')})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        os.chdir(current_dir)  # Quay lại thư mục làm việc ban đầu
        
@app.route('/api/runOtherRequest', methods=['GET'])
def run_other_request():
    # Thực hiện yêu cầu khác tại đây
    subprocess.Popen(["python", "D:/visomecens/HateSpeechDetectionApp/delete.py"])
    return jsonify({'success': True}), 200


from googleapiclient.discovery import build


# Hàm để lấy video ID từ URL của YouTube
def get_video_id(url):
    video_id = None
    # Các mẫu URL của YouTube khác nhau
    patterns = [
        r"(?<=v=)[\w-]+",
        r"(?<=be/)[\w-]+",
        r"(?<=v/)[\w-]+",
        r"(?<=embed/)[\w-]+"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(0)
            break
    return video_id

def get_comment_count(video_id, api_key):
    # Khởi tạo service của YouTube API với API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Sử dụng API để lấy thông tin của video
    video_response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    # Lấy số lượng bình luận từ phản hồi của API
    comment_count = int(video_response['items'][0]['statistics']['commentCount'])

    return comment_count

def get_video_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def extract_info_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trích xuất tiêu đề
        title_element = soup.find('meta', itemprop='name')
        title = title_element['content'].strip() if title_element else None
        
        # Trích xuất người đăng
        uploader_element = soup.find('link', itemprop='name')
        uploader = uploader_element['content'].strip() if uploader_element else None

        # Trích xuất ảnh thumbnail
        thumbnail_element = soup.find('meta', property='og:image')
        thumbnail_url = thumbnail_element['content'] if thumbnail_element else None

        # Trích xuất ID video
        video_id = get_video_id(url)
        
        # Lấy URL video
        video_url = get_video_url(video_id)
        
        return {
            'uploader': uploader,
            'title': title,
            'thumbnail_url': thumbnail_url,
            'video_id': video_id,
            'video_url': video_url,  # Thêm URL video vào kết quả trả về
        }
    except Exception as e:
        print("Error extracting info:", e)
        return None


# Route để lấy thông tin từ URL của video YouTube
@app.route('/api/getInfo', methods=['POST'])
def get_info():
    url = request.json['url']
    video_info = extract_info_from_url(url)
    if video_info:
        # Lấy API key từ tài khoản của bạn
        api_key = 'AIzaSyC5NSxek-GRs6BkWcUGxW79RQO0h0_5qdc'
        # Lấy tổng số bình luận
        comment_count = get_comment_count(video_info['video_id'], api_key)
        video_info['comment_count'] = comment_count
        return jsonify(video_info)
    else:
        return jsonify({'error': 'Không thể lấy thông tin từ đường liên kết YouTube.'}), 400




# Áp dụng hàm thêm tiêu đề CORS vào mỗi phản hồi trước khi trả về
app.after_request(add_cors_headers)

if __name__ == '__main__':
    app.run(debug=True)