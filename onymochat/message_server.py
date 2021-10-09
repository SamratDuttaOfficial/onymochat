from flask import Flask
import datetime
import urllib.parse

user_sep = '#USERNAME#'  # User separator.
msg_sep = '#MESSAGE#'  # Message separator.
line_sep = '#NEW_LINE#'  # Line separator.

talk = []
app = Flask('Onymochat Server')
# Flask automatically runs on port 5000


@app.route('/')    # App routing is used to map the specific URL with the associated function
def index():
    return line_sep.join(talk)


@app.route('/<username>/<message_text>')
def show_message(username, message_text):
    username = urllib.parse.unquote(username)
    message_text = urllib.parse.unquote(message_text)
    time = str(datetime.datetime.now())
    talk.append(msg_sep.join([user_sep.join([time, username]), message_text]))
    return line_sep.join(talk)


app.run()
