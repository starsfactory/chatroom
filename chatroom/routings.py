from django.urls import re_path
from chat import consumers


websocket_urlpatterns=[
    re_path(r'room/(?P<group>\d+)/$', consumers.ChatRoom.as_asgi())
]

