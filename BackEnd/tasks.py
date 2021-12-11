from A3_1155164941.celery import app as celeryApp
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from .models import Tokens

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


@celeryApp.task
def sendPush(chatroom_id, message):
    registration_tokens = Tokens.objects.all()
    token_list = []
    for token in registration_tokens:
        token_list.append(token.token)

    msg = messaging.MulticastMessage(
        tokens=token_list,
        data={
            'chatroom_id': chatroom_id,
            'chatroom_name': 'Chatroom ' + chatroom_id,
            'message': message
        },
        # notification=messaging.Notification(title=chatroom_id,body=message)
    )
    try:
        response = messaging.send_multicast(msg)
        print("Successfully sent message: ", response.success_count)
    except Exception as err:
        print(err)
