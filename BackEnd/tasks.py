from A3_1155164941.celery import app as celeryApp
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from .models import Tokens

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


@celeryApp.task
def sendPush(title,body):
    registration_tokens = Tokens.objects.all()
    token_list=[]
    for token in registration_tokens:
        token_list.append(token.token)

    message=messaging.MulticastMessage(
        tokens=token_list,
        notification=messaging.Notification(title=title,body=body)
    )
    try:
        response=messaging.send_multicast(message)
        print("Successfully sent message: ",response.success_count)
    except Exception as err:
        print(err)