from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models imoprt (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
SECRET = os.environ["SECRET"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route('/', methods=['GET'])
def index():
    return 'Hello World'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.haeders['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("RequestBody: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
if __name__ == '__main__':
    app.run()
