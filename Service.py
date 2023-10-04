import json

### Controllers ###
import Controllers

### LineBot ###
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

### Logger ###
import logging.config
logging.config.fileConfig('logging_config_line.ini')
logger = logging.getLogger('CsLogger')

### Flask ###
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

### 初始所有對話紀錄 (暫時使用程式內字典儲存) ###
conversation_history = {}

### Health Check ###
@app.route("/")
def index():
    """Server 是否正常的確認頁面.
    """
    return "server is ready"

### LineBot 對話 ###
@app.route("/linebot", methods=['POST', 'GET'])
def linebot():
    try:
        body = request.get_data(as_text=True)
        json_data = json.loads(body)
        line_bot_api = LineBotApi('你的 Channel access token')
        handler = WebhookHandler('你的 LINE Channel secret')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']

        user_id = json_data['events'][0]['source']['userId']
        if user_id not in conversation_history:
            conversation_history[user_id] = {
                'messages': [],
                'pending_deletion': False
            }

        # 檢查 conversation_history 的總字數是否超過 5000 (避免 Tokens 過多導致報錯)
        total_length = sum(len(msg) for msg in conversation_history[user_id]['messages'])
        while total_length > 5000 and len(conversation_history[user_id]['messages']) >= 4:
            logger.info("對話紀錄過長，刪除前4句")
            del conversation_history[user_id]['messages'][:4]
            total_length = sum(len(msg) for msg in conversation_history[user_id]['messages'])

        msg = json_data['events'][0]['message']['text']

        if conversation_history[user_id]['pending_deletion']:
            logger.info("重新規劃階段二")
            reply_msg = Controllers.handle_delete_response(msg, user_id, conversation_history)
        else:
            if msg == "重新規劃":
                logger.info("重新規劃階段一")
                conversation_history[user_id]['pending_deletion'] = True
                reply_msg = "是否確定要重新規劃課程？(Y/N)"
            else:
                logger.info("進入詢問 GPT 階段")
                conversation_history[user_id]['messages'].append(f"教師: {msg}")
                reply_msg = Controllers.chat(msg, conversation_history[user_id]['messages'])
                conversation_history[user_id]['messages'].append(f"課程規劃師: {reply_msg}")

        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk, text_message)

    except Exception as e:
        print(f"Error: {e}")
        logger.error("linebot 發生了一個例外情況", exc_info=True)
        return 'linebot error'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, threaded=True)
