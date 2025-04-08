import requests

def send_line_notify(message):
    line_notify_token = 'Vi5AuZ8qjgAW6OneoHgQIwYkC8uzm2C668keCRdPjj4WawOVyS47EIcD2h3gmA4R6lK8nDaMO/Vw0dbdg/aWFc/LxMvO9jEMRpb0p0zOGMk+c+7aRiShJvzD/G0CnrNRayQYrIWRI7M8rsPufJMRYAdB04t89/1O/w1cDnyilFU='  # LINE Messaging APIのChannel Access Token
    user_id = 'Cf1de4fae3662c84d0bd91c3d9111c4be'  # ユーザーIDを設定
    headers = {
        'Authorization': f'Bearer {line_notify_token}',  # アクセストークンを挿入
        'Content-Type': 'application/json'
    }
    payload = {
        'to': user_id,  # 通知を送るユーザーのID
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=payload)
    
    if response.status_code == 200:
        print("通知が送信されました。")
    else:
        print(f"エラー: {response.status_code} - {response.text}")

# メッセージ送信
send_line_notify("こんにちは！")
