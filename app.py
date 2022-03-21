# app.py
import random
from datetime import datetime, timezone, timedelta

import pinyin
import psycopg2
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
    '7pLD26+Bmw1psdh4pMk29ZE2C0k0PNokrTFV4rH5NGxRFxDpRZmoSiztwB4zHQblUOfnfFRnhPIZfay5QXOh7e4IWJK7wqO+0/B8SUfL+2PcGe8SaYxq+jYT/VhY2Uec8g3MTwJajQe5Cw/1O/tbr0dBdBid048Cw/62tbr0dBad')
handler = WebhookHandler('d881df8fed2ae70edd4e020d45f20bb5')


# -----------------------------------------------------------------------------------------------
# 檢查名字字數
def check_name(name):
    if len(name) > 30:
        return True
    else:
        return False


# -----------------------------------------------------------------------------------------------
# 課表
wek_curriculum = [['英文閱寫', '體育', '跑班選修', '跑班選修', '午休', '選修物理五', '閱讀與研究', '遠征式課程', '放學啦'],
                  ['閱讀與研究', '數學甲', '選修化學四', '選修化學四', '午休', '生命教育', '英文聽講', '文學選讀', '放學啦'],
                  ['英文聽講', '彈性學習', '彈性學習', '彈性學習', '午休', '美術', '美術', '選修物理五', '放學啦'],
                  ['跑班選修', '跑班選修', '英文閱寫', '數學甲', '午休', '遠征式課程', '遠征式課程', '體育', '放學啦'],
                  ['選化五', '數學甲', '團體活動', '團體活動', '午休', '文學選讀', '數學甲', '選物三-1', '放學啦']]


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


# -----------------------------------------------------------------------------------------------
conn = psycopg2.connect(database="d58bk1bhneu5t2",
                        user="inzyymgreqkfoh",
                        password="ae71e368bf350b8b9373aa0ab669ba07fa74e07444d74fcd824f72342180ea21",
                        host="ec2-54-235-45-88.compute-1.amazonaws.com",
                        port="5432")


# -----------------------------------------------------------------------------------------------

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global wek_curriculum
    line_text = event.message.text

    if line_text == "骰子":
        r = random.randint(1, 6)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'擲出 {r} 點'))

    if line_text == "猜拳":
        mora_list = ['剪刀', '石頭', '布']
        mora = str(random.choice(mora_list))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mora))

    if line_text == "不要問給我來一本正經的漫畫":
        sex_book = 'https://nhentai.net/g/' + str(random.randint(111111, 369999))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=sex_book))

    if '我出' in line_text:
        global mora_txt
        mora_list = ['剪刀', '石頭', '布']
        a = random.choice(mora_list)
        if '剪刀' in line_text:
            mora_player = '剪刀'
            if a == '石頭':
                mora_end = '我贏了'
            elif a == '布':
                mora_end = '你贏了'
            else:
                mora_end = '沒輸沒贏'
            mora_txt = f'你出:{mora_player}\n我出:{a}\n\n結果:{mora_end}'

        elif '石頭' in line_text:
            mora_player = '石頭'
            if a == '剪刀':
                mora_end = '你贏了'
            elif a == '布':
                mora_end = '我贏了'
            else:
                mora_end = '沒輸沒贏'
            mora_txt = f'你出:{mora_player}\n我出:{a}\n\n結果:{mora_end}'

        elif '布' in line_text:
            mora_player = '布'
            if a == '石頭':
                mora_end = '你贏了'
            elif a == '剪刀':
                mora_end = '我贏了'
            else:
                mora_end = '沒輸沒贏'
            mora_txt = f'你出:{mora_player}\n我出:{a}\n\n結果:{mora_end}'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mora_txt))

    if '不要問選一個 ' in line_text:
        event.message.text = event.message.text.replace('不要問選一個 ', '')
        ran_ran = event.message.text.split('/')
        ran_ran = f'我選 {random.choice(ran_ran)}'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ran_ran))

    if ('星期' in line_text or '禮拜' in line_text) and '課表' in line_text:
        cur_text = [TextSendMessage(text=line_text)]
        txt = list(line_text)
        if len(txt) != 5:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入要查詢禮拜幾的課表'))
        elif txt[2] == '一':
            cur = '\n'.join(wek_curriculum[0])
            cur_text.append(TextSendMessage(text=cur))
            line_bot_api.reply_message(event.reply_token, cur_text)
        elif txt[2] == '二':
            cur = '\n'.join(wek_curriculum[1])
            cur_text.append(TextSendMessage(text=cur))
            line_bot_api.reply_message(event.reply_token, cur_text)
        elif txt[2] == '三':
            cur = '\n'.join(wek_curriculum[2])
            cur_text.append(TextSendMessage(text=cur))
            line_bot_api.reply_message(event.reply_token, cur_text)
        elif txt[2] == '四':
            cur = '\n'.join(wek_curriculum[3])
            cur_text.append(TextSendMessage(text=cur))
            line_bot_api.reply_message(event.reply_token, cur_text)
        elif txt[2] == '五':
            cur = '\n'.join(wek_curriculum[4])
            cur_text.append(TextSendMessage(text=cur))
            line_bot_api.reply_message(event.reply_token, cur_text)
        elif txt[2] == '六' or txt[2] == '日':
            cur_text = '放假啦'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cur_text))
        else:
            cur_text = f'沒有星期{txt[2:-2]}'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cur_text))

    if line_text == '下一節':
        utc_0 = datetime.utcnow().replace(tzinfo=timezone.utc)
        utc_8 = utc_0.astimezone(timezone(timedelta(hours=8)))  # 轉換時區到UTC+8
        wek = utc_8.weekday() + 1
        th = utc_8.hour
        tm = utc_8.minute
        if wek <= 5:
            if 6 <= th <= 17:
                if th == 6 or th == 7 or (th == 8 and tm <= 10):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][0]))
                elif th == 8 and tm >= 10:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][1]))
                elif th == 9:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][2]))
                elif th == 10:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][3]))
                elif th == 11:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][4]))
                elif th == 12:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][5]))
                elif th == 13 or (th == 14 and tm <= 10):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][6]))
                elif th == 14:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][7]))
                elif th == 15:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wek_curriculum[wek - 1][8]))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='放學啦'))

            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='放學啦'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='放假啦'))

    



# -----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()
