# app.py
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# -----------------------------------------------------------------------------------------------
app = Flask(__name__)
# -----------------------------------------------------------------------------------------------
line_bot_api = LineBotApi(
    'qhWoEUF5o7M0gQ04kZsjZnLej8qfO+hqJb4fpku6dMC3aPmhh1SgJtFkHbJ0/UfofPK1Y6+IGQM/XV3avAy4TDEqHd+67TQBq/nYV4hSKJsMXO4ZEnSSc8DrW4fPcmapuB7/2cNsC9yzQEaHHIbvfgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('717cac038e9fa9691e017ffae2746e8c')


# -----------------------------------------------------------------------------------------------

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


a = '31150905'
b = '28564531'
c1 = '05754219'
c2 = '52891675'
c3 = '45327106'
c6 = '252'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_text = event.message.text

    if line_text == 'test':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='伺服器連線正常'))


if __name__ == "__main__":
    app.run()
