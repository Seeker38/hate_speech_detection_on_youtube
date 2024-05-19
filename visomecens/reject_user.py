from reject_comment import delete_record, service, delete_record_mongo
import json
import sys


def get_author_of_comment(comment_id):
    # Gửi yêu cầu để lấy thông tin của comment
    comment_info = service.comments().list(
        part='snippet',
        id=comment_id
    ).execute()

    # Trích xuất thông tin của tác giả từ kết quả
    author = comment_info['items'][0]['snippet']['authorDisplayName']

    return author


def reject_and_ban(comment_id):
    # Cập nhật trạng thái kiểm duyệt của bình luận thành 'published'
    service.comments().setModerationStatus(
        id=comment_id,
        moderationStatus='rejected',
        banAuthor=True
    ).execute()
    delete_record(comment_id)
    delete_record_mongo('youtube_comment','youtube_comment', comment_id )
    print("successfully rejected and banned user")

author = sys.argv[1]

hate_offen = []

with open('D:\\final\\comments.txt', 'r', encoding='utf-8') as file:
    comments = file.readlines()

for comment in comments:
    comment_data = json.loads(comment)
    if comment_data.get('author') == author:
        reject_and_ban(comment_data.get('comment_id'))
