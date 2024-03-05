import json
import os.path
import re
from datetime import datetime
import asyncio

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from chat.models import Chathistory
from projecttext.prediction import predict
from asgiref.sync import async_to_sync
# from predication2 import predict
from robot.chatgpt import robotchat_contact

# 加载模型

# 待分类文本
text = []
# GROUP_LIST = []
emotion_list = ['like', 'happy', 'angry', 'disgusting', 'fearful', 'sad', 'no emotion']
time = datetime.now()
empty = True
pattern = r'##(.*?)##'
folder_path = ''
robot_run = False

class ChatRoom(WebsocketConsumer):
    def websocket_connect(self, message):
        print('enter room')
        group = self.scope['url_route']['kwargs'].get('group')
        global folder_path
        global empty
        if empty:
            time = datetime.now()
            folder_path = os.getcwd() + '\\data\\' + str(group)
            if not os.path.exists(folder_path):
                # 如果不存在，创建文件夹
                os.makedirs(folder_path)
            empty = False
        self.accept()

        # GROUP_LIST.append(self)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        msg = json.loads(message['text'])
        print('receive message', msg)
        match_object = re.fullmatch(pattern, msg['message'], re.DOTALL)
        group = self.scope['url_route']['kwargs'].get('group')
        print(match_object)

        async_to_sync(self.channel_layer.group_send)(group, {'type': 'sendtoall',
                                                             'message': msg['message'],
                                                             'username': msg['username'],
                                                             'message_type': 'human',
                                                             'emotion': 'NULL'})
        if match_object:
            matched_content = match_object.group(1)
            print("order", matched_content)
            sysback = self.sysfunc(matched_content, group)
            async_to_sync(self.channel_layer.group_send)(group, {'type': 'sendtoall',
                                                                  'message': sysback,
                                                                  'username': 'sys',
                                                                  'message_type': 'human',
                                                                  'emotion': 'NULL'})
        else:
            addmessage, addemotion = predict(msg['message'])
            async_to_sync(self.channel_layer.group_send)(group, {'type': 'sendtoall',
                                                                  'message': msg['message'],
                                                                  'username': msg['username'],
                                                                  'message_type': 'emotion',
                                                                  'emotion': addmessage})

            robotmessage = self.robot_message_process(msg, addmessage, group, addemotion)
            global robot_run
            if robotmessage != "NULL" and robot_run:
                async_to_sync(self.channel_layer.group_send)(group, {'type': 'sendtoall',
                                                                      'message': robotmessage,
                                                                      'username': msg['username'],
                                                                      'message_type': 'robot',
                                                                      'emotion': 'NULL'})

        # msg = msg + predict(msg)
        # for sys in GROUP_LIST:
        #     sys.send(msg)

    def sendtoall(self, event):
        text = json.dumps({'message': event['message'],
                           'username': event['username'],
                           'message_type': event['message_type'],
                           'emotion': event['emotion']})
        self.send(text)





    def websocket_disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)('room', self.channel_name)
        raise StopConsumer()


    def robot_message_process(self, event, addmessage, group, addemotion):
        lines = []
        if not os.path.exists(folder_path +'\\'+ str(time).replace(':', '_') +'.json'):
            with open(folder_path +'\\'+ str(time).replace(':', '_') +'.json', 'w') as file:
                file.writelines('')

        with open(folder_path +'\\'+ str(time).replace(':', '_') +'.json', 'r+') as file:
            lines = file.readlines()

        with open(folder_path +'\\'+ str(time).replace(':', '_') +'.json', 'w') as file:
            # 检查文件是否为空
            # lines = file.readlines()

            if len(lines) == 0:

                lines.append(json.dumps({'message': event['message'],
                                         'username': event['username'],
                                         'emotion': addmessage,
                                         'subemotion': addemotion,
                                         'time': str(datetime.now())}) + '\n')
                emotiondata = {'negativecount': 0, 'sumnegative':0}
                if addmessage == 'pessimistic':
                    emotiondata['negativecount'] = emotiondata['negativecount'] + 1
                    emotiondata['sumnegative'] = emotiondata['sumnegative'] + 1
                lines.append(json.dumps(emotiondata))
                file.writelines(lines)
                return 'NULL'
            else:
                robotmessage = 'NULL'
                emotiondata = json.loads(lines[-1])
                lines.pop()
                lines.append(json.dumps({'message': event['message'],
                                         'username': event['username'],
                                         'emotion': addmessage,
                                         'subemotion': addemotion,
                                         'time': str(datetime.now()),}) + '\n')

                if addmessage == 'pessimistic':
                    emotiondata['negativecount'] = emotiondata['negativecount'] + 1
                    emotiondata['sumnegative'] = emotiondata['sumnegative'] + 1
                else:
                    emotiondata['negativecount'] = 0
                # 机器人干涉
                if emotiondata['negativecount'] > 3:
                    robotmessage = robotchat_contact(lines)
                    emotiondata['negativecount'] = emotiondata['negativecount'] - 3

                lines.append(json.dumps(emotiondata))
                file.writelines(lines)
                return robotmessage

    def sysfunc(self, order, roomid):
        global robot_run
        if order == 'save':
            history = Chathistory()
            history.chatroomid = roomid
            history.history = str(time).replace(':', '_') +'.json'
            history.save()
            return '消息记录已保存'
        if order == 'roboton':
            robot_run = True
            return '机器人已启动'
        if order == 'robotoff':
            robot_run = False
            return '机器人已关闭'
        return '未知指令'
    # def predict(sentence):
    #     text.append(sentence)
    #     result = senta.sentiment_classify(data={"text": text})
    #     print(result[0])
    #     return result[0]['sentiment_label']