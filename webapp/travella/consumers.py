import json
from django.utils.timezone import localtime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from travella.exceptions.business_exception import BusinessException

class ServiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        self.customer_id = self.scope['url_route']['kwargs']['customer_id']
        self.room_group_name = f'chat_{self.customer_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message_text = data['message']

        from travella.domains.models.account_models import Account
        account: Account = self.user
        # --- CHECK LIMIT BEFORE SAVING ---
        from travella.domains.models.limit_models import AccountLimit
        from travella.services import account_limit_service
        if account.role == Account.Role.CUSTOMER.value:
            try:
                await database_sync_to_async(account_limit_service.check_limit)(
                    account.id, AccountLimit.Type.CHAT
                )
            except BusinessException as e:
                # send alert to client
                limit_counts = await database_sync_to_async(account_limit_service.get_limit_counts)(
                                account.id, AccountLimit.Type.CHAT
                            )
                await self.send(text_data=json.dumps({
                    'type': 'limit_alert',
                    'message': e.get_message(),
                    'limit_counts': limit_counts,
                }))
                return  # do not save message

        # --- Determine receiver ---
        receiver_id = None if account.role == Account.Role.CUSTOMER.value else self.customer_id
        limit_counts = await database_sync_to_async(account_limit_service.get_limit_counts)(
                        account.id, AccountLimit.Type.CHAT
                    )

        # --- Save message ---
        msg = await self.save_message(
            sender_id=str(account.id),
            receiver_id=receiver_id,
            customer_id=self.customer_id,
            content=message_text
        )

        # --- Broadcast to room ---
        accountdetail = await self.get_account_detail(account)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': str(account.id),
                'sender_name': accountdetail.name,
                'sender_avatar': accountdetail.photo.url if accountdetail.photo else '',
                'sender_type': 'customer' if account.role == Account.Role.CUSTOMER.value else 'admin',
                'created_at': msg.created_at.isoformat(),
                'limit_counts': limit_counts,
            }
        )

        # --- Mark messages as read ---
        await self.mark_messages_as_read_in_room()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'sender_avatar': event['sender_avatar'],
            'sender_type': event['sender_type'],
            'created_at': event['created_at'],
            'limit_counts': event['limit_counts'],
        }))
        await self.mark_messages_as_read_in_room()

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, customer_id, content):
        from travella.domains.models.account_models import Account
        from travella.domains.models.chat_message_models import ChatMessage

        sender = Account.objects.get(id=sender_id)
        receiver = Account.objects.get(id=receiver_id) if receiver_id else None
        customer = Account.objects.get(id=customer_id)

        msg = ChatMessage(sender=sender, receiver=receiver, customer=customer, content=content)
        msg.save()
        return msg

    @database_sync_to_async
    def mark_messages_as_read_in_room(self):
        from travella.domains.models.chat_message_models import ChatMessage

        ChatMessage.objects.filter(
            customer_id=self.customer_id,
            is_read=False
        ).exclude(sender_id=self.user.id).update(is_read=True)

    @database_sync_to_async
    def get_account_detail(self, user):
        return user.accountdetail
