
from channels.generic.websocket import WebsocketConsumer
from collections import defaultdict
import json
from .models import Notification, User

allconn = defaultdict(lambda: defaultdict(list))

class NotificationConsumer(WebsocketConsumer):
    global allconn
    
    def connect(self):
        self.userId = self.scope['url_route']['kwargs']['userId']
        allconn[self.userId][len(allconn[self.userId])]=self
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        recipient = text_data_json['recipient']
        userModel = User.objects.get(id=self.userId)
        notification = Notification(user=userModel, content=message, sender=sender, recipient=recipient)
        notification.save()
        for i in allconn[self.userId]:
            allconn[self.userId][i].send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'recipient': recipient,
                'notificationId': notification.id
            }))