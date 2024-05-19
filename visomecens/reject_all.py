from reject_comment import reject_comments
import json


with open('D:\\final\\comments.txt', 'r', encoding='utf-8') as file:
    comments = file.readlines()
    
l = []

for comment in comments:
    comment_data = json.loads(comment)
    if comment_data.get('label') == 1 or comment_data.get('label') == 2:
        l.append(comment_data.get('comment_id'))

reject_comments(l)