from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from .models import Word, User, SendTime
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import os
import requests
import deepl

# Create your views here.

# deletes words from database
# TODO: authenticate token for security
@csrf_exempt
@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def delete_word(request):
    data = json.loads(request.body)
    word = data['word']
    user_info = data['userInfo']
    google_id = user_info['sub']
    Word.objects.get(original = word, user=User.objects.get(google_id=google_id)).delete()
    return HttpResponse(status=204)


# saves words to database
# TODO: authenticate token for security
@csrf_exempt
@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def save_word(request):
    data = json.loads(request.body)
    word = data['word']
    translation = data['translation']
    user_info = data['userInfo']
    google_id = user_info['sub']
    user_email = user_info['email']
    if not User.objects.filter(google_id=google_id):
        User.objects.create(google_id=google_id, user_email=user_email)
    Word.objects.create(original=word, translation=translation, user=User.objects.get(google_id=google_id))
    return HttpResponse(status=204)

@csrf_exempt
@api_view(('POST',))
def translate(request):
    word = json.loads(request.body)['word']
    try:
        translator
    except UnboundLocalError:
        translator = deepl.Translator(os.environ['DEEPL_AUTH_KEY'])
    res = translator.translate_text(word, target_lang='EN-US')
    return JsonResponse({'word':word, 'translation':str(res)})


# save updated user settings to database
@csrf_exempt
@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def update(request):
    data = json.loads(request.body)
    user_info = data['userInfo']
    google_id = user_info['sub']
    user_email = user_info['email']
    time_vals = data["timeVals"]
    # save user to database if they are first time user
    if not User.objects.filter(google_id=google_id):
        new_user = User.objects.create(google_id=google_id, user_email=user_email, send_to_phone=data['sendToPhone'], send_to_email=data['sendToEmail'], phone_number=data['phoneNumber'], num_words=data['numWords'])
        # add element to foreign key field (times of day that user wishes to receive words)
        for time in time_vals:
            new_user.send_times.add(SendTime.objects.get(hour=time))
    user = User.objects.get(google_id=user_info['sub'])
    user.send_to_phone = data['sendToPhone']
    user.send_to_email = data['sendToEmail']
    user.phone_number = data['phoneNumber']
    user.num_words = data['numWords']
    # clear user's time settings and reset
    user.send_times.clear()
    for time in time_vals:
            user.send_times.add(SendTime.objects.get(hour=time))
    user.save()
    return JsonResponse({'message':'successfully updated user settings'},status=204)
