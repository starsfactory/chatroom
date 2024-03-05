import json
import os
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from chat.models import Chatroom, Chathistory
from login.models import Roomlist


# Create your views here.

def go_room(request):
    print('welcome our room')
    return render(request, 'room.html')

def go_new_room(request):
    print('welcome our new room')
    return render(request, 'boot_chat.html')

def go_all_room(request):
    print('show all room')
    return render(request, 'allroom.html')

def go_history(request):
    print('show all room')
    return render(request, 'partvisualize.html')

def go_visualize(request):
    print('visualize page')
    return render(request, 'visualization.html')

def go_visualizeall(request):
    print('visualize all page')
    return render(request, 'visualization.html')

def get_all_room(request):
    print('getting all room')
    userid = request.session.get('userid')
    print(userid)
    # 加入的房间的列表
    alljoinroomid = list(Roomlist.objects.values_list('roomid', flat=True).filter(userid=userid))
    # 所有创建的房间
    allmainuserroom = Chatroom.objects.values().filter(mainuser=userid)
    allroom = list(allmainuserroom)
    if len(alljoinroomid) != 0:
        # 所有加入的房间
        alljoinroom = Chatroom.objects.values().filter(id__in=alljoinroomid)
        allroom = allroom + list(alljoinroom)

    if allroom:
        print(allroom)
        return JsonResponse({'allroom': allroom, 'empty': False})
    else:
        print('empty')
        return JsonResponse({'empty': True})

def get_all_history(request):
    print('getting all history')
    roomid = request.GET.get('roomid')
    print('roomid', roomid)
    allhistoryid = Chatroom.objects.values().filter(roomid=roomid)

def join_room(request):
    print('joinning room')
    roomid = request.GET.get('roomid')
    userid = request.GET.get('userid')
    room = Chatroom.objects.values().filter(id=roomid)
    if room:
        mainuser = room.first()['mainuser']
        alljoinroomid = list(Roomlist.objects.values_list('userid', flat=True).filter(roomid=roomid))
        print(mainuser, alljoinroomid)
        print(userid)
        if int(userid) == int(mainuser) or int(userid) in alljoinroomid:
            return JsonResponse({'success': True, 'joinmark': True})
        else:
            joinrecord = Roomlist()
            joinrecord.userid = userid
            joinrecord.roomid = roomid
            joinrecord.save()
            print('you join the room', roomid)
            return JsonResponse({'success': True, 'joinmark': False})
    else:
        return JsonResponse({'success': False})

def create_room(request):
    print('creating room')
    roomname = request.GET.get('roomname')
    userid = request.GET.get('userid')
    roomget = Chatroom.objects.values().filter(roomname=roomname, mainuser=userid)
    if roomget:
        return JsonResponse({'success': False})
    else:
        createroom = Chatroom()
        createroom.roomname = roomname
        createroom.mainuser = userid
        createroom.save()
        return JsonResponse({'success': True})

def get_history(request):
    userid = request.GET.get('userid')
    allroomidlist = list(Chatroom.objects.values_list('id', flat=True).filter(mainuser=userid))
    allroomidlist = allroomidlist + list(Roomlist.objects.values_list('roomid', flat=True).filter(userid=userid))
    history = list(Chathistory.objects.values().filter(chatroomid__in=allroomidlist))
    print(history)
    if history:
        return JsonResponse({'success': True, 'history': history})
    else:
        return JsonResponse({'success': False})


def visualize(request):
    roomid = request.GET.get('roomid')
    filename = request.GET.get('filename')
    filepath = os.getcwd() + '\\data\\' + str(roomid) +'\\'+ filename
    analysefilepath = os.getcwd() + '\\data\\' + str(roomid) + '\\analyse'

    # 存在保存的分析结果直接返回分析结果
    if os.path.exists(analysefilepath):
        if os.path.exists(analysefilepath + '\\' + filename):
            lines = []
            with open(analysefilepath + '\\' + filename, 'r+') as file:
                lines = file.readlines()
            print('load data here')
            return JsonResponse(json.loads(lines[0]))
    else:
        os.makedirs(analysefilepath)


    analysefilepath += '\\' + filename

    lines = []
    with open(filepath, 'r+') as file:
        lines = file.readlines()
    # 总语句数量
    sumline = len(lines) - 1

    time_format = "%Y-%m-%d %H:%M:%S.%f"
    starttime = datetime.strptime(json.loads(lines[0])['time'], time_format)
    endtime = datetime.strptime(json.loads(lines[-2])['time'], time_format)
    timing = endtime - starttime

    total_seconds = timing.total_seconds()
    interval_time = total_seconds / 5
    intervals = [starttime + timedelta(seconds=i * interval_time) for i in [1, 2, 3, 4, 5]]
    moment = intervals[0]
    momentcount = 0
    interval_total = 0

    print(timing)
    # 悲伤计数
    sadnesscount = 0
    subemotion = {'like': 0, 'happy': 0, 'angry': 0, 'disgusting': 0, 'fearful': 0, 'sad': 0, 'no obvious': 0}
    sumtimecount = [0, 0, 0, 0, 0]
    emotion = {'pessimistic': 0, 'neutral': 0, 'optimistic': 0}
    membercount = {}
    sumtimesentencescount = [0, 0, 0, 0, 0]
    sentencelenpercentage = [0, 0, 0, 0, 0]
    for line in lines[:-1]:
        line = json.loads(line)

        currnettime = datetime.strptime(line['time'], time_format)
        while currnettime > moment:
            sumtimecount[momentcount] = sumtimecount[momentcount] / interval_total
            momentcount += 1
            moment = intervals[momentcount]
            interval_total = 0
        # 完成悲伤计数
        if line['emotion'] == 'pessimistic':
            sadnesscount = sadnesscount + 1
            sumtimecount[momentcount] += 1
        # 二级情感计数
        subemotion[line['subemotion']] += 1
        #
        interval_total += 1
        # 一级情感计数
        emotion[line['emotion']] += 1
        # 成员对话计数
        sumtimesentencescount[momentcount] += 1
        # 语句长度计数
        count_value = membercount.get(line['username'], 0) + 1
        membercount[line['username']] = count_value
        for k, v in zip([10, 15, 20, 25, 30], [0, 1, 2, 3, 4]):
            if len(line['message']) > k:
                continue
            else:
                sentencelenpercentage[v] += 1
                break
    # 数据变形
    total = sum(membercount.values())
    percentage_membercount = {key: int((value / total) * 100) for key, value in membercount.items()}
    score = sadnesscount / sumline
    score_result = ''
    if score < 0.35:
        score_result = "积极"
    elif 0.35 <= score < 0.5:
        score_result = "较为积极"
    elif 0.5 <= score < 0.65:
        score_result = "较为消极"
    else:
        score_result = "消极"
    # 中英文修改
    translation = {
        'like': '喜欢',
        'happy': '高兴',
        'angry': '愤怒',
        'disgusting': '厌恶',
        'fearful': '害怕',
        'sad': '伤心',
        'no obvious': '无情感'
    }
    translated_subemotion = {translation[key]: value for key, value in subemotion.items()}

    translation = {'pessimistic': '悲观', 'neutral': '中立', 'optimistic': '乐观'}
    emotion_chinese = {translation.get(key, key): value for key, value in emotion.items()}


    # 分析记录写入文件
    with open(analysefilepath, 'w') as file:
        file.writelines(json.dumps({'success': True,
                                    'sumline': sumline,
                                    'mainemotion': score_result,
                                    'subemotion': translated_subemotion,
                                    'sumtimecount': sumtimecount,
                                    'emotion': emotion_chinese,
                                    'membercount': percentage_membercount,
                                    'sumtimesentencescount': sumtimesentencescount,
                                    'sentences': sentencelenpercentage}))


    return JsonResponse({'success': True,
                         'sumline': sumline,
                         'mainemotion': score_result,
                         'subemotion': translated_subemotion,
                         'sumtimecount': sumtimecount,
                         'emotion': emotion_chinese,
                         'membercount': percentage_membercount,
                         'sumtimesentencescount': sumtimesentencescount,
                         'sentences': sentencelenpercentage})


def visualizeall(request):
    return JsonResponse({'success': False})
