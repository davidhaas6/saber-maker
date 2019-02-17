#!/usr/bin/env python3

import flask

app = flask.Flask('saber-maker')

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
    app.run()
