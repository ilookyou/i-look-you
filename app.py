from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(
    'ITv1mfZvLANskQOSY7y9ZQTD45IppPLQiLMi7wu2ngea05Hv3RgPya74s165LXE+UOfnfFRnhPIZfay5QXOh7e4IWJK7wqO+0/B8SUfL+2OI8HT7MrbpLbfYBe9m64NMQFh+BL9dUnYDl5zbmnqRIwDnyilt8=')
handler = WebhookHandler('434126c11cd8861ccc01da4fdcb978b6')

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_text = event.message.text
    if line_text == 'test':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='伺服器連線正常'))









if __name__ == "__main__":
    app.run()