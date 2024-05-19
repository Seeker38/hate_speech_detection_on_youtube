import pprint
import sys
from pathlib import Path
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import pandas as pd
import numpy as np
from kafka import KafkaProducer
import logging
import socket
import json
import time
import os
import tensorflow as tf
import pickle
from preprocessing import preprocessing
from transformers import AutoTokenizer
import torch
import torch.nn as nn
import torch.nn.functional as F
import warnings

warnings.filterwarnings('ignore')

# Build service for calling the Youtube API:
## Arguments that need to passed to the build function
# DEVELOPER_KEY = "AIzaSyDbt-xdAOjDhJghQGVMxfbsSiSyCFJr1Jw"
DEVELOPER_KEY = "AIzaSyC5NSxek-GRs6BkWcUGxW79RQO0h0_5qdc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

## creating Youtube Resource Object
youtube_service = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)


class CNN(nn.Module):
    def __init__(self, embedding_dim, n_filters, filter_sizes, output_dim,
                 dropout, pad_idx):
        super().__init__()

        self.fc_input = nn.Linear(embedding_dim, embedding_dim)

        self.conv_0 = nn.Conv1d(in_channels=embedding_dim,
                                out_channels=n_filters,
                                kernel_size=filter_sizes[0])

        self.conv_1 = nn.Conv1d(in_channels=embedding_dim,
                                out_channels=n_filters,
                                kernel_size=filter_sizes[1])

        self.conv_2 = nn.Conv1d(in_channels=embedding_dim,
                                out_channels=n_filters,
                                kernel_size=filter_sizes[2])

        self.conv_3 = nn.Conv1d(in_channels=embedding_dim,
                                out_channels=n_filters,
                                kernel_size=filter_sizes[3])

        self.fc = nn.Linear(len(filter_sizes) * n_filters, output_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, encoded):
        embedded = self.fc_input(encoded)

        max_kernel_size = max(self.conv_0.kernel_size[0],
                              self.conv_1.kernel_size[0],
                              self.conv_2.kernel_size[0],
                              self.conv_3.kernel_size[0])

        padding = max_kernel_size - 1  # Adjust the padding based on your requirements
        embedded = F.pad(embedded, (0, 0, padding, 0))

        embedded = embedded.permute(0, 2, 1)

        conved_0 = F.relu(self.conv_0(embedded))
        conved_1 = F.relu(self.conv_1(embedded))
        conved_2 = F.relu(self.conv_2(embedded))
        conved_3 = F.relu(self.conv_3(embedded))

        pooled_0 = F.max_pool1d(conved_0, conved_0.shape[2]).squeeze(2)
        pooled_1 = F.max_pool1d(conved_1, conved_1.shape[2]).squeeze(2)
        pooled_2 = F.max_pool1d(conved_2, conved_2.shape[2]).squeeze(2)
        pooled_3 = F.max_pool1d(conved_3, conved_3.shape[2]).squeeze(2)

        cat = self.dropout(torch.cat((pooled_0, pooled_1, pooled_2, pooled_3), dim=1))

        result = self.fc(cat)

        return result


# Create a producer
def create_producer():
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
    except Exception as e:
        print("Couldn't create the producer")
        producer = None
    return producer


### Function to get youtube video id.
# source:
# https://stackoverflow.com/questions/45579306/get-youtube-video-url-or-youtube-video-id-from-a-string-using-regex
def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]


device = torch.device('cpu')

phoBert = torch.load("D:\\visomecens\\Models\\phobert_cnn_model_part1_task2a_2.pt",
                     map_location=device
                     )
cnn = torch.load('D:\\visomecens\\Models\\phobert_cnn_model_part2_task2a_2.pt',
                 map_location=device
                 )


def predict_label(text):
    phoBertTokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')
    # processing the text input    
    processed_sentence = preprocessing(text)

    # # Tokenize the sentence using PhoBERT tokenizer
    phobert_inputs = phoBertTokenizer(processed_sentence, return_tensors="pt")

    embedded = phoBert(phobert_inputs['input_ids'], phobert_inputs['attention_mask'])[0]
    predictions = cnn(embedded)
    predictions = predictions.detach().cpu().numpy()
    predictions = np.argmax(predictions, axis=1).flatten()

    return int(predictions[0])


# List to store IDs of comments that have been sent
sent_comments = []
sent_replies = []

video_link = sys.argv[1]

producer = create_producer()


def get_new_comments(video_id):
    response = youtube_service.commentThreads().list(
        part='snippet, replies',
        maxResults=9999,
        textFormat='plainText',
        order='time',
        videoId=video_id
    ).execute()

    results = response.get('items', [])
    return results


# Function to get replies for a specific comment
if __name__ == "__main__":
    while True:
        try:
            results = get_new_comments(get_id(video_link))
            for item in results:
                comment_id = item['id']
                # Check if comment ID has already been sent
                if comment_id not in sent_comments:
                    author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    datetime = item['snippet']['topLevelComment']['snippet']['updatedAt']

                    
                    # Assume you have your DNN prediction logic here
                    pred = predict_label(comment)

                    record = {"comment_id": comment_id, "author": author, "datetime": datetime, "raw_comment": comment,
                              "clean_comment": preprocessing(comment),
                              "label": pred
                              }

                    record = json.dumps(record, ensure_ascii=False).encode("utf-8")
                    producer.send(topic='rawData', value=record)

                    # Add comment ID to list of sent comments
                    sent_comments.append(comment_id)

                if item['snippet']['totalReplyCount'] > 0:
                    for reply in item['replies']['comments']:
                        reply_id = reply['id']

                        # Check if reply ID has already been sent
                        if reply_id not in sent_replies:
                            reply_comment = reply['snippet']['textDisplay']
                            reply_author = reply['snippet']['authorDisplayName']
                            reply_datetime = reply['snippet']['publishedAt']

                            record = {"comment_id": reply_id,
                                      "author": reply_author,
                                      "datetime": reply_datetime,
                                      "raw_comment": reply_comment,
                                      "clean_comment": preprocessing(reply_comment),
                                      "label": predict_label(reply_comment)
                                      }
                            # print(reply_comment)
                            record = json.dumps(record, ensure_ascii=False).encode("utf-8")
                            producer.send(topic='rawData', value=record)

                            # Add reply ID to list of sent replies
                            sent_replies.append(reply_id)

            # Sleep for a while before fetching comments again
            time.sleep(3)

        except KeyboardInterrupt:
            print('Stop flush!')
            break  # Exit the loop if KeyboardInterrupt is detected
