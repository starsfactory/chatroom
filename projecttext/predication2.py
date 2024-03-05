import paddlehub as hub

# 加载模型
senta = hub.Module(name="senta_lstm")
# 待分类文本
text = []

# 情感分类
# results = senta.sentiment_classify(data={"text": test_text})

# 得到结果
# for result in results:
#     print(result)


def predict(sentence):
        text.append(sentence)
        result = senta.sentiment_classify(data={"text": text})
        print(result[0])
        return result[0]['sentiment_label']
