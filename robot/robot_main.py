import requests
import json

API_KEY = "trWXQkgHz809pKRqlSGLmLqR"
SECRET_KEY = "tYXreuuUKEEfHlbM3ZpidKmsM717r39B"


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080"
    }
    return str(requests.post(url, params=params, proxies=proxies).json().get("access_token"))

def robotdetect(message):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-4k-0205?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你是一个协助机器人，需要注意多人对话中人们的对话是否偏移主题，（对话会给出内容和说话人"
            },
            {
                "role": "user",
                "content": "对话主题为，识别接下来的对话，\n" + str(message)
            },
        ],
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080"
    }

    print('here')
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

    print(response.text)
    print(json.loads(response.text)['result'])




def topicdetect(chatmessage):
  inputmessage = []
  for i in chatmessage:
    inputmessage.append(json.loads(i))
  robotmessage = robotdetect(inputmessage)
  # robotmessage = '你好'
  return robotmessage
