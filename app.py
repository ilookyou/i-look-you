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
    '7pLD26+Bmw1psdh4pMk29ZE2C0k0PNokrTFV4rH5NGxRFxDpRZmoSiztwB4zHQblUOfnfFRnhPIZfay5QXOh7e4IWJK7wqO+0/B8SUfL+2PcGe8SaYxq+jYT/VhY2Uec8g3MTwJajQe5Cw/62tbr0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d881df8fed2ae70edd4e020d45f20bb5')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_text = event.message.text
    if line_text =='test':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='伺服器連線正常'))



if __name__ == "__main__":
    app.run()
