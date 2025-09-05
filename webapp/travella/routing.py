from django.urls import re_path

from travella import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<customer_id>[^/]+)/$', consumers.ServiceChatConsumer.as_asgi()),
]