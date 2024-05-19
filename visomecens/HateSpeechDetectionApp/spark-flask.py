from flask import stream_with_context, Flask, render_template, request, redirect, url_for, Response

import json
import os
import time
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
import socket
import logging
import threading
import sys

comment_consumer = KafkaConsumer('cleanData', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
# statistic_consumer = KafkaConsumer('statistic', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
app = Flask(__name__)
url = "https://www.youtube.com/watch?v=AMr3rGd_FPY"
# url = sys.argv[1]
time_list = []


@app.route('/home')
def home():
    return render_template('firstPage.html', data=url)


@app.route('/table-data', methods=['GET', 'POST'])
def table_data():
    def get_stream_data1():
        try:
            for msg in comment_consumer:
                print('received')
                record = json.loads(msg.value.decode('utf-8'))
                if 'timestamp' in record:
                    record['timestamp'] = record['timestamp'][:19]
                print(record)
                yield f"data:{json.dumps(record)}\n\n"
        except KeyboardInterrupt:
            print('Stop streaming data')

    return Response(get_stream_data1(), mimetype="text/event-stream")


# @app.route('/statistic-data', methods=['GET', 'POST'])
# def statistic_data():
#     def get_stream_data2():
#         try:
#             for msg in statistic_consumer:
#                 print('received')
#                 record = json.loads(msg.value.decode('utf-8'))
#                 print(record)
#                 yield f"data:{json.dumps(record)}\n\n"
#         except KeyboardInterrupt:
#             print('Stop streaming data')
#
#     return Response(get_stream_data2(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
