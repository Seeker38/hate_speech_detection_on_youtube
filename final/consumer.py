from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Kết nối tới MongoDB
client = MongoClient('localhost', 27017)
db = client['youtube_comment']  # Thay 'mydatabase' bằng tên database của bạn
collection = db['youtube_comment']  # Thay 'comments' bằng tên collection của bạn

# Tạo KafkaConsumer
consumer = KafkaConsumer('rawData', bootstrap_servers=['localhost:9092'], api_version=(0, 10))

try:
    for message in consumer:
        # Giải mã thông điệp và chuyển sang dạng JSON
        message_text = message.value.decode('utf-8')
        message_json = json.loads(message_text)
        
        # Lưu thông điệp vào MongoDB
        collection.insert_one(message_json)
        
        # In thông báo khi lưu thành công
        print("Message saved to MongoDB:", message_json)
except KeyboardInterrupt:
    print("Process interrupted and messages saved.")
except Exception as e:
    print(f"An error occurred: {e}")
