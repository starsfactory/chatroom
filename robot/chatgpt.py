import openai
import json
from openai import OpenAI

# openai.api_key = "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"
# openai.api_base = "https://api.chatanywhere.com.cn/v1"


# 自己的key
openai.api_key = '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'

print('hello one')

# completion = openai.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
#   ],
# )
#
# print(completion.choices[0].message.content)

print('hello two')



def robotchat(message):
  # completion = openai.chat.completions.create(
  #   model="gpt-3.5-turbo",
  #   messages=[
  #     {"role": "system", "content": "You are a helpful assistant."},
  #     {"role": "user", "content": "Hello!"}
  #   ],
  # )
  # print(completion.choices[0])
  completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system",
       "content": "你是一个协助机器人，需要注意多人对话中人们的情绪，并给予人们鼓励，（对话会给出内容和说话人"},
      {"role": "user",
       "content": "对接下来的对话中情绪低落的人给予鼓励,最好根据对话中的具体内容给予鼓励,限制30字\n" + str(message)}
    ],
  )
  robotmessage = completion.choices[0].message.content
  return robotmessage

def robotchat_contact(chatmessage):
  inputmessage = []
  for i in chatmessage:
    inputmessage.append(json.loads(i))

  robotmessage = robotchat(inputmessage)
  # robotmessage = '你好'
  return robotmessage




