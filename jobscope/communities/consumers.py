import json

from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from .models import Message, Membership


User = get_user_model()



@database_sync_to_async
def get_membership(user, community_id):
    return Membership.objects.filter(
        user=user,
        community_id=community_id,
        is_blocked=False
    ).first()


@database_sync_to_async
def get_reply_message(reply_to_id):
    if not reply_to_id:
        return None

    return Message.objects.filter(
        id=reply_to_id
    ).first()


@database_sync_to_async
def create_message(user, community_id, message_text, reply_message):
    return Message.objects.create(
        user=user,
        community_id=community_id,
        content=message_text,
        reply_to=reply_message
    )



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]

        self.community_id = self.scope['url_route']['kwargs']['community_id']

        self.room_group_name = f'community_{self.community_id}'


     
        if not self.user or self.user.is_anonymous:

            await self.close()

            return


        membership = await get_membership(
            self.user,
            self.community_id
        )


        
        if not membership:

            await self.close()

            return


        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name

        )


        await self.accept()



    async def receive(self, text_data):

        data = json.loads(text_data)

        message_text = data.get("message")

        reply_to_id = data.get("reply_to")


        membership = await get_membership(
            self.user,
            self.community_id
        )


        if not membership:

            return


        reply_message = await get_reply_message(
            reply_to_id
        )


        message_obj = await create_message(

            self.user,

            self.community_id,

            message_text,

            reply_message

        )


        await self.channel_layer.group_send(

            self.room_group_name,

            {

                "type": "chat_message",

                "message": message_obj.content,

                "user": self.user.username if self.user.username else self.user.email.split("@")[0],

                "message_id": message_obj.id,

                "reply_to": reply_to_id

            }

        )



    async def chat_message(self, event):

        await self.send(

            text_data=json.dumps(event)

        )



class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]


        if not self.user or self.user.is_anonymous:

            await self.close()

            return


        self.group_name = f"user_{self.user.id}"


        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            "global_notifications",
            self.channel_name
        )


        await self.accept()



    async def notify(self, event):

        await self.send(

            text_data=json.dumps({

                "message": event["message"]

            })

        )