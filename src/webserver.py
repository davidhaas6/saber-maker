#!/usr/bin/env python3

import flask
from google.cloud import storage as gcs
import psycopg2
import os
import sys

def connect_to_postgres():
    pgpasswd = os.environ['POSTGRES_USER_PASSWORD']
    pghost = os.environ['POSTGRES_HOST']
    conn_str = "user='postgres' dbname='sm' host='{}' password='{}'".format(pghost, pgpasswd)
    return psycopg2.connect(conn_str)

app = flask.Flask('saber-maker')

# address and port configuration
port = 8080
address = '127.0.0.1'
if len(sys.argv) > 1:
    port = int(sys.argv[1])
if len(sys.argv) > 2:
    address = sys.argv[2]

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in flask.request.files:
        return 'No file part', 400
    file = flask.request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    file_raw = file.read()

    try:
        db = connect_to_postgres()
        db.execute('INSERT INTO sm.uploads VALUES (DEFAULT) RETURNING sm.uploads.id')
        rows = db.fetchall()
        print(rows)
    except:
        return 'Unknown internal server error', 505

    # gcs_client = gcs.Client()
    # bucket = gcs_client.get_bucket('saber-maker')
    return 'Hello, World!'

@app.route('/<path:filename>')
def static_pages(filename):
    return flask.send_from_directory('www', filename)

@app.route('/')
def static_index():
    return flask.send_file('www/index.html')

if __name__ == "__main__":
    app.run(host=address, port=port)
