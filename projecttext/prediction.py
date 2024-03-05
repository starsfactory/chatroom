'''
自己的算法1
'''

# # Import the necessary modules
# import pickle
# import numpy as np
# from keras.models import load_model
# from keras.preprocessing.sequence import pad_sequences
#
#
# def predict(sentence):
#     # 导入字典
#     with open('projecttext\\pickledata\\word_dict2.pk', 'rb') as f:
#         word_dictionary = pickle.load(f)
#     with open('projecttext\\pickledata\\label_dict2.pk', 'rb') as f:
#         output_dictionary = pickle.load(f)
#     try:
#         # 数据预处理
#         input_shape = 180
#         x = [[word_dictionary[word] for word in sentence]]
#         x = pad_sequences(maxlen=input_shape, sequences=x, padding='post', value=0)
#         # 载入模型
#         model_save_path = 'projecttext\\model\\model2.keras'
#         lstm_model = load_model(model_save_path)
#
#         # 模型预测
#         y_predict = lstm_model.predict(x)
#         label_dict = {v: k for k, v in output_dictionary.items()}
#         print('情感预测结果: %s' % label_dict[np.argmax(y_predict)])
#         return label_dict[np.argmax(y_predict)]
#     except KeyError as err:
#         print("您输入的句子有汉字不在词汇表中，请重新输入！")
#         print("不在词汇表中的单词为：%s." % err)


'''
百度api
'''

# 获取assesskey
# import requests
# import json
#
#
# def main():
#     url = "https://aip.baidubce.com/oauth/2.0/token?client_id=uKojToc6aIpbRUUhv5RIkvty&client_secret=wQLFC6H7LM1RYIl7pYkIjM7gc9rnmSWU&grant_type=client_credentials"
#
#     payload = json.dumps("你好")
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
#
#     proxies = {
#         "http": "http://127.0.0.1:1080",
#         "https": "http://127.0.0.1:1080"
#     }
#     print('posting')
#     response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
#     print('post finish')
#
#     access_token = response.text
#     print(access_token)
#
#
# if __name__ == '__main__':
#     main()
import requests
import json

API_KEY2 = "q0vYdp7I0fxaxcoYsDKRWlqt"
SECRET_KEY2 = "8bUHU13zoyyJK1ByEy5zGHOkna56DmwK"


API_KEY = "uKojToc6aIpbRUUhv5RIkvty"
SECRET_KEY = "wQLFC6H7LM1RYIl7pYkIjM7gc9rnmSWU"
access_token = '24.d55d328276ee3c20a638eecd1d1afd6e.2592000.1711802051.282335-54222820'

def predict(sentence):
    emotion = ''
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/emotion?charset=UTF-8&access_token=" + access_token

    payload = json.dumps({
        "text": sentence
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080"
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

    content = json.loads(response.text)
    items = content.get('items', [])
    # 选择概率最高的情绪标签
    top_item = max(items, key=lambda x: x.get('prob', 0))
    emotion = top_item.get('label', '未知')
    # 提取情绪标签
    emotion_label = top_item["label"]
    # 如果有subitem，取出其中的label
    subitem_label = top_item["subitems"][0]["label"] if top_item["subitems"] else "no obvious emotion"

    print('emotion', emotion)
    return str(emotion), str(subitem_label)


def predicate2(sentence):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + get_access_token()

    payload = json.dumps({
        "text": sentence
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080"
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)

    print(response.text)

    data = json.loads(response.text)

    # 获取积极和消极的概率值
    positive_prob = data["items"][0]["positive_prob"]
    negative_prob = data["items"][0]["negative_prob"]

    # 设置概率阈值，根据阈值判断积极或消极
    threshold = 0.4  # 设置阈值，可以根据实际情况调整

    if positive_prob >= threshold:
        emotion_label = "积极"
    else:
        emotion_label = "消极"

    # 输出结果
    print("情感类别:", emotion_label)

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY2, "client_secret": SECRET_KEY2}
    return str(requests.post(url, params=params).json().get("access_token"))