from flask import Flask, request, abort
import google.generativeai as genai
import requests

app = Flask(__name__)

# 設定您的 LINE Channel Token 和 Channel Secret
LINE_CHANNEL_TOKEN = '0NtOIZT6BCuu8HtgfNS8Ui8KuQ53kQtoD9fNrUHYNulJQhEGCYU5Mmv7qEQ39DQSfKn3SFTxOkjD0EJGHTCPpBuTsG1lgteeYQd1m45uCMBRmyeSmAqaIfJXtvzg8x41MlYyDdWmTY+5aQwsCrbV2QdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '44632ff3d25949555d3df578fe111183'

# 設定您的 Gemini API 金鑰
genai.configure(api_key="AIzaSyCadljClyECVRXh1gqsJXEgTAZivl1QwbY")

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
