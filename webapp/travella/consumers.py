import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ServiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            print("Anonymous user tried to connect")
            await self.close()
            return

        self.customer_id = self.scope['url_route']['kwargs']['customer_id']
        self.room_group_name = f'chat_{self.customer_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message_text = data['message']
        from travella.domains.models.account_models import Account
        from travella.domains.models.chat_message_models import ChatMessage
        account: Account = self.user

        # receiver logic (simplified for shared admin chat)
        if account.role == Account.Role.CUSTOMER.value:
            receiver_id = None  # any admin can see
        else:
            receiver_id = self.customer_id

        await self.save_message(
            sender_id=str(self.user.id),
            receiver_id=receiver_id,
            customer_id=self.customer_id,
            content=message_text
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': str(self.user.id),
                'sender_type': 'customer' if account.role == Account.Role.CUSTOMER.value else 'admin',
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_type': event['sender_type'],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, customer_id, content):
        from travella.domains.models.account_models import Account
        from travella.domains.models.chat_message_models import ChatMessage
        sender = Account.objects.get(id=sender_id)
        receiver = Account.objects.get(id=receiver_id) if receiver_id else None
        customer = Account.objects.get(id=customer_id)
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            customer=customer,
            content=content
        )
