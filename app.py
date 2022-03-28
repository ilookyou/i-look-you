from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'LNL8BtWTgFQFdTbjinnPm5TWMENZ9Y8Am7xcF+3/5ym6h1m2fHPSwTWNsekU7SsWUOfnfFRnhPIZfay5QXOh7e4IWJK7wqO+0/B8SUfL+2MXa4Qr/b+BQgNhdpbD1l9tSISvJbFZpnyilFU89OP3eQbQdBD1l9tSISvJbFZpnyilFU89OP3eQbQdBD')
handler = WebhookHandler('768215b4dc56992685d477e22b2c5d3a')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
