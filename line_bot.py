from flask import Flask, request, abort
import google.generativeai as genai
import requests

app = Flask(__name__)

# 設定您的 LINE Channel Token 和 Channel Secret
LINE_CHANNEL_TOKEN = 'YOUR_CHANNEL_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

# 設定您的 Gemini API 金鑰
genai.configure(api_key="YOUR_API_KEY")

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_json()
    for event in body['events']:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_message = event['message']['text']
            reply_token = event['replyToken']

            # 與 Gemini API 通訊
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(user_message)
            gemini_reply = response.text

            # 發送 LINE 回應
            reply_message(reply_token, gemini_reply)

    return 'OK'

def reply_message(reply_token, message):
    headers = {
        'Authorization': f'Bearer {LINE_CHANNEL_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': message}]
    }
    requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=data)

if __name__ == '__main__':
    app.run(port=8080)
