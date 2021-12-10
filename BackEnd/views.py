import django.conf
from django.shortcuts import render
from django.views import View
from .models import *
from django.http import JsonResponse
from math import ceil
from pytz import timezone
from .tasks import sendPush

local_timezone = timezone(django.conf.settings.TIME_ZONE)


# Create your views here.
# get ChatRooms
class GetChatRooms(View):

    def get(self, request):

        try:
            chatrooms = ChatRooms.objects.all()
        except Exception as err:
            return JsonResponse({"message": str(err), "status": "ERROR"})
        res = {}
        roomlist = []
        for room in chatrooms:
            temp_dict = {}
            temp_dict["id"] = room.id
            temp_dict["name"] = room.name
            roomlist.append(temp_dict)
        res["data"] = roomlist
        res["status"] = "OK"
        return JsonResponse(res)


class GetMessages(View):

    def get(self, request):

        try:
            chatroom_id = int(request.GET.get("chatroom_id"))
            page = int(request.GET.get("page"))
            messages = Messages.objects.filter(chatroom=chatroom_id).order_by("-id")[(page - 1) * 5:page * 5]
        except Exception as err:
            return JsonResponse({"message": str(err), "status": "ERROR"})
        if messages.count() == 0:
            return JsonResponse({"message": "Illegal parameters", "status": "ERROR"})
        total_pages = ceil(Messages.objects.filter(chatroom=chatroom_id).count() / 5)
        res = {}
        messages_list = []
        data = {}
        for message in messages:
            temp_dict = {}
            temp_dict["message"] = message.message
            temp_dict["name"] = message.name
            # localize the time
            temp_dict["message_time"] = message.message_time.astimezone(local_timezone).strftime("%Y-%m-%d %H:%M:%S")
            temp_dict["user_id"] = message.user_id
            messages_list.append(temp_dict)
        data["current_page"] = page
        data["messages"] = messages_list
        data["total_pages"] = total_pages
        res["data"] = data
        res["status"] = "OK"
        return JsonResponse(res)


class PubMessage(View):

    def post(self, request):
        try:
            chatroom_id = request.POST.get("chatroom_id")
            user_id = request.POST.get("user_id")
            name = request.POST.get("name")
            message = request.POST.get("message")
        except Exception as err:
            return JsonResponse({"message": str(err), "status": "ERROR"})
        pubMessage = Messages(chatroom_id=chatroom_id, user_id=user_id, name=name, message=message)
        try:
            pubMessage.save()
            sendPush.delay(chatroom_id,message)
        except Exception as err:
            return JsonResponse({"message": str(err), "status": "ERROR"})
        return JsonResponse({"status": "OK"})

class PubToken(View):

    def post(self,request):
        try:
            user_id=request.POST.get("user_id")
            token=request.POST.get("token")
        except Exception as err:
            return JsonResponse({"message": str(err),"status": "ERROR"})

        try:
            pubToken = Tokens(user_id=user_id, token=token)
            # update if token has changed
            oldToken = Tokens.objects.get(user_id=user_id)
            oldToken.token=token
            oldToken.save()
        except:
            # save a new record for a new user
            try:
                pubToken = Tokens(user_id=user_id, token=token)
                pubToken.save()
            except Exception as err:
                return JsonResponse({"message": str(err), "status": "ERROR"})
        return JsonResponse({"status": "OK"})