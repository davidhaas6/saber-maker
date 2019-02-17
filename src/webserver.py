#!/usr/bin/env python3

import flask
import sys

app = flask.Flask('saber-maker')

# address and port configuration
port = 8080
address = '127.0.0.1'
if len(sys.argv) > 1:
    port = int(sys.argv[1])
if len(sys.argv) > 2:
    address = sys.argv[2]

@app.route('/upload')
def upload():
    return 'Hello, World!'

@app.route('/<path:filename>')
def static_pages(filename):
    return flask.send_from_directory('www', filename)

@app.route('/')
def static_index():
    return flask.send_file('www/index.html')

if __name__ == "__main__":
    app.run(host=address, port=port)
